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

from __future__ import print_function

import json
import demjson
import datetime

from copy import deepcopy
from urlparse import urlsplit, urlunsplit, parse_qs, parse_qsl
from urllib import quote, quote_plus, unquote

from constants.sources import SOURCES

from config import CONFIG


def manual_quote(str_in):
    """
    Custom function to perform quoting
    :param str_in: str to quote
    :return: quotes string
    """
    always_safe = set(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                           'abcdefghijklmnopqrstuvwxyz'
                           '0123456789' '_.-'))
    str_out = ""
    for char in str_in:
        if char not in always_safe:
            str_out += "%%%02x" % ord(char)
        else:
            str_out += char

    return str_out


def recursive_replace(data_in, replace_value, replace_with):
    """
    Replace the specified value recursively in the provided object by the payload.
    :param data_in: the object which should be replaced
    :param replace_value: the value which should be replaced
    :param replace_with: the value it should be replaced with
    :return: the object in which the value is replaced
    """
    if isinstance(data_in, int):
        return recursive_replace(str(data_in), replace_value, replace_with)
    if isinstance(data_in, dict):
        data_out = dict()
        for key, value in data_in.items():
            if isinstance(key, int):
                key = str(key)
            if isinstance(value, str) or isinstance(value, unicode):
                data_out[key.replace(replace_value, replace_with)] = value.replace(replace_value, replace_with)
            elif isinstance(value, dict):
                data_out[key.replace(replace_value, replace_with)] = recursive_replace(value, replace_value,
                                                                                       replace_with)
            elif isinstance(value, list):
                data_out[key.replace(replace_value, replace_with)] = recursive_replace(value, replace_value,
                                                                                       replace_with)
            elif isinstance(value, int):
                data_out[key.replace(replace_value, replace_with)] = recursive_replace(value, replace_value,
                                                                                       replace_with)
            else:
                data_out[key.replace(replace_value, replace_with)] = value

    elif isinstance(data_in, list):
        data_out = []
        for element in data_in:
            if isinstance(element, str) or isinstance(element, unicode):
                element = element.replace(replace_value, replace_with)
                data_out.append(element)
            else:
                data_out.append(recursive_replace(element, replace_value, replace_with))
    elif isinstance(data_in, str):
        return data_in.replace(replace_value, replace_with)
    elif data_in is None:
        return data_in
    else:
        raise Exception("No such thing %s" % (type(data_in)))
    return data_out


def is_json(value):
    """
    Heuristic to check whether a given string is in JSON format to prevent costly parse attempts.
    :param value: the value to check
    :return: bool indicating judgement
    """
    value = value.strip()
    if value.startswith("{") and value.endswith("}"):
        return True
    if value.startswith("[") and value.endswith("]"):
        return True
    value = unquote(value)
    if value.startswith("{") and value.endswith("}"):
        return True
    if value.startswith("[") and value.endswith("]"):
        return True
    return False


def try_parse_json(storage_value):
    """
    Try to parse the provided value as JSON/JS objects.
    :param storage_value: the value to parse
    :return: the parsed value or None if not parseable
    """
    try:
        loaded = json.loads(storage_value)
        if type(loaded) in (dict, list):
            return loaded
    except ValueError:
        try:
            loaded = json.loads(unquote(storage_value))
            if type(loaded) in (dict, list):
                return loaded
        except ValueError:
            pass
    try:
        loaded = demjson.decode(storage_value)
        if type(loaded) in (dict, list):
            return loaded
    except Exception, e:
        try:
            loaded = demjson.decode(unquote(storage_value))
            if type(loaded) in (dict, list):
                return loaded
        except Exception, e:
            pass

    return None


