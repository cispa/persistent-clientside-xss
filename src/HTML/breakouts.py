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

# breakouts needed depending on in-tag context, e.g. if '<' was parsed we are in the TAG_OPEN_STATE
# which we can terminate with e.g. 'div></div>'
breakouts = [
    '',  # Dummy = 0
    '',  # DATA_STATE = 1
    'foo;',  # CHAR_REF_DATA_STATE = 2
    None,  # RCDATA_STATE = 3
    None,  # CHAR_REF_IN_RCDATA_STATE = 4
    None,  # RAWTEXT_STATE = 5
    '',  # SCRIPT_DATA_STATE = 6
    None,  # PLAINTEXT_STATE = 7
    'div></div>',  # TAG_OPEN_STATE = 8
    'div>',  # END_TAG_OPEN_STATE = 9
    '>',  # TAG_NAME_STATE = 10
    None,  # RCDATA_LESS_THAN_SIGN_STATE = 11
    None,  # RCDATA_END_TAG_OPEN_STATE = 12
    None,  # RCDATA_END_TAG_NAME_STATE = 13
    None,  # RAWTEXT_LESS_THAN_SIGN_STATE = 14
    None,  # RAWTEXT_END_TAG_OPEN_STATE = 15
    None,  # RAWTAG_END_TAG_NAME_STATE = 16
    None,  # SCRIPT_DATA_LESS_THAN_SIGN_STATE = 17
    None,  # SCRIPT_DATA_END_TAG_OPEN_STATE = 18
    None,  # SCRIPT_DATA_END_TAG_NAME_STATE = 19
    None,  # SCRIPT_DATA_ESCAPE_START_STATE = 20
    None,  # SCRIPT_DATA_ESCAPE_START_DASH_STATE = 21
    None,  # SCRIPT_DATA_ESCAPED_STATE = 22
    None,  # SCRIPT_DATA_ESCAPED_DASH_STATE = 23
    None,  # SCRIPT_DATA_ESCAPED_DASH_DASH_STATE = 24
    None,  # SCRIPT_DATA_ESCAPED_LESS_THAN_SIGN_STATE = 25
    None,  # SCRIPT_DATA_ESCAPED_END_TAG_OPEN_STATE = 26
    None,  # SCRIPT_DATA_ESCAPED_END_TAG_NAME_STATE = 27
    None,  # SCRIPT_DATA_DOUBLE_ESCAPE_START_STATE = 28
    None,  # SCRIPT_DATA_DOUBLE_ESCAPED_STATE = 29
    None,  # SCRIPT_DATA_DOUBLE_ESCAPED_DASH_STATE = 30
    None,  # SCRIPT_DATA_DOUBLE_ESCAPED_DASH_DASH_STATE = 31
    None,  # SCRIPT_DATA_DOUBLE_ESCAPED_LESS_THAN_SIGN_STATE = 32
    None,  # SCRIPT_DATA_DOUBLE_ESCAPE_END_STATE = 33
    '>',  # BEFORE_ATTRIBUTE_NAME_STATE = 34
    '>',  # ATTRIBUTE_NAME_STATE = 35
    '="">',  # AFTER_ATTRIBUTE_NAME_STATE = 36
    '"">',  # BEFORE_ATTRIBUTE_VALUE_STATE = 37
    '">',  # ATTRIBUTE_VALUE_DOUBLE_QUOTED_STATE = 38
    '\'>',  # ATTRIBUTE_VALUE_SINGLE_QUOTED_STATE = 39
    '>',  # ATTRIBUTE_VALUE_UNQUOTED_STATE = 40
    '',  # CHARACTER_REFERENCE_IN_ATTRIBUTE_VALUE_STATE = 41
    '>',  # AFTER_ATTRIBUTE_VALUE_QUOTED_STATE = 42
    '>',  # SELF_CLOSING_START_TAG_STATE = 43
    '>',  # BOGUS_COMMENT_STATE = 44
    None,  # MARKUP_DECLARATION_OPEN_STATE = 45
    '-- -->',  # COMMENT_START_STATE = 46
    '- -->',  # COMMENT_START_DASH_STATE = 47
    ' -->',  # COMMENT_STATE = 48
    '->',  # COMMENT_END_DASH_STATE = 49
    '>',  # COMMENT_END_STATE = 50
    None,  # COMMENT_END_BANK_STATE = 51
    None,  # DOCTYPE_STATE = 52
    None,  # BEFORE_DOCTYPE_NAME_STATE = 53
    None,  # DOCTYPE_NAME_STATE = 54
    None,  # AFTER_DOCTYPE_NAME_STATE = 55
    None,  # AFTER_DOCTYPE_PUBLIC_KEYWORD_STATE = 56
    None,  # BEFORE_DOCTYPE_PUBLIC_IDENTIFIER_STATE = 57
    None,  # DOCTYPE_PUBLIC_IDENTIFIER_DOUBLE_QUOTED_STATE = 58
    None,  # DOCTYPE_PUBLIC_IDENTIFIER_SINGLE_QUOTED_STATE = 59
    None,  # AFTER_DOCTPYE_PUBLIC_IDENTIFIER_STATE = 60
    None,  # BETWEEN_DOCTYPE_PUBLIC_AND_SYSTEM_IDENTIFIERS_STATE = 61
    None,  # AFTER_DOCTYPE_SYSTEM_KEYWORD_STATE = 62
    None,  # BEFORE_DOCTYPE_SYSTEM_IDENTIFIER_STATE = 63
    None,  # DOCTPYE_SYSTEM_IDENTIFIER_DOUBLE_QUOTED_STATE = 64
    None,  # DOCTPYE_SYSTEM_IDENTIFIER_SINGLE_QUOTED_STATE = 65
    None,  # AFTER_DOCTYPE_SYSTEM_IDENTIFIER_STATE = 66
    None,  # BOGUS_DOCTYPE_STATE = 67
    None,  # CDATA_SECTION_STATE = 68
    None,  # TOKENIZING_CHAR_REF = 69
]
