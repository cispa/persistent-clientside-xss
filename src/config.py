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

import argparse

from constants.sinks import SINKS
from constants.sources import SOURCES

parser = argparse.ArgumentParser(description="""Automatic Exploit Generator resulted from the work 
    Don't Trust The Locals: Investigating the Prevalence of Persistent Client-Side Cross-Site Scripting in the Wild.
    Capable of generating RCXSS and PCXSS exloits.
    Be aware there is a small caveat to changing the payload to something different ;)
    """)

parser.add_argument("--debug", action="store_true")
parser.add_argument("--payload", default='alert(document.domain)')

CONFIG = parser.parse_args()

JS_SINKS = [SINKS.SINK_EXEC, SINKS.SINK_SCRIPT_TEXT]
HTML_SINKS = [SINKS.SINK_DOC_WRITE, SINKS.SINK_INNER_HTML, SINKS.SINK_IFRAME_SRCDOC]

GENERATE_EXPLOIT_FOR_SOURCES = [SOURCES.SOURCE_LOCATION_HREF, SOURCES.SOURCE_LOCATION_SEARCH,
                                SOURCES.SOURCE_LOCATION_HASH, SOURCES.SOURCE_URL, SOURCES.SOURCE_DOCUMENT_URI,
                                SOURCES.SOURCE_BASE_URI]
GENERATE_EXPLOIT_FOR_SOURCES += [SOURCES.SOURCE_COOKIE]
GENERATE_EXPLOIT_FOR_SOURCES += [SOURCES.SOURCE_LOCAL_STORAGE]
GENERATE_EXPLOIT_FOR_SOURCES += [SOURCES.SOURCE_SESSION_STORAGE]

SCRIPT_SOURCE_HOSTNAME = 'foo.bar'