def find_match(items, tainted_value):
    """
    Fuzzily find the tainted value in the respective storage entry.
    :param items: the storage containing all the observed kvps
    :param tainted_value: the value to find
    :return: list of matched kvps annotated with context(e.g. whether or not the value was only found quoted)
    """
    tainted_value = tainted_value.decode("ascii", "ignore")
    matches = []
    log("Looking for %s" % tainted_value)
    if is_json(tainted_value):
        tainted_value_dic = try_parse_json(tainted_value)
    else:
        tainted_value_dic = None
    for key, storage_value, storage_type in items:
        if not storage_value:
            continue
        if tainted_value in storage_value:
            if storage_value.lower()[:3] in ("%7b", "%5b"):
                matches.append([key, tainted_value, storage_value, False, "quoted"])
            else:
                matches.append([key, tainted_value, storage_value, False, "plain"])
            continue
        if unquote(tainted_value) in unquote(storage_value):
            matches.append([key, unquote(tainted_value), unquote(storage_value), False, "quoted"])
            continue
        if not tainted_value_dic:
            continue
        try:
            if is_json(storage_value):
                storage_value_dic = try_parse_json(storage_value)
            else:
                storage_value_dic = None
            if isinstance(storage_value_dic, dict) and isinstance(tainted_value_dic, dict):
                keys_matching = set(storage_value_dic.keys()) & set(tainted_value_dic.keys())
                if len(keys_matching) and len(keys_matching) == len(tainted_value_dic.keys()):
                    if storage_value.lower()[:3] in ("%7b", "%5b"):
                        matches.append([key, tainted_value, storage_value, False, "dic_keys_quoted"])
                    else:
                        matches.append([key, tainted_value, storage_value, False, "dic_keys"])
                    continue
                elif len(keys_matching):
                    if storage_value.lower()[:3] in ("%7b", "%5b"):
                        matches.append([key, tainted_value, storage_value, False, "somewhat_dic_keys_quoted"])
                    else:
                        matches.append([key, tainted_value, storage_value, False, "somewhat_dic_keys"])
                    continue
                else:
                    pass
        except Exception as e:
            log('Unable to find match due to Exception {}'.format(e))
    return matches


