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

# flow from LocalStorage to script src
EXAMPLE5 = {
    "finding_id": 5,
    "sink_id": 8,
    "sources": [
        {
            "finding_id": 5,
            "end": 28,
            "hasEncodingURI": 0,
            "source": 13,
            "hasEscaping": 0,
            "start": 8,
            "value_part": "acstatic-dun.126.net",
            "source_name": "localStorage",
            "hasEncodingURIComponent": 0,
            "id": 43058
        },
        {
            "finding_id": 5,
            "end": 43,
            "hasEncodingURI": 0,
            "source": 13,
            "hasEscaping": 0,
            "start": 29,
            "value_part": "2.4.1_2e562ea2",
            "source_name": "localStorage",
            "hasEncodingURIComponent": 0,
            "id": 43060
        }
    ],
    "url": "https://foo.com/",
    "storage": {
        "cookies": [
            [
                "uuid_tt_dd",
                "10_22544960530-1552320706758-709585",
                -1
            ],
            [
                "c_adb",
                "1",
                -1
            ],
            [
                "_ga",
                "GA1.2.1652286326.1552312993",
                -1
            ],
            [
                "_gid",
                "GA1.2.2006355224.1552312993",
                -1
            ],
            [
                "c-login-auto",
                "2",
                -1
            ],
            [
                "UM_distinctid",
                "1696d10da042d1-0f5abab38-67257724-c0000-1696d10da0515d",
                -1
            ],
            [
                "CloudGuest",
                "wQ7avebqcKYEzx/0LSbci1m5tCX7OiTMb6UkTP6pN1awkjcOT5Kh2jlWob1G7XtG/KU97M2m32pju7ZMXYEeeUIGWT32+NoLx67Zb8WCfRxoYSR8+b11yq/8/Y81AhrlP6Jv3hAvEe7so8D/wwLaNye6/HRY/DzhTZjQql/xqDGdddR+aSajiR4SHZlt2QfI",
                -1
            ],
            [
                "Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac",
                "1552312923",
                -1
            ],
            [
                "Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac",
                "1552313041",
                -1
            ],
            [
                "Hm_ct_6bcd52f51e9b3dce32bec4a3997715ac",
                "6525*1*10_22544960530-1552320706758-709585",
                -1
            ],
            [
                "dc_session_id",
                "10_1552320706758.210763",
                -1
            ],
            [
                "WM_NI",
                "Sgn2cFKSRWzsr5OpJ%2F5ucKnPpadyXJRwd4srhU45WlAPSVnvAidq%2B6B4R64J4Rc2VkmgiI%2F90wAKlO5I65oG%2B7jTwWorx217IOaxUWDT9ecPlzWZSjbfa4%2FFycLBZAumcnk%3D",
                -1
            ],
            [
                "WM_NIKE",
                "9ca17ae2e6ffcda170e2e6ee85e9809bf5acd0f85293eb8ea2d14f938e8b85b83cf2a6fd8cd94f8994fbb2f22af0fea7c3b92a91b9a2d3e24e898d9eb8f979b2eb8191c925f7abadaced5cb4bfac9adb4292a9acd5f27aac8bfcd6d66883909db7ed7e83b7ac92aa3e82ec9ed7b742f88eadd3d561afb9a7aaae33f4a98facef45f797fad6ee4de9e9a6b5f65dadaeb8d3b43d8b91af99d85d888cf786e25cb0a699bbd262a2baafd5ae4ebbbd84a3d94bb7b3ad8fea37e2a3",
                -1
            ],
            [
                "WM_TID",
                "Azmj1TXfxC1BEFQRAAZphyyzldQLboQs",
                -1
            ],
            [
                "dc_tos",
                "po7gf4",
                -1
            ]
        ],
        "storage": [
            [
                "default:wm_cf",
                "acstatic-dun.126.net,ac.dun.163yun.com,9ca170a1abeedba16ba1f2ac96ed26f3eafd9af866eebda18eae7ef2f1acc3af2aa2bdbbc3b92aa3bde285f866eeeffad4fc7faef2ad90f025b6eee183a128e2bca4c3b92ae2f4ee8ee867e2e6fbd1af2aafbba7c3b939f4f0e4c3e26faffef6d3b328e2bdab8aa132f1f000cda161a7b3eedbb43cf0fea586ec2afaed00d1af2aa6bba3c3b93af4f4ee87e863e2e6fdd1b328e2adab8ea132f2f0e4c3f26fabfef6d4b33cf0feab8be270e2e6aa82ef79a7f4ee86e579e2e6aa82ef79a7f4ee86f679e2e6aa82ef79a7f4ee93e880e2e6ffcda169afb2eedbb128e2bda7c3b93bf4f0e4c3f366e2e6eebac73cf4f000d1b83dfbedf8dab740f1fee4c3e870a1fef695f17fa7f4ee83ef2afafeeecda163b6b0eedbb43af4f000d1af2aa8acba91a132fceafcd1b33cf4f0e4c3f780adfef6d3b33cf4a3,2.4.1_2e562ea2,2.4.1_a6cab3aa,1552313163235",
                1
            ],
            [
                "randomN",
                "0",
                1
            ],
            [
                "sourceFrom",
                "https://passport.csdn.net/login",
                1
            ],
            [
                "WM_CONFIG",
                "{\"sConfig\":\"9ca170a1abeedba16ba1f2ac96ed26f3eafd9af866eebda18eae7ef2f1acc3af2aa2bdbbc3b92aa3bde285f866eeeffad4fc7faef2ad90f025b6eee183a128e2bca4c3b92ae2f4ee8ee867e2e6fbd1af2aafbba7c3b939f4f0e4c3e26faffef6d3b328e2bdab8aa132f1f000cda161a7b3eedbb43cf0fea586ec2afaed00d1af2aa6bba3c3b93af4f4ee87e863e2e6fdd1b328e2adab8ea132f2f0e4c3f26fabfef6d4b33cf0feab8be270e2e6aa82ef79a7f4ee86e579e2e6aa82ef79a7f4ee86f679e2e6aa82ef79a7f4ee93e880e2e6ffcda169afb2eedbb128e2bda7c3b93bf4f0e4c3f366e2e6eebac73cf4f000d1b83dfbedf8dab740f1fee4c3e870a1fef695f17fa7f4ee83ef2afafeeecda163b6b0eedbb43af4f000d1af2aa8acba91a132fceafcd1b33cf4f0e4c3f780adfef6d3b33cf4a3\",\"buildVersion\":\"2.4.1_2e562ea2\",\"staticServer\":\"acstatic-dun.126.net\",\"valid\":1552313170191}",
                1
            ],
            [
                "WM_DID",
                "djtY+d/uZQ5BAREQREd502z3kZEKL5Qs__1552385046446__1552313046446",
                1
            ],
            [
                "WM_NI",
                "Sgn2cFKSRWzsr5OpJ/5ucKnPpadyXJRwd4srhU45WlAPSVnvAidq+6B4R64J4Rc2VkmgiI/90wAKlO5I65oG+7jTwWorx217IOaxUWDT9ecPlzWZSjbfa4/FycLBZAumcnk=",
                1
            ],
            [
                "WM_NIKE",
                "9ca17ae2e6ffcda170e2e6ee85e9809bf5acd0f85293eb8ea2d14f938e8b85b83cf2a6fd8cd94f8994fbb2f22af0fea7c3b92a91b9a2d3e24e898d9eb8f979b2eb8191c925f7abadaced5cb4bfac9adb4292a9acd5f27aac8bfcd6d66883909db7ed7e83b7ac92aa3e82ec9ed7b742f88eadd3d561afb9a7aaae33f4a98facef45f797fad6ee4de9e9a6b5f65dadaeb8d3b43d8b91af99d85d888cf786e25cb0a699bbd262a2baafd5ae4ebbbd84a3d94bb7b3ad8fea37e2a3",
                1
            ],
            [
                "WM_TID",
                "Azmj1TXfxC1BEFQRAAZphyyzldQLboQs",
                1
            ],
            [
                "_uab_collina",
                "155231304265382344795018",
                1
            ],
            [
                "_umcost",
                "5918",
                1
            ],
            [
                "_um_cn_umsvtn",
                "T1D5FF16D42539EB5F43DCE73F4118EFB24E39AD4E80B3DD335857F8CA0@@1552313056",
                1
            ],
            [
                "_um_cn__umdata",
                "G22F2AE3D0C79F3E99E20C60C4BC35CBE6B9F09",
                1
            ]
        ]
    },
    "value": "https://acstatic-dun.126.net/2.4.1_2e562ea2/watchman.min.js",
    "d2": '',
    "d3": "https://acstatic-dun.126.net/tool.min.js:6:149",
    "d1": ''
}
