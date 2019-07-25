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

import string

from HTMLParser import HTMLParser
from breakouts import breakouts
from utils import log

from constants.HTMLstates import HTMLStates

ALPHA_NUM = string.ascii_letters + string.digits


def find_tag_to_close(tag_name, opened_tags):
    for i in range(len(opened_tags) - 1, -1, -1):
        if opened_tags[i]['name'] == tag_name:
            return opened_tags[i]
    return None


class HTMLStateMachine:
    """
    HTMLStateMachine parsing according to the https://www.w3.org/TR/2011/WD-html5-20110113/tokenization.html

    functions prefixed with handle_ refer to the handler functions which should be called when a transition
    happens in that particular state. The transition_dict captures as kvp the state and its associated function
    and is generated in the __init__. This allows the processInput function to lookup the corresponding handler
    and apply the transition.

    """

    def consumeNextChar(self):
        """
        Pop the current tos and return it.
        :return: current tos
        """
        tos = self.input[0]
        self.input = self.input[1:]
        return tos

    def getState(self):
        """
        Get the current state.
        :return: state
        """
        return self.state

    def consumeCharRef(self):
        """
        Consume a char ref as specified in the standard.
        :return: the parsed char ref
        """
        return self.handle_TOKENIZING_CHAR_REF()

    def processInput(self):
        """
        process the remaining input until we have reached the end of the current input
        :return: the state at the end of the parsed input
        """
        while self.input != "":
            self.transitions[self.state]()
        return self.state

    def feed(self, new_input):
        """
        Append input to the end of the not yet parsed input
        :param new_input: new input to subsequently parse
        :return: None
        """
        self.input += new_input

    def __init__(self):
        self._in_opening_tag = False
        self.input = ""
        self.buffered_text = ""
        self.additional_allowed_char = ""
        self.state = HTMLStates.DATA_STATE
        self.current_tag = {}
        # Example tag entry:
        #
        # {
        #  name: TAGNAME,
        #  is_self_closing: BOOL,
        #  attributes: [
        #   {
        #       name: NAME,
        #       value: VALUE
        #   },
        #    ...
        #  ],
        #  data: TEXT,
        #  ...
        # }
        self.opened_tags = []
        self.closed_tags = []
        transition_dict = dict()
        # 8.2.4.1 Data state
        transition_dict[HTMLStates.DATA_STATE] = self.handle_DATA_STATE
        # 8.2.4.2 Character reference in data state
        transition_dict[HTMLStates.CHAR_REF_DATA_STATE] = self.handle_CHAR_REF_IN_DATA_STATE
        # 8.2.4.3 RCDATA state
        transition_dict[HTMLStates.RCDATA_STATE] = self.handle_RC_DATA_STATE
        # 8.2.4.4 Character reference in RCDATA state
        transition_dict[HTMLStates.CHAR_REF_IN_RCDATA_STATE] = self.handle_CHAR_REF_IN_RCDATA_STATE
        # 8.2.4.5 RAWTEXT state
        transition_dict[HTMLStates.RAWTEXT_STATE] = self.handle_RAWTEXT_STATE
        # 8.2.4.6 Script data state
        transition_dict[HTMLStates.SCRIPT_DATA_STATE] = self.handle_SCRIPT_DATA_STATE
        # 8.2.4.7 PLAINTEXT state
        transition_dict[HTMLStates.PLAINTEXT_STATE] = self.handle_PLAINTEXT_STATE
        # 8.2.4.8 Tag open state
        transition_dict[HTMLStates.TAG_OPEN_STATE] = self.handle_TAG_OPEN_STATE
        # 8.2.4.9 End tag open state
        transition_dict[HTMLStates.END_TAG_OPEN_STATE] = self.handle_END_TAG_OPEN_STATE
        # 8.2.4.10 Tag name state
        transition_dict[HTMLStates.TAG_NAME_STATE] = self.handle_TAG_NAME_STATE
        # 8.2.4.11 RCDATA less-than sign state
        transition_dict[HTMLStates.RCDATA_LESS_THAN_SIGN_STATE] = self.handle_RCDATA_LESS_THAN_SIGN_STATE
        # 8.2.4.12 RCDATA end tag open state
        transition_dict[HTMLStates.RCDATA_END_TAG_OPEN_STATE] = self.handle_RCDATA_END_TAG_OPEN_STATE
        # 8.2.4.13 RCDATA end tag name state
        transition_dict[HTMLStates.RCDATA_END_TAG_NAME_STATE] = self.handle_RCDATA_END_TAG_NAME_STATE
        # 8.2.4.14 RAWTEXT less-than sign state
        transition_dict[HTMLStates.RAWTEXT_LESS_THAN_SIGN_STATE] = self.handle_RAWTEXT_LESS_THAN_SIGN_STATE
        # 8.2.4.15 RAWTEXT end tag open state
        transition_dict[HTMLStates.RAWTEXT_END_TAG_OPEN_STATE] = self.handle_RAWTEXT_END_TAG_OPEN_STATE
        # 8.2.4.16 RAWTEXT end tag name state
        transition_dict[HTMLStates.RAWTAG_END_TAG_NAME_STATE] = self.handle_RAWTAG_END_TAG_NAME_STATE
        # 8.2.4.17 Script data less-than sign state
        transition_dict[HTMLStates.SCRIPT_DATA_LESS_THAN_SIGN_STATE] = self.handle_SCRIPT_DATA_LESS_THAN_SIGN_STATE
        # 8.2.4.18 Script data end tag open state
        transition_dict[HTMLStates.SCRIPT_DATA_END_TAG_OPEN_STATE] = self.handle_SCRIPT_DATA_END_TAG_OPEN_STATE
        # 8.2.4.19 Script data end tag name state
        transition_dict[HTMLStates.SCRIPT_DATA_END_TAG_NAME_STATE] = self.handle_SCRIPT_DATA_END_TAG_NAME_STATE
        # 8.2.4.20 Script data escape start state
        transition_dict[HTMLStates.SCRIPT_DATA_ESCAPE_START_STATE] = self.handle_SCRIPT_DATA_ESCAPE_START_STATE
        # 8.2.4.21 Script data escape start dash state
        transition_dict[
            HTMLStates.SCRIPT_DATA_ESCAPE_START_DASH_STATE] = self.handle_SCRIPT_DATA_ESCAPE_START_DASH_STATE
        # 8.2.4.22 Script data escaped state
        transition_dict[HTMLStates.SCRIPT_DATA_ESCAPED_STATE] = self.handle_SCRIPT_DATA_ESCAPED_STATE
        # 8.2.4.23 Script data escaped dash state
        transition_dict[HTMLStates.SCRIPT_DATA_ESCAPED_DASH_STATE] = self.handle_SCRIPT_DATA_ESCAPED_DASH_STATE
        # 8.2.4.24 Script data escaped dash dash state
        transition_dict[
            HTMLStates.SCRIPT_DATA_ESCAPED_DASH_DASH_STATE] = self.handle_SCRIPT_DATA_ESCAPED_DASH_DASH_STATE
        # 8.2.4.25 Script data escaped less-than sign state
        transition_dict[
            HTMLStates.SCRIPT_DATA_ESCAPED_LESS_THAN_SIGN_STATE] = self.handle_SCRIPT_DATA_ESCAPED_LESS_THAN_SIGN_STATE
        # 8.2.4.26 Script data escaped end tag open state
        transition_dict[
            HTMLStates.SCRIPT_DATA_ESCAPED_END_TAG_OPEN_STATE] = self.handle_SCRIPT_DATA_ESCAPED_END_TAG_OPEN_STATE
        # 8.2.4.27 Script data escaped end tag name state
        transition_dict[
            HTMLStates.SCRIPT_DATA_ESCAPED_END_TAG_NAME_STATE] = self.handle_SCRIPT_DATA_ESCAPED_END_TAG_NAME_STATE
        # 8.2.4.28 Script data double escape start state
        transition_dict[
            HTMLStates.SCRIPT_DATA_DOUBLE_ESCAPE_START_STATE] = self.handle_SCRIPT_DATA_DOUBLE_ESCAPE_START_STATE
        # 8.2.4.29 Script data double escaped state
        transition_dict[HTMLStates.SCRIPT_DATA_DOUBLE_ESCAPED_STATE] = self.handle_SCRIPT_DATA_DOUBLE_ESCAPED_STATE
        # 8.2.4.30 Script data double escaped dash state
        transition_dict[
            HTMLStates.SCRIPT_DATA_DOUBLE_ESCAPED_DASH_STATE] = self.handle_SCRIPT_DATA_DOUBLE_ESCAPED_DASH_STATE
        # 8.2.4.31 Script data double escaped dash dash state
        transition_dict[
            HTMLStates.SCRIPT_DATA_DOUBLE_ESCAPED_DASH_DASH_STATE] = self.handle_SCRIPT_DATA_DOUBLE_ESCAPED_DASH_DASH_STATE
        # 8.2.4.32 Script data double escaped less-than sign state
        transition_dict[
            HTMLStates.SCRIPT_DATA_DOUBLE_ESCAPED_LESS_THAN_SIGN_STATE] = self.handle_SCRIPT_DATA_DOUBLE_ESCAPED_LESS_THAN_SIGN_STATE
        # 8.2.4.33 Script data double escape end state
        transition_dict[
            HTMLStates.SCRIPT_DATA_DOUBLE_ESCAPE_END_STATE] = self.handle_SCRIPT_DATA_DOUBLE_ESCAPE_END_STATE
        # 8.2.4.34 Before attribute name state"""
        transition_dict[HTMLStates.BEFORE_ATTRIBUTE_NAME_STATE] = self.handle_BEFORE_ATTRIBUTE_NAME_STATE
        # 8.2.4.35 Attribute name state
        transition_dict[HTMLStates.ATTRIBUTE_NAME_STATE] = self.handle_ATTRIBUTE_NAME_STATE
        # 8.2.4.36 After attribute name state
        transition_dict[HTMLStates.AFTER_ATTRIBUTE_NAME_STATE] = self.handle_AFTER_ATTRIBUTE_NAME_STATE
        # 8.2.4.37 Before attribute value state
        transition_dict[HTMLStates.BEFORE_ATTRIBUTE_VALUE_STATE] = self.handle_BEFORE_ATTRIBUTE_VALUE_STATE
        # 8.2.4.38 Attribute value (double-quoted) state
        transition_dict[
            HTMLStates.ATTRIBUTE_VALUE_DOUBLE_QUOTED_STATE] = self.handle_ATTRIBUTE_VALUE_DOUBLE_QUOTED_STATE
        # 8.2.4.39 Attribute value (single-quoted) state
        transition_dict[
            HTMLStates.ATTRIBUTE_VALUE_SINGLE_QUOTED_STATE] = self.handle_ATTRIBUTE_VALUE_SINGLE_QUOTED_STATE
        # 8.2.4.40 Attribute value (unquoted) state
        transition_dict[HTMLStates.ATTRIBUTE_VALUE_UNQUOTED_STATE] = self.handle_ATTRIBUTE_VALUE_UNQUOTED_STATE
        # 8.2.4.41 Character reference in attribute value state
        transition_dict[HTMLStates.CHARACTER_REFERENCE_IN_ATTRIBUTE_VALUE_STATE] = self.handle_CHAR_REF_IN_ATTR_VALUE
        # 8.2.4.42 After attribute value (quoted) state
        transition_dict[HTMLStates.AFTER_ATTRIBUTE_VALUE_QUOTED_STATE] = self.handle_AFTER_ATTRIBUTE_VALUE_QUOTED_STATE
        # 8.2.4.43 Self-closing start tag state
        transition_dict[HTMLStates.SELF_CLOSING_START_TAG_STATE] = self.handle_SELF_CLOSING_START_TAG_STATE
        # 8.2.4.44 Bogus comment state
        transition_dict[HTMLStates.BOGUS_COMMENT_STATE] = self.handle_BOGUS_COMMENT_STATE
        # 8.2.4.45 Markup declaration open state
        transition_dict[HTMLStates.MARKUP_DECLARATION_OPEN_STATE] = self.handle_MARKUP_DECLARATION_OPEN_STATE
        # 8.2.4.46 Comment start state
        transition_dict[HTMLStates.COMMENT_START_STATE] = self.handle_COMMENT_START_STATE
        # 8.2.4.47 Comment start dash state
        transition_dict[HTMLStates.COMMENT_START_DASH_STATE] = self.handle_COMMENT_START_DASH_STATE
        # 8.2.4.48 Comment state
        transition_dict[HTMLStates.COMMENT_STATE] = self.handle_COMMENT_STATE
        # 8.2.4.49 Comment end dash state
        transition_dict[HTMLStates.COMMENT_END_DASH_STATE] = self.handle_COMMENT_END_DASH_STATE
        # 8.2.4.50 Comment end state
        transition_dict[HTMLStates.COMMENT_END_STATE] = self.handle_COMMENT_END_STATE
        # 8.2.4.51 Comment end bang state
        transition_dict[HTMLStates.COMMENT_END_BANK_STATE] = self.handle_COMMENT_END_BANK_STATE
        # 8.2.4.52 DOCTYPE state
        transition_dict[HTMLStates.DOCTYPE_STATE] = self.handle_DOCTYPE_STATE
        # 8.2.4.53 Before DOCTYPE name state
        transition_dict[HTMLStates.BEFORE_DOCTYPE_NAME_STATE] = self.handle_BEFORE_DOCTYPE_NAME_STATE
        # 8.2.4.54 DOCTYPE name state
        transition_dict[HTMLStates.DOCTYPE_NAME_STATE] = self.handle_DOCTYPE_NAME_STATE
        # 8.2.4.55 After DOCTYPE name state
        transition_dict[HTMLStates.AFTER_DOCTYPE_NAME_STATE] = self.handle_AFTER_DOCTYPE_NAME_STATE
        # 8.2.4.56 After DOCTYPE public keyword state
        transition_dict[HTMLStates.AFTER_DOCTYPE_PUBLIC_KEYWORD_STATE] = self.handle_AFTER_DOCTYPE_PUBLIC_KEYWORD_STATE
        # 8.2.4.57 Before DOCTYPE public identifier state
        transition_dict[
            HTMLStates.BEFORE_DOCTYPE_PUBLIC_IDENTIFIER_STATE] = self.handle_BEFORE_DOCTYPE_PUBLIC_IDENTIFIER_STATE
        # 8.2.4.58 DOCTYPE public identifier (double-quoted) state
        transition_dict[
            HTMLStates.DOCTYPE_PUBLIC_IDENTIFIER_DOUBLE_QUOTED_STATE] = self.handle_DOCTYPE_PUBLIC_IDENTIFIER_DOUBLE_QUOTED_STATE
        # 8.2.4.59 DOCTYPE public identifier (single-quoted) state
        transition_dict[
            HTMLStates.DOCTYPE_PUBLIC_IDENTIFIER_SINGLE_QUOTED_STATE] = self.handle_DOCTYPE_PUBLIC_IDENTIFIER_SINGLE_QUOTED_STATE
        # 8.2.4.60 After DOCTYPE public identifier state
        transition_dict[
            HTMLStates.AFTER_DOCTPYE_PUBLIC_IDENTIFIER_STATE] = self.handle_AFTER_DOCTPYE_PUBLIC_IDENTIFIER_STATE
        # 8.2.4.61 Between DOCTYPE public and system identifiers state
        transition_dict[
            HTMLStates.BETWEEN_DOCTYPE_PUBLIC_AND_SYSTEM_IDENTIFIERS_STATE] = self.handle_BETWEEN_DOCTYPE_PUBLIC_AND_SYSTEM_IDENTIFIERS_STATE
        # 8.2.4.62 After DOCTYPE system keyword state
        transition_dict[HTMLStates.AFTER_DOCTYPE_SYSTEM_KEYWORD_STATE] = self.handle_AFTER_DOCTYPE_SYSTEM_KEYWORD_STATE
        # 8.2.4.63 Before DOCTYPE system identifier state
        transition_dict[
            HTMLStates.BEFORE_DOCTYPE_SYSTEM_IDENTIFIER_STATE] = self.handle_BEFORE_DOCTYPE_SYSTEM_IDENTIFIER_STATE
        # 8.2.4.64 DOCTYPE system identifier (double-quoted) state
        transition_dict[
            HTMLStates.DOCTPYE_SYSTEM_IDENTIFIER_DOUBLE_QUOTED_STATE] = self.handle_DOCTPYE_SYSTEM_IDENTIFIER_DOUBLE_QUOTED_STATE
        # 8.2.4.65 DOCTYPE system identifier (single-quoted) state
        transition_dict[
            HTMLStates.DOCTPYE_SYSTEM_IDENTIFIER_SINGLE_QUOTED_STATE] = self.handle_DOCTPYE_SYSTEM_IDENTIFIER_SINGLE_QUOTED_STATE
        # 8.2.4.66 After DOCTYPE system identifier state
        transition_dict[
            HTMLStates.AFTER_DOCTYPE_SYSTEM_IDENTIFIER_STATE] = self.handle_AFTER_DOCTYPE_SYSTEM_IDENTIFIER_STATE
        # 8.2.4.67 Bogus DOCTYPE state
        transition_dict[HTMLStates.BOGUS_DOCTYPE_STATE] = self.handle_BOGUS_DOCTYPE_STATE
        # 8.2.4.68 CDATA section state
        transition_dict[HTMLStates.CDATA_SECTION_STATE] = self.handle_CDATA_SECTION_STATE
        # 8.2.4.69 Tokenizing character references
        transition_dict[HTMLStates.TOKENIZING_CHAR_REF] = self.handle_TOKENIZING_CHAR_REF
        ########################## FINISHED TRANSITIONS ##############################
        self.transitions = transition_dict

    def handle_DATA_STATE(self):
        c = self.current_tag
        if 'name' in c and c['name'] == 'script' and c not in self.closed_tags:
            self.state = HTMLStates.SCRIPT_DATA_STATE
        else:
            tos = self.consumeNextChar()
            if tos == "&":
                self.state = HTMLStates.CHAR_REF_DATA_STATE
            elif tos == "<":
                self.buffered_text = ""
                self.state = HTMLStates.TAG_OPEN_STATE
            else:
                # NOOP, no stat change
                pass

    def handle_CHAR_REF_IN_DATA_STATE(self):
        self.additional_allowed_char = ''
        self.consumeCharRef()
        self.state = HTMLStates.DATA_STATE

    def handle_RC_DATA_STATE(self):
        tos = self.consumeNextChar()
        if tos == "&":
            self.state = HTMLStates.CHAR_REF_IN_RCDATA_STATE
        elif tos == "<":
            self.state = HTMLStates.RCDATA_LESS_THAN_SIGN_STATE
        else:
            # NOOP, no stat change
            pass

    def handle_CHAR_REF_IN_RCDATA_STATE(self):
        self.consumeCharRef()
        self.state = HTMLStates.RCDATA_STATE

    def handle_RAWTEXT_STATE(self):
        tos = self.consumeNextChar()

        if tos == "<":
            self.state = HTMLStates.RAWTEXT_LESS_THAN_SIGN_STATE
        else:
            # NOOP, no stat change
            pass

    def handle_SCRIPT_DATA_STATE(self):
        tos = self.consumeNextChar()
        if tos == "<":
            self.state = HTMLStates.SCRIPT_DATA_LESS_THAN_SIGN_STATE
        else:
            self.current_tag['data'] += tos
            # NOOP, no stat change
            pass

    def handle_PLAINTEXT_STATE(self):
        tos = self.consumeNextChar()
        # Yes no way to switch state, thus we are trapped here

    def handle_TAG_OPEN_STATE(self):
        self._in_opening_tag = True
        tos = self.consumeNextChar()
        if tos == "!":
            self.state = HTMLStates.MARKUP_DECLARATION_OPEN_STATE
        elif tos == "/":
            self.state = HTMLStates.END_TAG_OPEN_STATE
        elif tos in string.ascii_letters:
            self.state = HTMLStates.TAG_NAME_STATE
            self.buffered_text += tos.lower()
        elif tos == "?":
            self.state = HTMLStates.BOGUS_COMMENT_STATE
        else:
            self.input = tos + self.input
            self.state = HTMLStates.DATA_STATE

    def handle_END_TAG_OPEN_STATE(self):
        self._in_opening_tag = False
        tos = self.consumeNextChar()
        if tos in string.ascii_letters:
            self.state = HTMLStates.TAG_NAME_STATE
            self.buffered_text += tos.lower()
        elif tos == ">":
            self.state = HTMLStates.DATA_STATE
        else:
            self.state = HTMLStates.BOGUS_COMMENT_STATE

    def handle_TAG_NAME_STATE(self):
        tos = self.consumeNextChar()
        if tos in [" ", "\t", "\n", "\x0c"]:
            self.state = HTMLStates.BEFORE_ATTRIBUTE_NAME_STATE
            if self._in_opening_tag:
                self.current_tag = {
                    'name': self.buffered_text,
                    'attributes': [],
                    'data': ''
                }
                self.opened_tags.append(self.current_tag)
            else:
                # Done by next State
                pass
        elif tos == "/":
            self.state = HTMLStates.SELF_CLOSING_START_TAG_STATE
            if self._in_opening_tag:
                self.current_tag = {
                    'name': self.buffered_text,
                    'attributes': [],
                    'data': ''
                }
                self.opened_tags.append(self.current_tag)
            else:
                # Done by next State
                pass
        elif tos == ">":
            self.state = HTMLStates.DATA_STATE
            if self._in_opening_tag:
                self.current_tag = {
                    'name': self.buffered_text,
                    'attributes': [],
                    'data': ''
                }
                self.opened_tags.append(self.current_tag)
            else:
                tag = find_tag_to_close(self.buffered_text, self.opened_tags)
                if tag is not None:
                    self.opened_tags.remove(tag)
                    self.closed_tags.append(tag)
        else:
            self.buffered_text += tos.lower()

    def handle_RCDATA_LESS_THAN_SIGN_STATE(self):
        tos = self.consumeNextChar()
        if tos == "/":
            self.buffered_text = ""
            self.state = HTMLStates.RCDATA_END_TAG_OPEN_STATE
        else:
            self.input = tos + self.input
            self.state = HTMLStates.RCDATA_STATE

    def handle_RCDATA_END_TAG_OPEN_STATE(self):
        tos = self.consumeNextChar()
        if tos in string.ascii_letters:
            self.buffered_text = tos.lower()
            self.state = HTMLStates.RCDATA_END_TAG_NAME_STATE
        else:
            self.input = tos + self.input

    def handle_RCDATA_END_TAG_NAME_STATE(self):
        tos = self.consumeNextChar()

        if tos in [" ", "\t", "\n", "\x0c"]:
            self.state = HTMLStates.BEFORE_ATTRIBUTE_NAME_STATE
        elif tos == "/":
            if "[CDATA[".lower() in self.buffered_text.lower():
                self.state = HTMLStates.SELF_CLOSING_START_TAG_STATE
            else:
                self.input = tos + self.input
                self.state = HTMLStates.RCDATA_STATE
        elif tos == ">":
            if "[CDATA[".lower() in self.buffered_text.lower():
                self.state = HTMLStates.DATA_STATE
                self.opened_tags.remove(self.current_tag)
                self.closed_tags.append(self.current_tag)
            else:
                self.input = tos + self.input
                self.state = HTMLStates.RCDATA_STATE
        elif tos in string.ascii_letters:
            self.buffered_text += tos.lower()
        else:
            self.input = tos + self.input
            self.state = HTMLStates.RCDATA_STATE

    def handle_RAWTEXT_LESS_THAN_SIGN_STATE(self):
        tos = self.consumeNextChar()
        if tos == "/":
            self.buffered_text = ""
            self.state = HTMLStates.RAWTEXT_END_TAG_OPEN_STATE
        else:
            self.input = tos + self.input
            self.state = HTMLStates.RAWTEXT_STATE

    def handle_RAWTEXT_END_TAG_OPEN_STATE(self):
        tos = self.consumeNextChar()
        if tos in string.ascii_letters:
            self.buffered_text = tos.lower()
            self.state = HTMLStates.RAWTAG_END_TAG_NAME_STATE
        else:
            self.input = tos + self.input
            self.state = HTMLStates.RAWTEXT_STATE

    def handle_RAWTAG_END_TAG_NAME_STATE(self):
        tos = self.consumeNextChar()
        if tos in [" ", "\t", "\n", "\x0c"]:
            self.state = HTMLStates.BEFORE_ATTRIBUTE_NAME_STATE
        elif tos == "/":
            if self.buffered_text == "plaintext":
                self.state = HTMLStates.SELF_CLOSING_START_TAG_STATE
            else:
                self.input = tos + self.input
                self.state = HTMLStates.RAWTEXT_STATE
        elif tos == ">":
            if self.buffered_text == "plaintext":
                self.state = HTMLStates.DATA_STATE
                self.opened_tags.remove(self.current_tag)
                self.closed_tags.append(self.current_tag)
            else:
                self.input = tos + self.input
                self.state = HTMLStates.RAWTEXT_STATE
        elif tos in string.ascii_letters:
            self.buffered_text += tos.lower()
        else:
            self.input = tos + self.input
            self.state = HTMLStates.RAWTEXT_STATE

    def handle_SCRIPT_DATA_LESS_THAN_SIGN_STATE(self):
        tos = self.consumeNextChar()
        if tos == "/":
            self.buffered_text = ""
            self.state = HTMLStates.SCRIPT_DATA_END_TAG_OPEN_STATE
        elif tos == "!":
            self.state = HTMLStates.SCRIPT_DATA_ESCAPE_START_STATE
        else:
            self.input = tos + self.input
            self.state = HTMLStates.SCRIPT_DATA_STATE

    def handle_SCRIPT_DATA_END_TAG_OPEN_STATE(self):
        tos = self.consumeNextChar()
        if tos in string.ascii_letters:
            self.buffered_text = tos
            self.state = HTMLStates.SCRIPT_DATA_END_TAG_NAME_STATE
        else:
            self.input = tos + self.input
            self.state = HTMLStates.SCRIPT_DATA_STATE

    def handle_SCRIPT_DATA_END_TAG_NAME_STATE(self):
        tos = self.consumeNextChar()
        if tos in [" ", "\t", "\n", "\x0c"]:
            self.state = HTMLStates.BEFORE_ATTRIBUTE_NAME_STATE
        elif tos == "/":
            if self.buffered_text == 'script':
                self.state = HTMLStates.SELF_CLOSING_START_TAG_STATE
            else:
                self.input = tos + self.input
                self.state = HTMLStates.SCRIPT_DATA_STATE
        elif tos == ">":
            if self.buffered_text == 'script':
                self.state = HTMLStates.DATA_STATE
                self.opened_tags.remove(self.current_tag)
                self.closed_tags.append(self.current_tag)
            else:
                self.input = tos + self.input
                self.state = HTMLStates.SCRIPT_DATA_STATE
        elif tos in string.ascii_letters:
            self.buffered_text += tos.lower()
        else:
            self.input = tos + self.input
            self.state = HTMLStates.SCRIPT_DATA_STATE

    def handle_SCRIPT_DATA_ESCAPE_START_STATE(self):
        tos = self.consumeNextChar()
        if tos == "-":
            self.state = HTMLStates.SCRIPT_DATA_ESCAPE_START_DASH_STATE
        else:
            self.input = tos + self.input
            self.state = HTMLStates.SCRIPT_DATA_STATE

    def handle_SCRIPT_DATA_ESCAPE_START_DASH_STATE(self):
        tos = self.consumeNextChar()
        if tos == "-":
            self.state = HTMLStates.SCRIPT_DATA_ESCAPED_DASH_DASH_STATE
        else:
            self.input = tos + self.input
            self.state = HTMLStates.SCRIPT_DATA_STATE

    def handle_SCRIPT_DATA_ESCAPED_STATE(self):
        tos = self.consumeNextChar()
        if tos == "-":
            self.state = HTMLStates.SCRIPT_DATA_ESCAPED_DASH_STATE
        elif tos == "<":
            self.state = HTMLStates.SCRIPT_DATA_ESCAPED_LESS_THAN_SIGN_STATE

    def handle_SCRIPT_DATA_ESCAPED_DASH_STATE(self):
        tos = self.consumeNextChar()
        if tos == "-":
            self.state = HTMLStates.SCRIPT_DATA_ESCAPED_DASH_DASH_STATE
        elif tos == "<":
            self.state = HTMLStates.SCRIPT_DATA_ESCAPED_LESS_THAN_SIGN_STATE
        elif tos == "\0":
            self.state = HTMLStates.SCRIPT_DATA_ESCAPED_STATE
        else:
            self.state = HTMLStates.SCRIPT_DATA_ESCAPED_STATE

    def handle_SCRIPT_DATA_ESCAPED_DASH_DASH_STATE(self):
        tos = self.consumeNextChar()
        if tos == "-":
            pass
        elif tos == "<":
            self.state = HTMLStates.SCRIPT_DATA_ESCAPED_LESS_THAN_SIGN_STATE
        elif tos == "\0":
            self.state = HTMLStates.SCRIPT_DATA_ESCAPED_STATE
        elif tos == ">":
            self.state = HTMLStates.SCRIPT_DATA_STATE
        else:
            self.state = HTMLStates.SCRIPT_DATA_ESCAPED_STATE

    def handle_SCRIPT_DATA_ESCAPED_LESS_THAN_SIGN_STATE(self):
        tos = self.consumeNextChar()
        if tos == "/":
            self.buffered_text = ""
            self.state = HTMLStates.SCRIPT_DATA_ESCAPED_END_TAG_OPEN_STATE
        elif tos in string.ascii_letters:
            self.buffered_text = tos.lower()
            self.state = HTMLStates.SCRIPT_DATA_DOUBLE_ESCAPE_START_STATE
        else:
            self.input = tos + self.input
            self.state = HTMLStates.SCRIPT_DATA_ESCAPED_STATE

    def handle_SCRIPT_DATA_ESCAPED_END_TAG_OPEN_STATE(self):
        tos = self.consumeNextChar()
        if tos in string.ascii_letters:
            self.buffered_text = tos
            self.state = HTMLStates.SCRIPT_DATA_ESCAPED_END_TAG_NAME_STATE
        else:
            self.input = tos + self.input
            self.state = HTMLStates.SCRIPT_DATA_ESCAPED_STATE

    def handle_SCRIPT_DATA_ESCAPED_END_TAG_NAME_STATE(self):
        tos = self.consumeNextChar()
        if tos in [" ", "\t", "\n", "\x0c"]:
            self.state = HTMLStates.BEFORE_ATTRIBUTE_NAME_STATE
        elif tos == "/":
            if self.buffered_text == 'script':
                self.state = HTMLStates.SELF_CLOSING_START_TAG_STATE
            else:
                self.input = tos + self.input
                self.state = HTMLStates.SCRIPT_DATA_ESCAPED_STATE
        elif tos == ">":
            if self.buffered_text == 'script':
                self.state = HTMLStates.DATA_STATE
                self.opened_tags.remove(self.current_tag)
                self.closed_tags.append(self.current_tag)
            else:
                self.input = tos + self.input
                self.state = HTMLStates.SCRIPT_DATA_ESCAPED_STATE
        elif tos in string.ascii_letters:
            self.buffered_text += tos.lower()
        else:
            self.input = tos + self.input
            self.state = HTMLStates.SCRIPT_DATA_ESCAPED_STATE

    def handle_SCRIPT_DATA_DOUBLE_ESCAPE_START_STATE(self):
        tos = self.consumeNextChar()
        if tos in [" ", "\t", "\n", "\x0c", "/", ">"]:
            if self.buffered_text == "string":
                self.state = HTMLStates.SCRIPT_DATA_DOUBLE_ESCAPED_STATE
            else:
                self.state = HTMLStates.SCRIPT_DATA_ESCAPED_STATE
        elif tos in string.ascii_letters:
            self.buffered_text += tos.lower()
        else:
            self.input = tos + self.input
            self.state = HTMLStates.SCRIPT_DATA_ESCAPED_STATE

    def handle_SCRIPT_DATA_DOUBLE_ESCAPED_STATE(self):
        tos = self.consumeNextChar()
        if tos == "-":
            self.state = HTMLStates.SCRIPT_DATA_DOUBLE_ESCAPED_DASH_STATE
        elif tos == "<":
            self.state = HTMLStates.SCRIPT_DATA_DOUBLE_ESCAPED_LESS_THAN_SIGN_STATE
        elif tos == "\0":
            pass
        elif tos == ">":
            self.state = HTMLStates.SCRIPT_DATA_STATE
        else:
            self.state = HTMLStates.SCRIPT_DATA_ESCAPED_STATE

    def handle_SCRIPT_DATA_DOUBLE_ESCAPED_DASH_STATE(self):
        tos = self.consumeNextChar()
        if tos == "-":
            self.state = HTMLStates.SCRIPT_DATA_DOUBLE_ESCAPED_DASH_DASH_STATE
        elif tos == "<":
            self.state = HTMLStates.SCRIPT_DATA_DOUBLE_ESCAPED_LESS_THAN_SIGN_STATE
        elif tos == "\0":
            pass
        else:
            self.state = HTMLStates.SCRIPT_DATA_DOUBLE_ESCAPED_STATE

    def handle_SCRIPT_DATA_DOUBLE_ESCAPED_DASH_DASH_STATE(self):
        tos = self.consumeNextChar()
        if tos == "-":
            pass
        elif tos == "<":
            self.state = HTMLStates.SCRIPT_DATA_DOUBLE_ESCAPED_LESS_THAN_SIGN_STATE
        elif tos == ">":
            self.state = HTMLStates.SCRIPT_DATA_STATE
        elif tos == "\0":
            self.state = HTMLStates.SCRIPT_DATA_DOUBLE_ESCAPED_STATE
        else:
            self.state = HTMLStates.SCRIPT_DATA_DOUBLE_ESCAPED_STATE

    def handle_SCRIPT_DATA_DOUBLE_ESCAPED_LESS_THAN_SIGN_STATE(self):
        tos = self.consumeNextChar()
        if tos == "/":
            self.buffered_text = ''
            self.state = HTMLStates.SCRIPT_DATA_DOUBLE_ESCAPE_END_STATE
        else:
            self.input = tos + self.input
            self.state = HTMLStates.SCRIPT_DATA_DOUBLE_ESCAPED_STATE

    def handle_SCRIPT_DATA_DOUBLE_ESCAPE_END_STATE(self):
        tos = self.consumeNextChar()
        if tos in [" ", "\t", "\n", "\x0c", "/", ">"]:
            if self.buffered_text == "script":
                self.state = HTMLStates.SCRIPT_DATA_ESCAPED_STATE
            else:
                self.state = HTMLStates.SCRIPT_DATA_DOUBLE_ESCAPED_STATE
        elif tos in string.ascii_letters:
            self.buffered_text += tos.lower()
        else:
            self.state = HTMLStates.SCRIPT_DATA_DOUBLE_ESCAPED_STATE

    def handle_BEFORE_ATTRIBUTE_NAME_STATE(self):
        tos = self.consumeNextChar()
        while tos in [" ", "\t", "\n", "\x0c"]:
            tos = self.consumeNextChar()
        if tos == "/":
            self.state = HTMLStates.SELF_CLOSING_START_TAG_STATE
        elif tos == ">":
            self.state = HTMLStates.DATA_STATE
        elif tos in string.ascii_letters:
            self.current_tag['attributes'].append(
                {
                    'name': tos.lower(),
                    'value': ''
                }
            )
            self.state = HTMLStates.ATTRIBUTE_NAME_STATE
        elif tos == "\0":
            self.current_tag['attributes'].append(
                {
                    'name': u'\ufffd',
                    'value': ''
                }
            )
            self.state = HTMLStates.ATTRIBUTE_NAME_STATE
        else:
            self.current_tag['attributes'].append(
                {
                    'name': tos,
                    'value': ''
                }
            )
            self.state = HTMLStates.ATTRIBUTE_NAME_STATE

    def handle_ATTRIBUTE_NAME_STATE(self):
        tos = self.consumeNextChar()
        if tos in [" ", "\t", "\n", "\x0c"]:
            self.state = HTMLStates.AFTER_ATTRIBUTE_NAME_STATE
        elif tos == "/":
            self.state = HTMLStates.SELF_CLOSING_START_TAG_STATE
        elif tos == "=":
            self.state = HTMLStates.BEFORE_ATTRIBUTE_VALUE_STATE
        elif tos == ">":
            tag = find_tag_to_close(self.buffered_text, self.opened_tags)
            if tag is not None:
                self.opened_tags.remove(tag)
                self.closed_tags.append(tag)
            self.state = HTMLStates.DATA_STATE
        elif tos in string.ascii_letters:
            self.current_tag['attributes'][-1]['name'] += tos.lower()
        elif tos == "\0":
            self.current_tag['attributes'][-1]['name'] += u'\ufffd'
        else:
            self.current_tag['attributes'][-1]['name'] += tos

    def handle_AFTER_ATTRIBUTE_NAME_STATE(self):
        tos = self.consumeNextChar()
        while tos in [" ", "\t", "\n", "\x0c"]:
            tos = self.consumeNextChar()
        if tos == "/":
            self.state = HTMLStates.SELF_CLOSING_START_TAG_STATE
        elif tos == "=":
            self.state = HTMLStates.BEFORE_ATTRIBUTE_VALUE_STATE
        elif tos == ">":
            tag = find_tag_to_close(self.buffered_text, self.opened_tags)
            if tag is not None:
                self.opened_tags.remove(tag)
                self.closed_tags.append(tag)
            self.state = HTMLStates.DATA_STATE
        elif tos in string.ascii_letters:
            self.current_tag['attributes'][-1]['name'] += tos.lower()
        elif tos == "\0":
            self.current_tag['attributes'][-1]['name'] += u'\ufffd'
        else:
            self.current_tag['attributes'].append(
                {
                    'name': tos,
                    'value': ''
                }
            )
            self.state = HTMLStates.ATTRIBUTE_NAME_STATE

    def handle_BEFORE_ATTRIBUTE_VALUE_STATE(self):
        tos = self.consumeNextChar()
        while tos in [" ", "\t", "\n", "\x0c"]:
            tos = self.consumeNextChar()
        if tos == "\"":
            self.current_tag['attributes'][-1]['kind'] = 'double'
            self.state = HTMLStates.ATTRIBUTE_VALUE_DOUBLE_QUOTED_STATE
        elif tos == "&":
            self.input = tos + self.input
            self.current_tag['attributes'][-1]['kind'] = 'unquoted'
            self.state = HTMLStates.ATTRIBUTE_VALUE_UNQUOTED_STATE
        elif tos == "'":
            self.current_tag['attributes'][-1]['kind'] = 'single'
            self.state = HTMLStates.ATTRIBUTE_VALUE_SINGLE_QUOTED_STATE
        elif tos == "\0":
            self.current_tag['attributes'][-1]['value'] += u'\ufffd'
        else:
            self.current_tag['attributes'][-1]['kind'] = 'unquoted'
            self.current_tag['attributes'][-1]['value'] += tos
            self.state = HTMLStates.ATTRIBUTE_VALUE_UNQUOTED_STATE

    def handle_ATTRIBUTE_VALUE_DOUBLE_QUOTED_STATE(self):
        tos = self.consumeNextChar()
        if tos == "\"":
            self.state = HTMLStates.AFTER_ATTRIBUTE_VALUE_QUOTED_STATE
        elif tos == "&":
            self.additional_allowed_char = "\""
            self.state = HTMLStates.CHARACTER_REFERENCE_IN_ATTRIBUTE_VALUE_STATE
        elif tos == "\0":
            self.current_tag['attributes'][-1]['value'] += u'\ufffd'
        else:
            self.current_tag['attributes'][-1]['value'] += tos

    def handle_ATTRIBUTE_VALUE_SINGLE_QUOTED_STATE(self):
        tos = self.consumeNextChar()
        if tos == "'":
            self.state = HTMLStates.AFTER_ATTRIBUTE_VALUE_QUOTED_STATE
        elif tos == "&":
            self.additional_allowed_char = "'"
            self.state = HTMLStates.CHARACTER_REFERENCE_IN_ATTRIBUTE_VALUE_STATE
        else:
            self.current_tag['attributes'][-1]['value'] += tos

    def handle_ATTRIBUTE_VALUE_UNQUOTED_STATE(self):
        tos = self.consumeNextChar()
        if tos in [" ", "\t", "\n", "\x0c"]:
            self.state = HTMLStates.BEFORE_ATTRIBUTE_NAME_STATE
        elif tos == "&":
            self.additional_allowed_char = ">"
            self.state = HTMLStates.CHARACTER_REFERENCE_IN_ATTRIBUTE_VALUE_STATE
        elif tos == ">":
            self.state = HTMLStates.DATA_STATE
        elif tos == "\0":
            self.current_tag['attributes'][-1]['value'] += u'\ufffd'
        else:
            self.current_tag['attributes'][-1]['value'] += tos

    def handle_CHAR_REF_IN_ATTR_VALUE(self):
        char_ref = self.consumeCharRef()
        if char_ref == "":
            self.current_tag['attributes'][-1]['value'] += '&'
        else:
            self.current_tag['attributes'][-1]['value'] += char_ref
        if 'kind' in self.current_tag['attributes'][-1]:
            if self.current_tag['attributes'][-1]['kind'] == 'unquoted':
                self.state = HTMLStates.ATTRIBUTE_VALUE_UNQUOTED_STATE
            elif self.current_tag['attributes'][-1]['kind'] == 'double':
                self.state = HTMLStates.ATTRIBUTE_VALUE_DOUBLE_QUOTED_STATE
            elif self.current_tag['attributes'][-1]['kind'] == 'single':
                self.state = HTMLStates.ATTRIBUTE_VALUE_SINGLE_QUOTED_STATE
        else:
            pass

    def handle_AFTER_ATTRIBUTE_VALUE_QUOTED_STATE(self):
        tos = self.consumeNextChar()
        if tos in [" ", "\t", "\n", "\x0c"]:
            self.state = HTMLStates.BEFORE_ATTRIBUTE_NAME_STATE
        elif tos == "/":
            self.state = HTMLStates.SELF_CLOSING_START_TAG_STATE
        elif tos == ">":
            self.state = HTMLStates.DATA_STATE
        else:
            self.input = tos + self.input
            self.state = HTMLStates.BEFORE_ATTRIBUTE_NAME_STATE

    def handle_SELF_CLOSING_START_TAG_STATE(self):
        tos = self.consumeNextChar()
        if tos == ">":
            self.current_tag['is_self_closing_tag'] = True
            tag = find_tag_to_close(self.buffered_text, self.opened_tags)
            if tag is not None:
                self.opened_tags.remove(tag)
                self.closed_tags.append(tag)
            self.state = HTMLStates.DATA_STATE
        else:
            self.input = tos + self.input
            self.state = HTMLStates.BEFORE_ATTRIBUTE_NAME_STATE

    def handle_BOGUS_COMMENT_STATE(self):
        tos = self.consumeNextChar()
        while tos != ">":
            if len(self.input) < 1:
                return
            tos = self.consumeNextChar()
        self.state = HTMLStates.DATA_STATE

    def handle_MARKUP_DECLARATION_OPEN_STATE(self):
        if self.input[:2] == "--":
            self.consumeNextChar()
            self.consumeNextChar()
            self.current_tag = {
                'name': 'comment',
                'attributes': [],
                'data': ''
            }
            self.opened_tags.append(self.current_tag)
            self.state = HTMLStates.COMMENT_START_STATE
        elif self.input[:7].upper() == "DOCTYPE":
            for i in range(7):
                self.consumeNextChar()
            self.state = HTMLStates.DOCTYPE_STATE
        elif self.input[:7].upper() == "[CDATA[":
            for i in range(7):
                self.consumeNextChar()
            self.state = HTMLStates.CDATA_SECTION_STATE
        else:
            self.state = HTMLStates.BOGUS_COMMENT_STATE

    def handle_COMMENT_START_STATE(self):
        tos = self.consumeNextChar()
        if tos == "-":
            self.state = HTMLStates.COMMENT_START_DASH_STATE
        elif tos == "\0":
            self.current_tag['data'] += u'\ufffd'
            self.state = HTMLStates.COMMENT_STATE
        else:
            self.current_tag['data'] += tos
            self.state = HTMLStates.COMMENT_STATE

    def handle_COMMENT_START_DASH_STATE(self):
        tos = self.consumeNextChar()
        if tos == "-":
            self.state = HTMLStates.COMMENT_END_STATE
        elif tos == "\0":
            self.current_tag['data'] += '-' + u'\ufffd'
            self.state = HTMLStates.COMMENT_STATE
        elif tos == ">":
            self.state = HTMLStates.DATA_STATE
        else:
            self.current_tag['data'] += '-' + tos
            self.state = HTMLStates.COMMENT_STATE

    def handle_COMMENT_STATE(self):
        tos = self.consumeNextChar()
        if tos == "-":
            self.state = HTMLStates.COMMENT_END_DASH_STATE
        elif tos == "\0":
            self.current_tag['data'] += u'\ufffd'
        else:
            self.current_tag['data'] += tos

    def handle_COMMENT_END_DASH_STATE(self):
        tos = self.consumeNextChar()
        if tos == "-":
            self.state = HTMLStates.COMMENT_END_STATE
        elif tos == "\0":
            self.current_tag['data'] += '-' + u'\ufffd'
        else:
            self.current_tag['data'] += '-' + tos
            self.state = HTMLStates.COMMENT_STATE

    def handle_COMMENT_END_STATE(self):
        tos = self.consumeNextChar()
        if tos == ">":
            self.state = HTMLStates.DATA_STATE
        elif tos == "\0":
            self.current_tag['data'] += '-' + u'\ufffd'
            self.state = HTMLStates.COMMENT_STATE
        elif tos == "!":
            self.state = HTMLStates.COMMENT_END_BANK_STATE
        elif tos == "-":
            self.current_tag['data'] += '-'
        else:
            self.current_tag['data'] += '-' + tos
            self.state = HTMLStates.COMMENT_STATE

    def handle_COMMENT_END_BANK_STATE(self):
        tos = self.consumeNextChar()
        if tos == "-":
            self.current_tag['data'] += '--!'
            self.state = HTMLStates.COMMENT_END_DASH_STATE
        elif tos == ">":
            self.state = HTMLStates.DATA_STATE
        elif tos == "\0":
            self.current_tag['data'] += '--!' + u'\ufffd'
            self.state = HTMLStates.COMMENT_STATE
        else:
            self.current_tag['data'] += '--!' + tos
            self.state = HTMLStates.COMMENT_STATE

    def handle_DOCTYPE_STATE(self):
        tos = self.consumeNextChar()
        if tos in [" ", "\t", "\n", "\x0c"]:
            self.state = HTMLStates.BEFORE_DOCTYPE_NAME_STATE
        else:
            self.input = tos + self.input
            self.state = HTMLStates.BEFORE_DOCTYPE_NAME_STATE

    def handle_BEFORE_DOCTYPE_NAME_STATE(self):
        tos = self.consumeNextChar()
        while tos in [" ", "\t", "\n", "\x0c"]:
            tos = self.consumeNextChar()
        if tos in string.ascii_letters:
            self.state = HTMLStates.DOCTYPE_NAME_STATE
        elif tos == "\0":
            self.state = HTMLStates.DOCTYPE_NAME_STATE
        elif tos == ">":
            self.state = HTMLStates.DATA_STATE
        else:
            self.state = HTMLStates.DOCTYPE_NAME_STATE

    def handle_DOCTYPE_NAME_STATE(self):
        tos = self.consumeNextChar()
        if tos in [" ", "\t", "\n", "\x0c"]:
            self.state = HTMLStates.AFTER_DOCTYPE_NAME_STATE
        elif tos == ">":
            self.state = HTMLStates.DATA_STATE
        else:
            # NOOP because DOCTYPE does not care:
            pass

    def handle_AFTER_DOCTYPE_NAME_STATE(self):
        tos = self.consumeNextChar()
        while tos in [" ", "\t", "\n", "\x0c"]:
            tos = self.consumeNextChar()
        if tos == ">":
            self.state = HTMLStates.DATA_STATE
        elif tos == "P" and "UBLIC" == self.input[:5].upper():
            for i in range(5):
                self.consumeNextChar()
            self.state = HTMLStates.AFTER_DOCTYPE_PUBLIC_KEYWORD_STATE
        elif tos == "S" and "YSTEM" == self.input[:5].upper():
            for i in range(5):
                self.consumeNextChar()
            self.state = HTMLStates.AFTER_DOCTYPE_SYSTEM_KEYWORD_STATE
        else:
            self.state = HTMLStates.BOGUS_DOCTYPE_STATE

    def handle_AFTER_DOCTYPE_PUBLIC_KEYWORD_STATE(self):
        tos = self.consumeNextChar()
        if tos in [" ", "\t", "\n", "\x0c"]:
            self.state = HTMLStates.BEFORE_DOCTYPE_PUBLIC_IDENTIFIER_STATE
        elif tos == "\"":
            self.state = HTMLStates.DOCTYPE_PUBLIC_IDENTIFIER_DOUBLE_QUOTED_STATE
        elif tos == "'":
            self.state = HTMLStates.DOCTYPE_PUBLIC_IDENTIFIER_SINGLE_QUOTED_STATE
        elif tos == ">":
            self.state = HTMLStates.DATA_STATE
        else:
            self.state = HTMLStates.BOGUS_DOCTYPE_STATE

    def handle_BEFORE_DOCTYPE_PUBLIC_IDENTIFIER_STATE(self):
        tos = self.consumeNextChar()
        while tos in [" ", "\t", "\n", "\x0c"]:
            tos = self.consumeNextChar()
        if tos == "\"":
            self.state = HTMLStates.DOCTYPE_PUBLIC_IDENTIFIER_DOUBLE_QUOTED_STATE
        elif tos == "'":
            self.state = HTMLStates.DOCTYPE_PUBLIC_IDENTIFIER_SINGLE_QUOTED_STATE
        elif tos == ">":
            self.state = HTMLStates.DATA_STATE
        else:
            self.state = HTMLStates.BOGUS_DOCTYPE_STATE

    def handle_DOCTYPE_PUBLIC_IDENTIFIER_DOUBLE_QUOTED_STATE(self):
        tos = self.consumeNextChar()
        if tos == "\"":
            self.state = HTMLStates.AFTER_DOCTPYE_PUBLIC_IDENTIFIER_STATE
        elif tos == ">":
            self.state = HTMLStates.DATA_STATE
        else:
            # NOOP because DOCTYPE does not care:
            pass

    def handle_DOCTYPE_PUBLIC_IDENTIFIER_SINGLE_QUOTED_STATE(self):
        tos = self.consumeNextChar()
        if tos == "'":
            self.state = HTMLStates.AFTER_DOCTPYE_PUBLIC_IDENTIFIER_STATE
        elif tos == ">":
            self.state = HTMLStates.DATA_STATE
        else:
            # NOOP because DOCTYPE does not care:
            pass

    def handle_AFTER_DOCTPYE_PUBLIC_IDENTIFIER_STATE(self):
        tos = self.consumeNextChar()
        if tos in [" ", "\t", "\n", "\x0c"]:
            self.state = HTMLStates.BETWEEN_DOCTYPE_PUBLIC_AND_SYSTEM_IDENTIFIERS_STATE
        elif tos == "\"":
            self.state = HTMLStates.DOCTPYE_SYSTEM_IDENTIFIER_DOUBLE_QUOTED_STATE
        elif tos == "'":
            self.state = HTMLStates.DOCTPYE_SYSTEM_IDENTIFIER_SINGLE_QUOTED_STATE
        elif tos == ">":
            self.state = HTMLStates.DATA_STATE
        else:
            self.state = HTMLStates.BOGUS_DOCTYPE_STATE

    def handle_BETWEEN_DOCTYPE_PUBLIC_AND_SYSTEM_IDENTIFIERS_STATE(self):
        tos = self.consumeNextChar()
        while tos in [" ", "\t", "\n", "\x0c"]:
            tos = self.consumeNextChar()
        if tos == "\"":
            self.state = HTMLStates.DOCTPYE_SYSTEM_IDENTIFIER_DOUBLE_QUOTED_STATE
        elif tos == "'":
            self.state = HTMLStates.DOCTPYE_SYSTEM_IDENTIFIER_SINGLE_QUOTED_STATE
        elif tos == ">":
            self.state = HTMLStates.DATA_STATE
        else:
            self.state = HTMLStates.BOGUS_DOCTYPE_STATE

    def handle_AFTER_DOCTYPE_SYSTEM_KEYWORD_STATE(self):
        tos = self.consumeNextChar()
        if tos in [" ", "\t", "\n", "\x0c"]:
            self.state = HTMLStates.BEFORE_DOCTYPE_SYSTEM_IDENTIFIER_STATE
        elif tos == "\"":
            self.state = HTMLStates.DOCTPYE_SYSTEM_IDENTIFIER_DOUBLE_QUOTED_STATE
        elif tos == "'":
            self.state = HTMLStates.DOCTPYE_SYSTEM_IDENTIFIER_SINGLE_QUOTED_STATE
        elif tos == ">":
            self.state = HTMLStates.DATA_STATE
        else:
            self.state = HTMLStates.BOGUS_DOCTYPE_STATE

    def handle_BEFORE_DOCTYPE_SYSTEM_IDENTIFIER_STATE(self):
        tos = self.consumeNextChar()
        while tos in [" ", "\t", "\n", "\x0c"]:
            tos = self.consumeNextChar()
        if tos == "\"":
            self.state = HTMLStates.DOCTPYE_SYSTEM_IDENTIFIER_DOUBLE_QUOTED_STATE
        elif tos == "'":
            self.state = HTMLStates.DOCTPYE_SYSTEM_IDENTIFIER_SINGLE_QUOTED_STATE
        elif tos == ">":
            self.state = HTMLStates.DATA_STATE
        else:
            self.state = HTMLStates.BOGUS_DOCTYPE_STATE

    def handle_DOCTPYE_SYSTEM_IDENTIFIER_DOUBLE_QUOTED_STATE(self):
        tos = self.consumeNextChar()
        if tos == "\"":
            self.state = HTMLStates.AFTER_DOCTYPE_SYSTEM_IDENTIFIER_STATE
        elif tos == ">":
            self.state = HTMLStates.DATA_STATE
        else:
            self.state = HTMLStates.BOGUS_DOCTYPE_STATE

    def handle_DOCTPYE_SYSTEM_IDENTIFIER_SINGLE_QUOTED_STATE(self):
        tos = self.consumeNextChar()
        if tos == "'":
            self.state = HTMLStates.AFTER_DOCTYPE_SYSTEM_IDENTIFIER_STATE
        elif tos == ">":
            self.state = HTMLStates.DATA_STATE
        else:
            self.state = HTMLStates.BOGUS_DOCTYPE_STATE

    def handle_AFTER_DOCTYPE_SYSTEM_IDENTIFIER_STATE(self):
        tos = self.consumeNextChar()
        while tos in [" ", "\t", "\n", "\x0c"]:
            tos = self.consumeNextChar()
        if tos == ">":
            self.state = HTMLStates.DATA_STATE
        else:
            self.state = HTMLStates.BOGUS_DOCTYPE_STATE

    def handle_BOGUS_DOCTYPE_STATE(self):
        tos = self.consumeNextChar()
        while tos != ">":
            tos = self.consumeNextChar()
        self.state = HTMLStates.DATA_STATE

    def handle_CDATA_SECTION_STATE(self):
        tos = self.consumeNextChar() + self.consumeNextChar() + self.consumeNextChar()
        while tos != "]]>":
            tos = tos[1:] + self.consumeNextChar()
        self.state = HTMLStates.DATA_STATE

    def handle_TOKENIZING_CHAR_REF(self):
        return ""
        tos = self.consumeNextChar()
        decoded_value = ''
        if tos in [" ", "\t", "\n", "\x0c", "<", "&", self.additional_allowed_char]:
            pass
        else:
            html_entity = "&"
            curr = self.consumeNextChar()
            while curr != ';':
                html_entity += curr
                curr = self.consumeNextChar()
            html_entity += curr
            try:
                decoded_value = HTMLParser().unescape(html_entity)
            except Exception:
                decoded_value = u'\ufffd'
        self.additional_allowed_char = ""
        return decoded_value