def build_reflected_exploit(finding, replace_with, replace_value, source, url=None):
    """
    Helper function to generate RCXSS exploits given the value to replace and the payload.
    :param finding: the finding which is currently investigated
    :param replace_with: the payload
    :param replace_value: the value to replace
    :param source: the source from which this flow originated(e.g. SOURCE_LOCATION_HREF)
    :param url: optional url where the flow was found
    :return: list of exploit url candidates
    """
    try:
        replace_value = str(replace_value)
    except:
        pass
    log("building RCXSS URL for ({},{},{})".format(finding, repr(replace_with), repr(replace_value)))

    # url, break_out, payload, break_in, domain, sink, d3, source, value_part, finding, flowhash, position = row
    if url is None:
        url = finding["url"]

    d3 = finding["d3"]
    exploit_urls = list()

    if "connect.facebook.net" in d3:
        return

    if len(replace_value) < 3 and url.count(replace_value) > 2:
        log('value which should be replaced is too small, such that substitution makes no sense!')
        return

    if replace_value in ["facebook", "http", "https", "com", "/", "http:", "https:", "ht"]:
        log('Found value which are known to only generate erroneous subsititions!')
        return

    domain = urlsplit(url).netloc
    if domain in ["platform.twitter.com", "platform.linkedin.com"]:
        log('Found domains which are not susceptible but generate lots of URLs')
        return

    parsed_url = urlsplit(url)
    # URL starts with what we control, but flow does not use complete URL: we cannot exploit this
    if url.startswith(replace_value) and replace_value != url:
        log('Value flown into sink is not under out control!')
        return

    if replace_value in parsed_url.netloc:
        try:
            if bytes(unquote(url)).count(bytes(unquote(replace_value))) == 1:
                log('Value only originates from the netlocation so no substitution is possible!')
                return
        except UnicodeEncodeError:
            pass
    if replace_value in parsed_url.path and url.count(replace_value) < 2 and not url.endswith(replace_value):
        log('Value only originates from path so no substitution is possible!')
        return

    if source in [SOURCES.SOURCE_LOCATION_HREF, SOURCES.SOURCE_URL, SOURCES.SOURCE_DOCUMENT_URI,
                  SOURCES.SOURCE_BASE_URI]:
        # ensure that injection is actually where we can control it, so either in the query or fragment
        query = parsed_url.query
        fragment = parsed_url.fragment

        if replace_value == url and replace_with.startswith(replace_value):
            # easy case, just take the whole URL, no need for further urls
            return [
                url.replace(replace_value, replace_with),
                url.replace(replace_value, replace_value + "#" + replace_with[len(replace_value):])]

        if replace_value.startswith('#') and replace_value == '#' + fragment:
            return [url.replace('#' + fragment, replace_with)]

        if replace_value.startswith('?') and replace_value == '?' + query:
            return [
                url.replace(replace_value, replace_with),
                url.replace(replace_value, replace_value + "#" + replace_with[len(replace_value):])
            ]

        if "&" not in replace_value and "=" not in replace_value:
            # check if the injection is its own GET parameter
            query_params = parse_qsl(query)
            for i, (key, value) in enumerate(query_params):
                copied_query_params = deepcopy(query_params)
                # cycle GET parameter to the end
                value = value.encode('ascii', 'ignore')
                assert isinstance(value, str)
                if matches_value(needle=replace_value, haystack=value) or replace_value in value:
                    del copied_query_params[i]
                    new_value = str(value).replace(bytes(replace_value), bytes(replace_with))
                    copied_query_params.append((key, new_value))

                    # default case, no hash tag

                    def asciify(s):
                        if not all(ord(c) < 128 for c in s):
                            return quote_plus(s)
                        return s

                    new_query = "&".join(['%s=%s' % (asciify(k), asciify(v))
                                          for k, v in copied_query_params])
                    exploit_url = urlunsplit([parsed_url.scheme, parsed_url.netloc, parsed_url.path,
                                              new_query, parsed_url.fragment])
                    exploit_urls.append(exploit_url)

                    # add a hashtag just in case
                    copied_query_params.pop(-1)
                    copied_query_params.append((key, value))
                    if len(parsed_url.fragment):
                        new_fragment = replace_with + parsed_url.fragment
                    else:
                        new_fragment = replace_with
                    new_query = "&".join(['%s=%s' % (asciify(k), asciify(v))
                                          for k, v in copied_query_params])
                    exploit_url = urlunsplit([parsed_url.scheme, parsed_url.netloc, parsed_url.path,
                                              new_query, new_fragment])
                    exploit_urls.append(exploit_url)
        elif '=' in replace_value and replace_value in query:
            new_query = query.replace(replace_value, replace_with)
            exploit_url = urlunsplit([parsed_url.scheme, parsed_url.netloc, parsed_url.path,
                                      new_query, parsed_url.fragment])
            exploit_urls.append(exploit_url)

        if len(exploit_urls):
            return exploit_urls

        try:
            if replace_value in query:
                new_query = query.replace(replace_value, replace_with)
                exploit_url = urlunsplit([parsed_url.scheme, parsed_url.netloc, parsed_url.path,
                                          new_query, parsed_url.fragment])
                return [exploit_url]
            elif replace_value in unquote(query):
                new_query = replace_quoted(query, replace_value, replace_with[len(replace_value):])
                exploit_url = urlunsplit([parsed_url.scheme, parsed_url.netloc, parsed_url.path,
                                          new_query, parsed_url.fragment])
                return [exploit_url]
        except UnicodeDecodeError:
            log('Encountered Unicode Error when replacing the value in the URL!')
        if replace_value in fragment:
            exploit_payload = replace_with
            exploit_url = urlunsplit([parsed_url.scheme, parsed_url.netloc, parsed_url.path,
                                      parsed_url.query, parsed_url.fragment.replace(replace_value, exploit_payload)])
            return [exploit_url]
        elif replace_value in "#" + fragment and len(replace_value) > 1 and replace_value[0] == '#':
            exploit_payload = replace_with[len(replace_value):]
            exploit_url = urlunsplit([parsed_url.scheme, parsed_url.netloc, parsed_url.path,
                                      parsed_url.query,
                                      parsed_url.fragment.replace(replace_value[1:], exploit_payload)])
            return [exploit_url]
        elif replace_value in unquote(fragment):
            new_fragment = replace_quoted(fragment, replace_value, replace_with[len(replace_value):])
            exploit_url = urlunsplit([parsed_url.scheme, parsed_url.netloc, parsed_url.path,
                                      parsed_url.query, new_fragment])
            return [exploit_url]

        if len(exploit_urls) == 0:
            # fallback, just append?
            if replace_with.startswith(replace_value):
                exploit_urls.append(url + "#" + replace_with[len(replace_value):])

    elif source == SOURCES.SOURCE_LOCATION_SEARCH:
        # we only need to look at the query parameters for replacement, then
        query = "?" + parsed_url.query

        if replace_value in query:
            # ok, unquoted attribute
            new_query = query.replace(replace_value, replace_with)
            exploit_url = urlunsplit([parsed_url.scheme, parsed_url.netloc, parsed_url.path,
                                      new_query[1:], parsed_url.fragment])
            exploit_urls.append(exploit_url)

        elif replace_value.lower() in query.lower():
            offset = query.lower().find(replace_value.lower())
            exploit_payload = replace_with
            new_query = query[:offset] + exploit_payload + query[offset + len(replace_value):]
            exploit_url = urlunsplit([parsed_url.scheme, parsed_url.netloc, parsed_url.path,
                                      new_query[1:], parsed_url.fragment])
            exploit_urls.append(exploit_url)

        elif replace_value.lower() in unquote(query).lower():
            for i in xrange(0, len(query)):
                if unquote(query[i:]).lower().startswith(replace_value.lower()):
                    remainder = query[i:]
                    for j in xrange(len(remainder), 0, -1):
                        if unquote(remainder[:j]).lower() == replace_value.lower():
                            exploit_payload = quote(replace_with)
                            new_query = query[:i] + exploit_payload + query[j:]
                            exploit_url = urlunsplit([parsed_url.scheme, parsed_url.netloc, parsed_url.path,
                                                      new_query[1:], parsed_url.fragment])
                            exploit_urls.append(exploit_url)
        elif replace_value.lower() == "?" + query.lower():
            new_query = query + "&foo=" + replace_with
            exploit_url = urlunsplit([parsed_url.scheme, parsed_url.netloc, parsed_url.path,
                                      new_query[1:], parsed_url.fragment])
            exploit_urls.append(exploit_url)
        else:
            parsed_query = parse_qs(query)
            sorted_query = sorted(parsed_query.items(), key=lambda x: -len(x[1][0]))
            for key, value in sorted_query:
                if isinstance(value, list):
                    value = value[0]
                if value in replace_value:
                    exploit_payload = "=" + replace_with
                    new_query = query.replace("=" + value, exploit_payload)
                    exploit_url = urlunsplit([parsed_url.scheme, parsed_url.netloc, parsed_url.path,
                                              new_query[1:], parsed_url.fragment])
                    exploit_urls.append(exploit_url)

    elif source == SOURCES.SOURCE_LOCATION_HASH:
        # we only need to look at the hash for replacement, then
        if replace_value.startswith("#") and replace_with.startswith("#"):
            replace_value = replace_value[1:]
            replace_with = replace_with[1:]
        fragment = parsed_url.fragment
        # WARNING: fragment does not contain a hash!!!

        if replace_value in fragment:
            # ok, unquoted attribute
            new_fragment = fragment.replace(replace_value, replace_with)
            exploit_url = urlunsplit([parsed_url.scheme, parsed_url.netloc, parsed_url.path,
                                      parsed_url.query, new_fragment])
            exploit_urls.append(exploit_url)
            # if we have an = in the URL, there is a chance that the whole things get split
            # so, we try to encode the =
            # example: https://widget.pushbullet.com/widget.html#channel=am-1071836729&code=6821&widget=button&size=large
            if '=' in fragment:
                new_fragment = fragment.replace(replace_value, replace_with.replace('=', '%3D'))
                exploit_url = urlunsplit([parsed_url.scheme, parsed_url.netloc, parsed_url.path,
                                          parsed_url.query, new_fragment])
                exploit_urls.append(exploit_url)

        elif quote(replace_value).lower() in fragment.lower():
            # ok, quoted attribute
            exploit_payload = quote(replace_with)

            offset = fragment.lower().find(quote(replace_value).lower())
            new_fragment = fragment[:offset] + exploit_payload + fragment[offset + len(quote(replace_value)):]

            exploit_url = urlunsplit([parsed_url.scheme, parsed_url.netloc, parsed_url.path,
                                      parsed_url.query, new_fragment])
            exploit_urls.append(exploit_url)

        elif quote_plus(replace_value).lower() in fragment.lower():
            # ok, quoted attribute
            exploit_payload = quote_plus(replace_with)

            offset = fragment.lower().find(quote_plus(replace_value).lower())
            new_fragment = fragment[:offset] + exploit_payload + fragment[offset + len(quote_plus(replace_value)):]

            exploit_url = urlunsplit([parsed_url.scheme, parsed_url.netloc, parsed_url.path,
                                      parsed_url.query, new_fragment])
            exploit_urls.append(exploit_url)

        elif quote_without_plus(replace_value).lower() in fragment.lower():
            # ok, quoted attribute
            exploit_payload = quote_without_plus(replace_with)

            offset = fragment.lower().find(quote_without_plus(replace_value).lower())
            new_fragment = fragment[:offset] + exploit_payload + fragment[
                                                                 offset + len(quote_without_plus(replace_value)):]

            exploit_url = urlunsplit([parsed_url.scheme, parsed_url.netloc, parsed_url.path,
                                      parsed_url.query, new_fragment])
            exploit_urls.append(exploit_url)

        elif replace_value.lower() in fragment.lower():
            # lower case match
            exploit_payload = replace_with

            offset = fragment.lower().find(replace_value.lower())
            new_fragment = fragment[:offset] + exploit_payload + fragment[offset + len(replace_value):]

            exploit_url = urlunsplit([parsed_url.scheme, parsed_url.netloc, parsed_url.path,
                                      parsed_url.query, new_fragment])
            exploit_urls.append(exploit_url)

        elif replace_value in unquote(fragment):
            for i in xrange(0, len(fragment)):
                if unquote(fragment[i:]).startswith(replace_value):
                    remainder = fragment[i:]
                    for j in xrange(len(remainder), 0, -1):
                        if unquote(remainder[:j]) == replace_value:
                            exploit_payload = quote(replace_with)
                            new_fragment = fragment[:i] + exploit_payload + fragment[j:]
                            exploit_url = urlunsplit([parsed_url.scheme, parsed_url.netloc, parsed_url.path,
                                                      parsed_url.query, new_fragment])
                            exploit_urls.append(exploit_url)

    if not len(exploit_urls):
        return None
    return exploit_urls


