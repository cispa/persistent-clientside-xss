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

# flow from document.cookie into eval
EXAMPLE3 = {
    "finding_id": 3,
    "sink_id": 1,
    "sources": [
        {
            "finding_id": 3,
            "end": 22,
            "hasEncodingURI": 0,
            "source": 8,
            "hasEscaping": 0,
            "start": 1,
            "value_part": "{\"countryCode\": \"de\"}",
            "source_name": "document.cookie",
            "hasEncodingURIComponent": 0,
            "id": 24599
        }
    ],
    "url": "https://foo.com/",
    "storage": {
        "cookies": [
            [
                "sbi_debug",
                "false",
                -1
            ],
            [
                "sbi_debug",
                "false",
                -1
            ],
            [
                "CBS_INTERNAL",
                "0",
                -1
            ],
            [
                "fly_geo",
                "{\"countryCode\": \"de\"}",
                -1
            ],
            [
                "fly_device",
                "desktop",
                -1
            ],
            [
                "fly_zip",
                "",
                -1
            ],
            [
                "_cb_ls",
                "1",
                -1
            ],
            [
                "cnetSessionStarted",
                "true",
                -1
            ],
            [
                "cnetSessionCount",
                "1",
                -1
            ],
            [
                "cnet_ad",
                "%7B%22region%22%3A%22uk%22%2C%22session%22%3A%22b%22%2C%22subSession%22%3A%225%22%2C%22type%22%3A%22gpt%22%7D",
                -1
            ],
            [
                "arrowImp",
                "true",
                -1
            ],
            [
                "carriercount",
                "4",
                -1
            ],
            [
                "currentcarriername",
                "not-specified",
                -1
            ],
            [
                "_cb",
                "eheyVCTXDx8D97IVM",
                -1
            ],
            [
                "_chartbeat2",
                ".1552312965752.1552313012202.1.DiDMiAC3bEHCDJplsIBDbYkuBqzvVY.22",
                -1
            ],
            [
                "_cb_svref",
                "null",
                -1
            ],
            [
                "_chartbeat4",
                "t=-cWH2BDQkn9Cm_RqZCk7mVCgjJ3K&E=0&x=0&c=0.07&y=4566&w=502",
                -1
            ],
            [
                "__gads",
                "ID=24c14c73bb31d697:T=1552320819:S=ALNI_MacGEc--SGOigx0Cd5SDDeVx0jDEw",
                -1
            ],
            [
                "pv",
                "51",
                -1
            ],
            [
                "arrowImpCnt",
                "100",
                -1
            ],
            [
                "utag_main",
                "v_id:01696d10e3ac001d6f609aef03c503067001c05f00718$_sn:1$_ss:0$_st:1552314822696$ses_id:1552313017263%3Bexp-session$_pn:2%3Bexp-session$dc_visit:1$dc_event:1%3Bexp-session$dc_region:eu-central-1%3Bexp-session",
                -1
            ],
            [
                "LDCLGFbrowser",
                "d7e347b2-69d8-4ace-aea7-19601b67fd27",
                -1
            ],
            [
                "XCLGFbrowser",
                "Kf2qqFyGiTU/irEHobM",
                -1
            ],
            [
                "prevPageType",
                "tag_page",
                -1
            ],
            [
                "s_vnum",
                "1554905022924%26vn%3D1",
                -1
            ],
            [
                "s_invisit",
                "true",
                -1
            ],
            [
                "s_getNewRepeat",
                "1552313022938-New",
                -1
            ],
            [
                "s_lv_undefined",
                "1552313022939",
                -1
            ],
            [
                "s_lv_undefined_s",
                "First%20Visit",
                -1
            ],
            [
                "AMCVS_10D31225525FF5790A490D4D%40AdobeOrg",
                "1",
                -1
            ],
            [
                "AMCV_10D31225525FF5790A490D4D%40AdobeOrg",
                "-894706358%7CMCMID%7C78454760721416537983444194616159121248%7CMCAAMLH-1552917823%7C6%7CMCAAMB-1552917823%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCCIDH%7C111562540%7CMCOPTOUT-1552320223s%7CNONE%7CvVersion%7C2.3.0",
                -1
            ],
            [
                "RT",
                "\"sl=48&ss=1552312963993&tt=118880&obo=0&bcn=%2F%2F0211c813.akstat.io%2F&sh=1552313020195%3D48%3A0%3A118880%2C1552313019955%3D47%3A0%3A115328%2C1552313019461%3D46%3A0%3A108184%2C1552313015824%3D45%3A0%3A101454%2C1552313009938%3D44%3A0%3A98425&dm=cnet.com&si=9082a4ae-ba5a-4f29-b32d-2691fe3980bd\"",
                -1
            ]
        ],
        "storage": [
            [
                "IXWRAPPERAdserverOrgIp",
                "{\"t\":1552312965498,\"d\":{\"response\":\"match\",\"data\":{\"TDID\":\"d9652573-a70b-45ec-acdd-5bbcfa14022a\",\"TDID_LOOKUP\":\"TRUE\",\"TDID_CREATED_AT\":\"2019-02-11T16:12:48\"}},\"e\":1552917765498}",
                1
            ],
            [
                "tealium_timing",
                "{\"domain\":\"www.cnet.com\",\"pathname\":\"/google/\",\"query_string\":\"\",\"timestamp\":1552313021576,\"dns\":0,\"connect\":0,\"response\":17,\"dom_loading_to_interactive\":543,\"dom_interactive_to_complete\":0,\"load\":0,\"time_to_first_byte\":1486,\"front_end\":0,\"fetch_to_response\":1486,\"fetch_to_complete\":0,\"fetch_to_interactive\":2114}",
                1
            ],
            [
                "_cb",
                "eheyVCTXDx8D97IVM",
                1
            ],
            [
                "_cb_expires",
                "1586441012203",
                1
            ],
            [
                "_cb_svref",
                "null",
                1
            ],
            [
                "_cb_svref_expires",
                "1552314812428",
                1
            ],
            [
                "_chartbeat2",
                ".1552312965752.1552313012202.1.DiDMiAC3bEHCDJplsIBDbYkuBqzvVY.22",
                1
            ],
            [
                "_chartbeat2_expires",
                "1586441012204",
                1
            ],
            [
                "_chartbeat4",
                "t=-cWH2BDQkn9Cm_RqZCk7mVCgjJ3K&E=0&x=0&c=0.07&y=4566&w=502",
                1
            ],
            [
                "_chartbeat4_expires",
                "1552313076232",
                1
            ]
        ]
    },
    "value": "({\"countryCode\": \"de\"})",
    "d2": "",
    "d3": "",
    "d1": "eval"
}
