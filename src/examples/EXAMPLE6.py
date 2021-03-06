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

# flow from cookie to script src
EXAMPLE6 = {
    "finding_id": 6,
    "sink_id": 8,
    "sources": [
        {
            "finding_id": 6,
            "end": 12,
            "hasEncodingURI": 0,
            "source": 8,
            "hasEscaping": 0,
            "start": 10,
            "value_part": "26",
            "source_name": "document.cookie",
            "hasEncodingURIComponent": 0,
            "id": 4979096
        }
    ],
    "url": "https://foo.com/",
    "storage": {
        "cookies": [
            [
                "qqConfig",
                "%7B%22adaptCfgUri%22%3A%20true%7D",
                -1
            ],
            [
                "AMCVS_EDA101AC512D2B230A490D4C%40AdobeOrg",
                "1",
                -1
            ],
            [
                "bkSent",
                "true",
                -1
            ],
            [
                "surveyThreshold_jar",
                "%7B%22pageViewThreshold%22%3A5%7D",
                -1
            ],
            [
                "LANGUAGE_MESSAGE_DISPLAY",
                "3",
                -1
            ],
            [
                "AMCVS_CB793704532E6E4D0A490D44%40AdobeOrg",
                "1",
                -1
            ],
            [
                "AMCV_CB793704532E6E4D0A490D44%40AdobeOrg",
                "2096510701%7CMCIDTS%7C17967%7CMCMID%7C86876343874017344290356127955508516586%7CMCAAMLH-1552918072%7C6%7CMCAAMB-1552918072%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1552320472s%7CNONE%7CvVersion%7C2.0.0%7CMCAID%7CNONE",
                -1
            ],
            [
                "ab.storage.sessionId.039f6de1-2c05-4a2a-8f6e-07d7c8bbde96",
                "%7B%22g%22%3A%22e6914350-4ed1-d3d2-8d1b-671be99c0541%22%2C%22e%22%3A1552315104553%2C%22c%22%3A1552313304579%2C%22l%22%3A1552313304579%7D",
                -1
            ],
            [
                "ab.storage.deviceId.039f6de1-2c05-4a2a-8f6e-07d7c8bbde96",
                "%7B%22g%22%3A%22a0b4b1d2-9783-da4d-34ea-99ca7c50c2b0%22%2C%22c%22%3A1552313304960%2C%22l%22%3A1552313304960%7D",
                -1
            ],
            [
                "amplitude_id_0a8f248176ee40bd81cc371b7cba515ego.com",
                "eyJkZXZpY2VJZCI6IjY2YjE0NjRhLTExYTMtNGVlNC1iMmM4LTY5OTc2YWZhODc3NFIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTU1MjMxMzI5MTYzMiwibGFzdEV2ZW50VGltZSI6MTU1MjMxMzMxODk4MiwiZXZlbnRJZCI6MSwiaWRlbnRpZnlJZCI6Miwic2VxdWVuY2VOdW1iZXIiOjN9",
                -1
            ],
            [
                "geoIP_aka",
                "EU",
                -1
            ],
            [
                "qqPosition",
                "top",
                -1
            ],
            [
                "Conversation_UUID",
                "66999350-441a-11e9-8576-eb5c886fac95",
                -1
            ],
            [
                "MYW_jar",
                "%7B%22addon%22%3A%22%22%2C%22calendarDate%22%3A%22%22%2C%22calendarTier%22%3A%22%22%2C%22date%22%3Anull%2C%22daysTotal%22%3A1%2C%22monthly%22%3Anull%2C%22numDaysElementId%22%3Anull%2C%22numberOfGuests%22%3Anull%2C%22personalMagic%22%3A%22%22%2C%22ticketId%22%3A%22%22%2C%22vouchers%22%3A%22%22%7D",
                -1
            ],
            [
                "TICKET_DATA_jar",
                "%7B%22adultTotal%22%3A2%2C%22childTotal%22%3A0%2C%22allAgesTotal%22%3A0%7D",
                -1
            ],
            [
                "survey_jar",
                "%7B%22skipSurvey%22%3Atrue%7D",
                -1
            ],
            [
                "AMCV_EDA101AC512D2B230A490D4C%40AdobeOrg",
                "-330454231%7CMCIDTS%7C17967%7CMCMID%7C81787613123089510151000178567029872656%7CMCAAMLH-1552926914%7C6%7CMCAAMB-1552926914%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1552329314s%7CNONE%7CMCAID%7CNONE%7CMCSYNCSOP%7C411-17974%7CvVersion%7C3.1.2",
                -1
            ],
            [
                "ppSession_conversationId",
                "148b5740-441c-11e9-97d0-33158405a73b",
                -1
            ],
            [
                "PERSONALMAGIC_jar",
                "%7B%22date%22%3Anull%2C%22daysTotal%22%3Anull%2C%22monthly%22%3Anull%2C%22numberOfGuests%22%3Anull%2C%22addon%22%3Anull%2C%22personalMagic%22%3A%22memory-maker_1_0_AT_progenstr%22%2C%22ticketId%22%3Anull%2C%22numDaysElementId%22%3Anull%7D",
                -1
            ],
            [
                "AFFILIATIONS_jar",
                "%7B%22storedAffiliations%22%3A%5B%5D%7D",
                -1
            ],
            [
                "personalization_jar",
                "%7B%22id%22%3A%22f768c3fa-96b8-4a74-baf9-2ed8b82d0876%22%7D",
                -1
            ],
            [
                "HTTP_X_DISNEY_INTERNAL_SITE",
                "wdw",
                -1
            ],
            [
                "_abck",
                "AE4AC7224ED1AE211C24E66A195ED9DC0214BE9AF73100003B90865C7277EF74~0~8iqRsNfnKL+T6KFBkdeat83orZ2fmaZaN4SvSM/7Iig=~-1~-1",
                -1
            ],
            [
                "IBCDLR_v0201Session",
                "126f1044000001696da71b18604f35deb0043714",
                -1
            ],
            [
                "ppSession_loggedIn",
                "false",
                -1
            ],
            [
                "ppSession_homepageVisitCount",
                "4",
                -1
            ],
            [
                "IBCWDWSession",
                "106f1044000001696debcab75ac0e367368827c2",
                -1
            ],
            [
                "csrf_token",
                "681100584815523273632526720",
                -1
            ],
            [
                "signInHttpReferrer",
                "https%3A%2F%2Fdisneyvacationclub.disney.go.com%2F%3FCMP%3DAFC-DPFY13Q1DIENT1378E%26DISCID%3DDI_go_dvc",
                -1
            ],
            [
                "gi",
                "DE%7CSL%7CSAARBRUCKEN%7C49.23%7C7.00",
                -1
            ],
            [
                "dvcgz",
                "%3F%7C%3F%7CDE%7C%3F%7C%3F",
                -1
            ],
            [
                "SWID",
                "849c48eb-59cf-4918-aee4-f03cf35b1f56",
                -1
            ],
            [
                "ctoVisitor",
                "{%22visitorId%22:%221552322694349-5218009615782%22}",
                -1
            ],
            [
                "ctoSession",
                "{%22sessionId%22:%221552327394256-1485200878232%22%2C%22timestamp%22:1552327394297}",
                -1
            ],
            [
                "ctoBrowserSession",
                "1552327394255",
                -1
            ],
            [
                "boomr_rt",
                "%22%22=&hd=1552327464989",
                -1
            ],
            [
                "mbox",
                "check#true#1552327536|session#74c421f9eee1421c891d4b22f38713b8#1552329336|PC#86ac3cc559ec4b478063725cb8856e62.26_14#1560103476|mboxEdgeServer#mboxedge26.tt.omtrdc.net#1552329336",
                -1
            ],
            [
                "s_pers",
                "%20s_gpv_pn%3Dwdpro%252Fwdw%252Feu%252Fen%252Ftools%252Ffinder%252Fattractions%252Fhollywoodstudios%252Fstarwars%7C1552329276991%3B",
                -1
            ],
            [
                "_fbp",
                "fb.1.1552327387758.376045261",
                -1
            ],
            [
                "_ga",
                "GA1.2.1830535599.1552327388",
                -1
            ],
            [
                "_gid",
                "GA1.2.1287888762.1552327388",
                -1
            ],
            [
                "_gat_gtag_UA_99867646_1",
                "1",
                -1
            ],
            [
                "LPVID",
                "E5YjUyM2Y0YjUwMTYxN2Ey",
                -1
            ],
            [
                "LPSID-65526753",
                "7_Li4ejcTfKju8SavU9LHw",
                -1
            ],
            [
                "finderPublicTokenExpireTime",
                "1552356218686",
                -1
            ],
            [
                "s_sess",
                "%20s_cc%3Dtrue%3B%20s_slt%3D%3B%20s_tp%3D3933%3B%20s_ppv%3Dwdpro%252Fwdw%252Feu%252Fen%252Ftools%252Ffinder%252Fattractions%252Fhollywoodstudios%252Fstarwars%252C13%252C13%252C517%3B",
                -1
            ],
            [
                "_sdsat_enableClickTale",
                "true",
                -1
            ],
            [
                "localeCookie_jar_aka",
                "%7B%22contentLocale%22%3A%22en-eu%22%2C%22version%22%3A%223%22%2C%22precedence%22%3A0%2C%22akamai%22%3A%22true%22%7D",
                -1
            ],
            [
                "languageSelection_jar_aka",
                "%7B%22preferredLanguage%22%3A%22en-eu%22%2C%22version%22%3A%221%22%2C%22precedence%22%3A0%2C%22language%22%3A%22en-eu%22%2C%22akamai%22%3A%22true%22%7D",
                -1
            ],
            [
                "WDPROView",
                "%7B%22version%22%3A2%2C%22preferred%22%3A%7B%22device%22%3A%22desktop%22%2C%22screenWidth%22%3A959%2C%22screenHeight%22%3A517%2C%22screenDensity%22%3A1%7D%2C%22deviceInfo%22%3A%7B%22device%22%3A%22desktop%22%2C%22screenWidth%22%3A959%2C%22screenHeight%22%3A517%2C%22screenDensity%22%3A1%7D%2C%22browserInfo%22%3A%7B%22agent%22%3A%22Chrome%22%2C%22version%22%3A%2230.0.1561.0%22%7D%7D",
                -1
            ],
            [
                "jsongeoip",
                "eyJhcmVhY29kZSI6IjAiLCJjb3VudHJ5IjoiZ2VybWFueSIsImNvbnRpbmVudCI6ImV1IiwiY29ubmVjdGlvbiI6ImJyb2FkYmFuZCIsImNvdW50cnljb2RlIjoiMjc2IiwiY291bnRyeWlzb2NvZGUiOiJkZXUiLCJkb21haW4iOiJ1bmktc2FhcmxhbmQuZGUiLCJkc3QiOiJuIiwiaXNwIjoidW5pdmVyc2l0YWV0IGRlcyBzYWFybGFuZGVzIHNhYXJicnVlY2tlbiIsIm1ldHJvIjoibmllbHNlbiBpaWlhIiwibWV0cm9jb2RlIjoiMjc2MDAzIiwib2Zmc2V0IjoiMTAwIiwicG9zdGNvZGUiOiI2NjEyMSIsInNpYyI6Im5vIHNpYyAiLCJzaWNjb2RlIjoiMCIsInN0YXRlIjoic2FhcmxhbmQiLCJ6aXAiOiIwIiwiaXAiOiIxMzQuOTYuMjI1LjUzIn0%3D",
                -1
            ],
            [
                "geolocation_aka_jar",
                "%7B%22zipCode%22%3A%22%22%2C%22region%22%3A%22SL%22%2C%22country%22%3A%22DE%22%2C%22metro%22%3A%22SAARBRUCKEN%22%2C%22metroCode%22%3A%22%22%7D",
                -1
            ]
        ],
        "storage": [
            [
                "afta_sk",
                "{\"value\":{\"state\":2}}",
                0
            ],
            [
                "en-eu-heroImageDesktop",
                "https://cdn1.parksmedia.wdprapps.disney.com/resize/mwImage/2/1280/720/75/dam/disney-world/es-ar/admission/tickets/latam-scope-DIQS7548000H-30-video-loop.jpg",
                1
            ],
            [
                "en-eu-heroImageMobile",
                "https://cdn1.parksmedia.wdprapps.disney.com/resize/mwImage/2/1280/720/75/dam/disney-world/es-ar/admission/tickets/latam-scope-DIQS7548000H-30-video-loop.jpg",
                1
            ],
            [
                "en_CA-heroImageDesktop",
                "https://cdn1.parksmedia.wdprapps.disney.com/resize/mwImage/2/1280/720/75/dam/disney-world/home/video/now-more-than-ever-tix-offer/walt-disney-world-DIQF5997000H-now-more-than-ever-tix-offer-video.jpg",
                1
            ],
            [
                "en_CA-heroImageMobile",
                "https://cdn1.parksmedia.wdprapps.disney.com/resize/mwImage/2/1280/720/75/dam/disney-world/home/video/now-more-than-ever-tix-offer/walt-disney-world-DIQF5997000H-now-more-than-ever-tix-offer-video.jpg",
                1
            ],
            [
                "en_GB-heroImageDesktop",
                "https://cdn1.parksmedia.wdprapps.disney.com/resize/mwImage/2/1280/720/75/dam/disney-world/es-ar/admission/tickets/latam-scope-DIQS7548000H-30-video-loop.jpg",
                1
            ],
            [
                "en_GB-heroImageMobile",
                "https://cdn1.parksmedia.wdprapps.disney.com/resize/mwImage/2/1280/720/75/dam/disney-world/es-ar/admission/tickets/latam-scope-DIQS7548000H-30-video-loop.jpg",
                1
            ],
            [
                "en_US-heroImageDesktop",
                "https://cdn1.parksmedia.wdprapps.disney.com/resize/mwImage/2/1280/720/75/dam/disney-world/home/video/now-more-than-ever-tix-offer/walt-disney-world-DIQF5997000H-now-more-than-ever-tix-offer-video.jpg",
                1
            ],
            [
                "en_US-heroImageMobile",
                "https://cdn1.parksmedia.wdprapps.disney.com/resize/mwImage/2/1280/720/75/dam/disney-world/home/video/now-more-than-ever-tix-offer/walt-disney-world-DIQF5997000H-now-more-than-ever-tix-offer-video.jpg",
                1
            ],
            [
                "es_AR-heroImageDesktop",
                "https://cdn1.parksmedia.wdprapps.disney.com/resize/mwImage/2/1280/720/75/dam/disney-world/es-ar/admission/tickets/latam-scope-DIQS7548000H-30-video-loop.jpg",
                1
            ],
            [
                "es_AR-heroImageMobile",
                "https://cdn1.parksmedia.wdprapps.disney.com/resize/mwImage/2/1280/720/75/dam/disney-world/es-ar/admission/tickets/latam-scope-DIQS7548000H-30-video-loop.jpg",
                1
            ],
            [
                "es_CL-heroImageDesktop",
                "https://cdn1.parksmedia.wdprapps.disney.com/resize/mwImage/2/1280/720/75/dam/disney-world/es-ar/admission/tickets/latam-scope-DIQS7548000H-30-video-loop.jpg",
                1
            ],
            [
                "es_CL-heroImageMobile",
                "https://cdn1.parksmedia.wdprapps.disney.com/resize/mwImage/2/1280/720/75/dam/disney-world/es-ar/admission/tickets/latam-scope-DIQS7548000H-30-video-loop.jpg",
                1
            ],
            [
                "es_CO-heroImageDesktop",
                "https://cdn1.parksmedia.wdprapps.disney.com/resize/mwImage/2/1280/720/75/dam/disney-world/es-ar/admission/tickets/latam-scope-DIQS7548000H-30-video-loop.jpg",
                1
            ],
            [
                "es_CO-heroImageMobile",
                "https://cdn1.parksmedia.wdprapps.disney.com/resize/mwImage/2/1280/720/75/dam/disney-world/es-ar/admission/tickets/latam-scope-DIQS7548000H-30-video-loop.jpg",
                1
            ],
            [
                "lpLastVisit-65526753",
                "1552327476731",
                1
            ],
            [
                "lpTabId",
                "4418002169",
                0
            ],
            [
                "party_mix",
                "[{\"isDefault\":false,\"accessible\":false,\"adultCount\":2,\"seniorCount\":0,\"childCount\":0,\"orderBuilderId\":null,\"nonAdultAges\":[],\"partyMixId\":\"0\"}]",
                1
            ],
            [
                "prevPageLoadTime",
                "{\"value\":\"wdpro/wdw/eu/en/tools/finder/attractions/hollywoodstudios/starwars|10.0\"}",
                0
            ],
            [
                "translate._wdw_en_EU_en-eu.a11y.loading",
                "Loading your content...",
                0
            ],
            [
                "translate._wdw_en_EU_en-eu.button.action.readless",
                "Show Less",
                0
            ],
            [
                "translate._wdw_en_EU_en-eu.button.action.readmore",
                "Read More",
                0
            ],
            [
                "translate._wdw_en_EU_en-eu.calendar.selectedDate",
                "Selected date ",
                0
            ],
            [
                "translate._wdw_en_EU_en-eu.calendar.today",
                "Today",
                0
            ],
            [
                "_bcnbf",
                "JTVCJTdCJTIybG9jJTIyJTNBJTIyaHR0cHMlM0ElMkYlMkZkaXNuZXl3b3JsZC5kaXNuZXkuZ28uY29tJTJGZW4tZXUlMkZhdHRyYWN0aW9ucyUyRmhvbGx5d29vZC1zdHVkaW9zJTJGc3Rhci13YXJzJTJGJTIyJTJDJTIycGlkJTIyJTNBMTI1OTU0NDU0MTkyMTI3JTJDJTIyc2lkJTIyJTNBJTIyMWQyNDhpajMyOGpoMGduMm81czV1ajNrNDElMjIlMkMlMjJic2lkJTIyJTNBJTIyZGIwYzNiNDYxMDYwYjg1NDY4MDViYmExZTRiNzUzNjZhNjQxJTIyJTJDJTIydHMlMjIlM0ExNTUyMzI3NDc4NDE0JTJDJTIydHlwZSUyMiUzQSUyMmF1dG9mJTIyJTJDJTIycGF5JTIyJTNBJTdCJTIydCUyMiUzQTE1NTIzMjc0Nzg0MTQlMkMlMjJwJTIyJTNBJTVCJTIyX19fRE9NWFNTRmluZGVyUmVwb3J0UmVjb3JkcyUyMiUyQyUyMl9fX0RPTVhTU1Rva2VuUmVwb3J0UmVjb3JkcyUyMiUyQyUyMl9fX0RPTVhTU0ZpbmRlckV2YWxTY3JpcHRzJTIyJTJDJTIyX19fRE9NWFNTRmluZGVyRGVjb2RlQ291bnRlcnMlMjIlMkMlMjJfX19ET01YU1NGaW5kZXJJbmRleGVkREJzJTIyJTVEJTJDJTIyYSUyMiUzQSU3QiU3RCUyQyUyMmMlMjIlM0EwJTdEJTdEJTVE",
                0
            ],
            [
                "_bcnbsid",
                "db0c3b461060b8546805bba1e4b75366a641",
                0
            ],
            [
                "_bcncsid",
                "1d248ij328jh0gn2o5s5uj3k41",
                0
            ],
            [
                "_bcnctkn",
                "797d4d419fb31ab4b5e08b29dc0f4f68eb85",
                1
            ],
            [
                "_bcnsts",
                "1552331067193",
                0
            ]
        ]
    },
    "value": "//mboxedge26.tt.omtrdc.net/m2/disney/mbox/ajax?mboxHost=disneyworld.disney.go.com&mboxPage=1a34d44177c94a99a5ab1b7e7ca2fe8e&screenHeight=768&screenWidth=1024&browserWidth=959&browserHeight=517&browserTimeOffset=60&colorDepth=24&mboxSession=74c421f9eee1421c891d4b22f38713b8&mboxXDomain=enabled&host=https%3A%2F%2Fdisneyworld.disney.go.com%2Fen-eu%2Fattractions%2Fhollywood-studios%2Fstar-wars%2F&mboxCount=1&mboxTime=1552331074514&mboxPC=86ac3cc559ec4b478063725cb8856e62.26_14&mboxMCSDID=2906D36503C95488-5F1BC001C14E43D1&mboxMCGVID=81787613123089510151000178567029872656&mboxAAMB=RKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y&mboxMCGLH=6&vst.trk=w88.go.com&vst.trks=sw88.go.com&mbox=WDW_Global_Mbox&mboxId=0&contentLocale=eu&contentLanguage=en&marketingRegion=eu&deviceInfo=desktop%3Adesktop&guestType=Guest&guestAffiliations=Standard%20Guest&registrationStatus=Not%20Registered&pageId=starwars&storeType=Consumer&siteSection=tools%2Ffinder%2Fattractions%2Fhollywoodstudios&toggles=rt%3BpersonalizationDecision%3Atrue%2Crt%3BJSP13N%3Atrue%2Crt%3BECAF%3Atrue&entity.id=18263038%3BentityType%3DAttraction&entity.name=Star%20Wars%20at%20Walt%20Disney%20World%20Resort&mboxURL=https%3A%2F%2Fdisneyworld.disney.go.com%2Fen-eu%2Fattractions%2Fhollywood-studios%2Fstar-wars%2F&mboxReferrer=&mboxVersion=62",
    "d2": "",
    "d3": "",
    "d1": ""
}
