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

# flow from LocalStorage into a DOM sink
EXAMPLE2 = {u'd1': u'innerHTML',
            u'd2': u'div',
            u'd3': u'http://cpro.baidustatic.com/cpro/ui/c.js:5:6125',
            u'finding_id': 364,
            u'sink_id': 3,
            u'sources': [{u'end': 120,
                          u'finding_id': 364,
                          u'hasEncodingURI': 0,
                          u'hasEncodingURIComponent': 0,
                          u'hasEscaping': 0,
                          u'id': 1497,
                          u'source': 13,
                          u'source_name': u'localStorage',
                          u'start': 113,
                          u'value_part': u'2989570'},
                         {u'end': 1360,
                          u'finding_id': 364,
                          u'hasEncodingURI': 0,
                          u'hasEncodingURIComponent': 0,
                          u'hasEscaping': 0,
                          u'id': 1513,
                          u'source': 13,
                          u'source_name': u'localStorage',
                          u'start': 1344,
                          u'value_part': u'9d8c87a7a6cbd356'}],
            u'storage': {u'cookies': [[u'itssohu', u'true', -1],
                                      [u'reqtype', u'pc', -1],
                                      [u'gidinf', u'x099980108ee0f563e31ca077000ad917e88eaddac43', -1],
                                      [u'IPLOC', u'EU', -1],
                                      [u'SUV', u'190312001119IHW8', -1],
                                      [u'beans_freq', u'1', -1],
                                      [u'beans_dmp',
                                       u'%7B%22admaster%22%3A1552312928%2C%22shunfei%22%3A1552312928%2C%22reachmax%22%3A1552312928%2C%22lingji%22%3A1552312928%2C%22yoyi%22%3A1552312928%2C%22ipinyou%22%3A1552312928%2C%22ipinyou_admaster%22%3A1552312928%2C%22miaozhen%22%3A1552312928%2C%22diantong%22%3A1552312928%2C%22huayang%22%3A1552312928%7D',
                                       -1],
                                      [u'beans_dmp_done', u'1', -1],
                                      [u't', u'1552312931474', -1]],
                         u'storage': [[u'u2989570_0',
                                       u'{"queryid":"9d8c87a7a6cbd356","tuid":"u2989570_0","placement":{"basic":{"sspId":1,"userId":7017965,"flowType":1,"cname":"50071140_cpr","tuId":9223372032562799000,"sellType":2,"rspFormat":1,"conBackEnv":1},"container":{"height":250,"width":300,"sizeType":1,"anchoredType":1,"floated":{}},"fillstyle":{"elements":[51],"layout":[1,2],"styleTemplateId":[60103],"txt":{"number":0},"styleType":3,"ignoreStyleMode":1},"adslottype":0,"userdefine":"%7Cadp%3D1%7Cat%3D3%7CconBW%3D1%7Ccpro%5Ftemplate%3DbaiduCustNativeAD%7Cpat%3D1%7Cpih%3D0%7Cpiw%3D0%7Cptbg%3D90%7Cptp%3D0%7Cptt%3D0%7Crss1%3D%23FFFFFF%7Crss2%3D%23000000%7Ctft%3D0%7CtitFF%3D%E5%BE%AE%E8%BD%AF%E9%9B%85%E9%BB%91%7CtitFS%3D14%7CtitSU%3D0%7Ctlt%3D1%7Ctn%3DbaiduCustNativeAD","encode_userdefine":"encoded","complement_type":2,"update":"1551061818_1550815158"},"extends":{"ssph":250,"sspw":300},"pdb_deliv":{"deliv_id":"0","deliv_des":{},"brandad":0},"order_deliv":{"deliv_id":"0","demand_id":"0"},"rtb_deliv":{"deliv_id":"0","demand_id":"2989570"},"media_protect":"","adExpire":1552312893991}',
                                       1],
                                      [u'u3030067_0',
                                       u'{"queryid":"04e803ce7d9afdf6","tuid":"u3030067_0","placement":{"basic":{"sspId":1,"userId":7017965,"flowType":1,"cname":"50071140_cpr","tuId":9223372032562839000,"sellType":2,"rspFormat":1,"conBackEnv":1},"container":{"height":250,"width":300,"sizeType":1,"anchoredType":1,"floated":{}},"fillstyle":{"elements":[51],"layout":[1,2],"styleTemplateId":[60102],"txt":{"number":0},"styleType":3,"ignoreStyleMode":1},"adslottype":0,"userdefine":"%7Cat%3D3%7Ccpro%5Ftemplate%3DbaiduCustNativeAD%7Cpat%3D17%7Ctn%3DbaiduCustNativeAD","encode_userdefine":"encoded","complement_type":2,"update":"1551061913_1500078144"},"extends":{"ssph":250,"sspw":300},"pdb_deliv":{"deliv_id":"0","deliv_des":{},"brandad":0},"order_deliv":{"deliv_id":"0","demand_id":"0"},"rtb_deliv":{"deliv_id":"0","demand_id":"3030067"},"media_protect":"","adExpire":1552312896313}',
                                       1],
                                      [u'u3030383_0',
                                       u'{"queryid":"e4b854e0b6362d00","tuid":"u3030383_0","placement":{"basic":{"sspId":1,"userId":7017965,"flowType":1,"cname":"50071140_cpr","tuId":9223372032562839000,"sellType":2,"rspFormat":1,"conBackEnv":1},"container":{"height":150,"width":300,"sizeType":1,"anchoredType":1,"floated":{}},"fillstyle":{"elements":[51],"layout":[1,2],"styleTemplateId":[60101],"txt":{"number":0},"styleType":3,"ignoreStyleMode":1},"adslottype":0,"userdefine":"%7Cadp%3D1%7Cat%3D3%7CconBW%3D1%7Ccpro%5Ftemplate%3DbaiduCustNativeAD%7Cpat%3D6%7Cpih%3D0%7Cpiw%3D0%7CptBC%3D%23F2F2F2%7CptFC%3D%23000000%7CptFS%3D14%7Cptbg%3D50%7Cptc%3D%25E7%258C%259C%25E4%25BD%25A0%25E6%2584%259F%25E5%2585%25B4%25E8%25B6%25A3%7Cptp%3D1%7Cptt%3D1%7Crss1%3D%23ffffff%7Crss2%3D%23000000%7CtitFF%3D%E5%BE%AE%E8%BD%AF%E9%9B%85%E9%BB%91%7CtitFS%3D12%7CtitSU%3D0%7Ctn%3DbaiduCustNativeAD","encode_userdefine":"encoded","complement_type":2,"update":"1551061989_1500078144"},"extends":{"ssph":150,"sspw":300},"pdb_deliv":{"deliv_id":"0","deliv_des":{},"brandad":0},"order_deliv":{"deliv_id":"0","demand_id":"0"},"rtb_deliv":{"deliv_id":"0","demand_id":"3030383"},"media_protect":"","adExpire":1552312894174}',
                                       1],
                                      [u'u3031513_0',
                                       u'{"queryid":"a3da7ca3123f0f40","tuid":"u3031513_0","placement":{"basic":{"sspId":1,"userId":7017965,"flowType":1,"cname":"50071140_cpr","tuId":9223372032562840000,"sellType":2,"rspFormat":1,"conBackEnv":1},"container":{"height":100,"width":850,"sizeType":1,"anchoredType":1,"floated":{}},"fillstyle":{"elements":[51],"layout":[1,2],"styleTemplateId":[60103],"txt":{"number":0},"styleType":3,"ignoreStyleMode":1},"adslottype":0,"userdefine":"%7Cadp%3D1%7Cat%3D3%7CconBW%3D1%7Ccpro%5Ftemplate%3DbaiduCustNativeAD%7Cpat%3D1%7Cpih%3D0%7Cpiw%3D0%7Cptbg%3D90%7Cptp%3D1%7Cptt%3D0%7Crss1%3D%23ffffff%7Crss2%3D%23000000%7Ctft%3D0%7CtitFF%3D%E5%BE%AE%E8%BD%AF%E9%9B%85%E9%BB%91%7CtitFS%3D12%7CtitSU%3D0%7Ctlt%3D1%7Ctn%3DbaiduCustNativeAD","encode_userdefine":"encoded","complement_type":2,"update":"1551423622_1551423622"},"extends":{"ssph":100,"sspw":850},"pdb_deliv":{"deliv_id":"0","deliv_des":{},"brandad":0},"order_deliv":{"deliv_id":"0","demand_id":"0"},"rtb_deliv":{"deliv_id":"0","demand_id":"3031513"},"media_protect":"","adExpire":1552312894111}',
                                       1],
                                      [u'u3031522_0',
                                       u'{"queryid":"9e706dbcf5ede9c7","tuid":"u3031522_0","placement":{"basic":{"sspId":1,"userId":7017965,"flowType":1,"cname":"50071140_cpr","tuId":9223372032562840000,"sellType":2,"rspFormat":1,"conBackEnv":1},"container":{"height":100,"width":850,"sizeType":1,"anchoredType":1,"floated":{}},"fillstyle":{"elements":[51],"layout":[1,2],"styleTemplateId":[60103],"txt":{"number":0},"styleType":3,"ignoreStyleMode":1},"adslottype":0,"userdefine":"%7Cadp%3D1%7Cat%3D3%7CconBW%3D1%7Ccpro%5Ftemplate%3DbaiduCustNativeAD%7Cpat%3D1%7Cpih%3D0%7Cpiw%3D0%7Cptbg%3D50%7Cptp%3D1%7Cptt%3D0%7Crss1%3D%23d2d2d2%7Crss2%3D%23000000%7Ctft%3D0%7CtitFF%3D%E5%BE%AE%E8%BD%AF%E9%9B%85%E9%BB%91%7CtitFS%3D13%7CtitSU%3D0%7Ctlt%3D1%7Ctn%3DbaiduCustNativeAD","encode_userdefine":"encoded","complement_type":2,"update":"1551061887_1500471754"},"extends":{"ssph":100,"sspw":850},"pdb_deliv":{"deliv_id":"0","deliv_des":{},"brandad":0},"order_deliv":{"deliv_id":"0","demand_id":"0"},"rtb_deliv":{"deliv_id":"0","demand_id":"3031522"},"media_protect":"","adExpire":1552312894058}',
                                       1],
                                      [u'_taxac_exp', u'1552314696367::1552399295553', 1],
                                      [u'_taxfp', u'595416160,1613793645::1583848895553', 1],
                                      [u'_taxtax_vi',
                                       u'a3e0518fc0eb86fe77379a86a65c3740|1552312895556::1552917695553',
                                       1]]},
            u'url': u'http://images.sohu.com/bill/jingzhun/2017/baidu/juxinggengxin.html#1514254036#1520323659?clkm=%2F%2Fi.go.sohu.com%2Fcount%2Fc%3Fsource%3D0%26newsid%3D%26subid%3D%26aid%3D100200308%26apid%3Dbeans_15542%26impid%3D0cec6f881091b7a8f_0_0%26mkey%3D0cec6f881091b7a8f_0_0%26freq%3D0%26ax%3D890%26ay%3D5640%26ed%3D%26bucket%3D%26ext%3De%253DPD39c0XEnZD6ZVzdR0sBla9H%252FxSKC1%252BpoMSwIxQ4plBMvtxNEqbFcxYrn6v%252FIMzYwBCpf3FvJAob11%252FKXY3wVk5LLG0wCVS2tmMSjH6R0mdTEVTTpzsikgK8ws1vKpSNaR0HI%252BRA2eyIU833HOwiI07P3uNJuR11hblIO2DT3cXiQCntq%252FC11NH9D0kV34CKJKRSnz9ZACRqKy2tjW0b%252BLg3y8x0kCkGNvbWgMmoJbueOtyr7zAvR9mZ5sCHwtLRrRyqPWYaFHHZBa06H%252BFxnJv57DPWca0B2BqOu%252FkeliDaY%252B8m%252BkbL3U81Q6z8Rv0IFwwIf5qIqfgrA4a%252BO5vCbNSAjeKFSz9dBw6plkKegoPyZeX5UqsztCUoIoj%252Fxk2uuHC9NfeKMr5SuSXJsotsi3%252BH5ZW8QA4gcmcyt3yEMER43misi9lJxLLyjeQjojZSNggXTKpjqTDSqw%252FQDXYThPRz4qR2OUFPLZRdv0uXEBzgueKLquN0Cn%252F%252BN8Wp7BuIHiFKUVVDLd4MLQjTqhHdEebApB5xAbsFhzdDdLZMFy3xT0Hwb1fVAUPQILY0nx4VomdRT5zWTT4%252FMKLQgaMsavEf9mYsHWMgZ%252B%252FvN79Ahzu5Xkg%252Bwa0XHIgz66lmhGc6dINVdr8msp%252FSuSjZsKx4mRfQ%252BkMO5KcXq5chyTcW0rk19m9qp%252F8vrOK%252FDN6mQf6EuqH92TVv3%252BO%252FZnPb6m%252BoAZz7cifNjVkkn6QAoiNHsHpiRzqG8zEJlnc6lJ8omuY%252B%2509tt2%253D1552320726091%2509turn%253D1%2509geoid1%253D1356000000%2509geoid2%253D1840000000%2509source%253Dshjtsybxpsyq%26uloc%3D%26turn%3D1%26sf%3D1%26newschn%3D1000000000%26pgid%3Dsohu-index%26shbd_monitor_ext%3Dc%26latcy%3D87%26position%3D%26at%3D1%26supplyid%3D1%26timestamp%3D1552312941905%26r%3D0.5763225532136858%26rsln%3D1024*768%26smuid%3D%26suv%3D190312001119IHW8%26pagerefer%3D%26appid%3Dpcnews',
            u'value': u'<iframe id="iframeu2989570_0" name="iframeu2989570_0"  src="http://pos.baidu.com/kcdm?conwid=300&conhei=250&rdid=2989570&dc=3&exps=110011&psi=93c5a460310299bb6bf0474f0cce84ef&di=u2989570&dri=0&dis=11&dai=1&ps=0x0&enu=encoding&dcb=___adblockplus&dtm=HTML_POST&dvi=0.0&dci=-1&dpt=none&tsr=0&tpr=1552312950884&ari=2&dbv=2&drs=1&pcs=300x250&pss=300x250&cfv=32&cpl=3&chi=6&cce=true&cec=ISO-8859-1&tlm=1512373164&rw=320&ltu=http%3A%2F%2Fwww.sohu.com%2F%3Fspm%3Dsmpc.home.top-logo.1.1552312887417trU2SnP&liu=http%3A%2F%2Fimages.sohu.com%2Fbill%2Fjingzhun%2F2017%2Fbaidu%2Fjuxinggengxin.html%231514254036%231520323659%3Fclkm%3D%252F%252Fi.go.sohu.com%252Fcount%252Fc%253Fsource%253D0%2526newsid%253D%2526subid%253D%2526aid%253D100200308%2526apid%253Dbeans_15542%2526impid%253D0cec6f881091b7a8f_0_0%2526mkey%253D0cec6f881091b7a8f_0_0%2526freq%253D0%2526ax%253D890%2526ay%253D5640%2526ed%253D%2526bucket%253D%2526ext%253De%25253DPD39c0XEnZD6ZVzdR0sBla9H%25252FxSKC1%25252BpoMSwIxQ4plBMvtxNEqbFcxYrn6v%25252FIMzYwBCpf3FvJAob11%25252FKXY3wVk5LLG0wCVS2tmMSjH6R0mdTEVTTpzsikgK8ws1vKpSNaR0HI%25252BRA2eyIU833HOwiI07P3uNJuR11hblIO2DT3cXiQCntq%25252FC11NH9D0kV34CKJKRSnz9ZACRqKy2tjW0b%25252BLg3y8x0kCkGNvbWgMmoJbueOtyr&ltr=http%3A%2F%2Fwww.sohu.com%2F%3Fspm%3Dsmpc.home.top-logo.1.1552312887417trU2SnP&ecd=1&uc=959x744&pis=300x250&sr=1024x768&tcn=1552312951&qn=9d8c87a7a6cbd356&tt=1552312950857.55.56.93&lto=http%3A%2F%2Fwww.sohu.com&ltl=1" width="300" height="250" align="center,center" vspace="0" hspace="0" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" style="border:0;vertical-align:bottom;margin:0;width:300px;height:250px" allowtransparency="true"></iframe>'}
