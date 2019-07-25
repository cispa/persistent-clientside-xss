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

from generator import generate_exploit_for_finding
from examples.EXAMPLE1 import EXAMPLE1
from examples.EXAMPLE2 import EXAMPLE2
from examples.EXAMPLE3 import EXAMPLE3
from examples.EXAMPLE4 import EXAMPLE4
from examples.EXAMPLE5 import EXAMPLE5
from examples.EXAMPLE6 import EXAMPLE6
from pprint import pprint

sep = '---------------------'


def main():
    # Example 1 is annotated with the structure of a `finding` and `source`
    print 'Running Exploit generation on example 1, which consist of a flow from a cookie into the DOM. ' \
          'Annotated flow can be found in examples/EXAMPLE1.py'
    print sep
    print 'Flow:'
    pprint(EXAMPLE1)
    print sep
    print 'Generated Exploit:'
    print generate_exploit_for_finding(EXAMPLE1)

    # print len(generate_exploit_for_finding(EXAMPLE2))
    # print len(generate_exploit_for_finding(EXAMPLE3))
    # print len(generate_exploit_for_finding(EXAMPLE4))
    # print len(generate_exploit_for_finding(EXAMPLE5))
    # Example 6 generates 7 exploits due to the value ending up in the sink being '26'
    # this value can be found in various storage entries such that for each one there will be an exploit generated
    # print len(generate_exploit_for_finding(EXAMPLE6))


if __name__ == '__main__':
    main()