def close_opened_tags(list_of_opened_tags):
    """
    Generate the breakout sequence given the current contexts of opened HTML tags.
    :param list_of_opened_tags: list of opened tags
    :return: breakout sequence
    """
    must_close_tags = ['style', 'title', 'textarea', 'object', 'map', 'video', 'xmp', 'iframe', 'frame', 'noframe',
                       'embed', 'noembed', 'script', 'noscript']
    breakout = ''
    for el in list_of_opened_tags:
        if el['name'] in must_close_tags:
            breakout += '</' + el['name'] + '>'
    return breakout


def breakout_of_current_state(current_state, current_tag):
    """
    Generate the breakout sequence given the current context *within* the current tag.
    :param current_state:
    :param current_tag:
    :return: breakout sequence
    """
    if current_state == HTMLStates.CHARACTER_REFERENCE_IN_ATTRIBUTE_VALUE_STATE:
        if 'kind' in current_tag['attributes'][-1]:
            if current_tag['attributes'][-1]['kind'] == 'unquoted':
                return '>'
            elif current_tag['attributes'][-1]['kind'] == 'double':
                return '">'
            elif current_tag['attributes'][-1]['kind'] == 'single':
                return '\'>'

    if current_tag and current_tag['name'] == 'script' and current_state == HTMLStates.DATA_STATE:
        return '</script>'
    return breakouts[current_state]


def generate_breakout(parser):
    """
    Generate the breakout sequence for the state of parser. This includes breaking out of the current tag and breaking
    out of the context of all opened tags which could interfere with the addition of our markup payload.
    :param parser: the parser and its inherent state for which to generate the breakout sequence
    :return: breakout sequence
    """
    breakout = breakout_of_current_state(parser.state, parser.current_tag)
    if breakout is None:
        log("Missing implementation for breakout state %d" % parser.state)
        raise Exception
    breakout += close_opened_tags(parser.opened_tags)
    return breakout


def getHTMLBreakout(parser, new_part):
    """
    Feed the new part of the input to the parser and generate the breakout sequence of the resulting state.
    :param parser: the parser to feed the part into
    :param new_part: the part which lies between the current state of the parser and the currently investigates source
    :return: the breakout sequence according to the context after processing new_part
    """
    parser.feed(new_part)
    parser.processInput()
    return generate_breakout(parser)