def replace_quoted(input, value_part, replacement, remove_value_part=False):
    """
    Replace values in a quoted environment e.g. location.search.
    :param input: the value to replace in
    :param value_part: the value part to replace
    :param replacement: the payload
    :param remove_value_part: indication whether the tainted value should be removed
    :return: the substituted string if successful, empty string otherwise
    """
    for i in xrange(0, len(input)):
        if unquote(input[i:]).lower().startswith(value_part.lower()):
            remainder = input[i:]
            for j in xrange(len(remainder), 0, -1):
                if unquote(remainder[:j]).lower() == value_part.lower():
                    if remove_value_part:
                        exploit_payload = quote(replacement)
                    else:
                        exploit_payload = quote(value_part + replacement)
                    return input[:i] + exploit_payload + input[i + j:]
    return ""


def quote_without_plus(input):
    return quote_plus(input).replace("+", "%20").replace("#", "%23")


def substring_match(value_part, query, windowsize=10):
    for i in xrange(0, len(value_part)):
        if value_part[i:i + windowsize] in query:
            return True
    return False


def matches_value(needle, haystack):
    """
    Check whether the searched value is present within the storage entry
    :param needle: value to search for
    :param haystack: value in which the needle should be searched for
    :return: bool indicating success
    """
    if needle == haystack:
        return True
    if unquote(needle) == haystack:
        return True
    if needle == unquote(haystack):
        return True
    if unquote(needle) == unquote(haystack):
        return True
    return False


def log(st):
    """
    Log functionality. Controllable via the config option --debug.
    :param st: string to log
    :return: None
    """
    if CONFIG.debug:
        ts = datetime.datetime.now()
        print(str(ts), ":", st)
