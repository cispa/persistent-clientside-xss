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


class SINKS:
    SINK_EXEC = 1
    SINK_DOC_WRITE = 2
    SINK_INNER_HTML = 3
    SINK_IFRAME_SRCDOC = 4
    SINK_SCRIPT_TEXT = 5
    SINK_LOCATION = 7
    SINK_SCRIPT_SRC = 8
    SINK_IMG_SRC = 10
    SINK_OBJECT_DATA = 10
    SINK_EMBED_SRC = 10
    SINK_IFRAME_SRC = 10
    SINK_FRAME_SRC = 10
    SINK_COOKIE = 14
    SINK_POST_MESSAGE = 15
    SINK_SET_ATTR_BOTH = 16
    SINK_SET_ATTR_VAL = 17
    SINK_LOCAL_STORAGE_NAME = 20
    SINK_LOCAL_STORAGE_VALUE = 21
    SINK_LOCAL_STORAGE_BOTH_VALUE = 23
    SINK_LOCAL_STORAGE_BOTH_NAME = 22
    SINK_FAKE_EVAL_FLOW = 30
