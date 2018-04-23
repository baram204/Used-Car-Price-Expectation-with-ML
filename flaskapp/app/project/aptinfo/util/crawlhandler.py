from flask import json, Response
import urllib3, pandas as pd
from urllib.parse import urlencode



from .modelhandler import ModelHandler

md = ModelHandler

class CrawlHandler():

    def crawl_apt_list(self, bjdCodeList):
        apt_list = []
        bjdCode_list = []
        for bjdCode in bjdCodeList:
            # print(bjdCode, end=" ")
            try:
                http = urllib3.PoolManager()
                url = 'http://www.k-apt.go.kr/kaptinfo/getKaptList.do?'
                # requrl = url + "bjd_code="+str(bjdCode)
                encoded_args = urlencode({'bjd_code': str(bjdCode)})
                requrl = url + encoded_args
                # print(requrl)
                r = http.request('GET', requrl)

                res = json.loads(r.data.decode('utf-8'))['resultList']
                # print(res)
                # http://pbpython.com/pandas-list-dict.html
                # [{'KAPT_USEDATE': '199701', 'BJD_CODE': .... }, {....}]
                df = pd.DataFrame(res)

                apt_columns={"KAPT_USEDATE" : "아파트사용일",
                             "BJD_CODE" : "법정동코드",
                             "KAPT_NAME" : "아파트이름",
                             "OPEN_TERM" : "OPEN_TERM",
                             "KAPT_CODE" : "아파트코드",
                             "OCCU_FIRST_DATE" : "완공첫날",
                             "X" : "x좌표",
                             "Y" : "y좌표",
                             "ENERGY_B_COUNT" : "에너지_B_횟수",
                             "BJD_NAME" : "법정동명",}
                apt_df = df.rename(index=str, columns=apt_columns)

                if apt_df.empty:
                    pass
                else:
                    apt_list += apt_df['아파트코드'].tolist()
                    bjdCode_list += apt_df['법정동코드'].tolist()
            except Exception as e:
                print(str(e))

        return apt_list, bjdCode_list

        # for deceving server.
        # https://urllib3.readthedocs.io/en/latest/user-guide.html#request-data
        # headers = {}
        # headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        # req = urllib.request.Request(URL, data=data, headers = headers)
        # resp = urllib.request.urlopen(req)
        # respData = resp.read()
        #
        # print(respData)
        # saveFile = open('withHeaders.txt','w')
        # saveFile.write(str(respData))
        # saveFile.close()

    def crawl_apt_info(self, aptCodeList, bldCode_list):

        순서 = ["법정동코드",
              "아파트코드",
              "아파트이름",
              "마을코드",
              "법정동주소",
              "도로명주소",
              "단지분류",
              "동수",
              "세대수",
              "전용면적60이하아파트코드",
              "전용면적60이하세대수",
              "전용면적60이상85이하아파트코드",
              "전용면적60이상85이하세대수",
              "전용면적85이상135이하아파트코드",
              "전용면적85이상135이하세대수",
              "전용면적135초과아파트코드",
              "전용면적135초과세대수",
              "분양형태",
              "난방방식",
              "복도유형",
              "연면적",
              "시공사",
              "시행사",
              "관리사무소연락처",
              "관리사무소팩스",
              "홈페이지주소",
              "일반관리방식",
              "일반관리인원",
              "일반관리계약업체",
              "경비관리방식",
              "경비관리인원",
              "경비관리계약업체",
              "청소관리방식",
              "청소관리인원",
              "음식물처리방법",
              "소독관리방식",
              "연간소독횟수",
              "소독방법",
              "승강기관리형태",
              "승객용승강기",
              "화물용승강기",
              "비상승강기",
              "주차관제홈네트워크",
              "건물구조",
              "세대전기계약방식",
              "화재수신반방식",
              "지상주차장대수",
              "지하주차장대수",
              "cctv대수",
              "부대복리시설",
              "수전용량",
              "전기안전관리자법정선임여부",
              "급수방식",
              "버스정류장",
              "편의시설",
              "교육시설",
              "사용승인일",
              "주거전용면적",
              "인근지하철역",
              "인근지하철호선",
              "지하철까지시간",
              'APPL_CODE', 'APPL_PRODATE',
              'CODE_CLTIME', 'CODE_EMAINT', 'EMPTY_HO_CNT',
              'KAPTD_ECNTB', 'KAPTD_ECNTC', 'KAPTD_ECNTD', 'KAPTD_ECNTE', 'KAPTD_ECNTM',
              'KAPT_MCAREA', 'KAPT_ME1AREA', 'KAPT_ME2AREA', 'KAPT_ME3AREA', 'KAPT_ME4AREA', 'KAPT_ME5AREA', 'KAPT_MEAREA',
              'KAPT_PAREA', 'KAPT_PE1AREA', 'KAPT_PE2AREA', 'KAPT_PE3AREA', 'KAPT_PE4AREA', 'KAPT_PE5AREA', 'KAPT_PEAREA', 'KAPT_PHAREA', 'KAPT_PPAREA',
              'KAPT_MHAREA', 'KAPT_MPAREA',
              'SETDAY_TEMP_XLS_YN', 'SETDAY_TEMP_YN',
              ]
        aptinfo_list_df = pd.DataFrame(data=None, columns=순서)

        cnt = 0
        # https://stackoverflow.com/a/47189816
        for aptCode, bjdCode in zip(aptCodeList, bldCode_list):
            try:
                http = urllib3.PoolManager()
                url = 'http://www.k-apt.go.kr/kaptinfo/getKaptInfo_detail.do?'
                # requrl = url + "bjd_code="+str(bjdCode)

                encoded_args = urlencode({'kapt_code': str(aptCode)})
                requrl = url + encoded_args
                # print(requrl)
                r = http.request('GET', requrl)
                # res =json.loads(r.data.decode('utf-8'))

                매치정보 = json.loads(r.data.decode('utf-8'))['resultMap_match']
                세부정보 = json.loads(r.data.decode('utf-8'))['resultMap_kapt']
                세대정보 = json.loads(r.data.decode('utf-8'))['resultMap_kapt_areacnt']
                주소정보 = json.loads(r.data.decode('utf-8'))['resultMap_kapt_addrList']

                매치이름 ={
                    "KAPT_CODE" : "아파트코드",
                    "TOWN_CODE" : "마을코드"
                }

                세부이름={
                    "KAPT_NAME" : "아파트이름",
                    "CODE_SALE" : "분양형태",
                    "CODE_HEAT" : "난방방식",
                    "KAPT_TAREA" : "연면적",
                    "KAPT_DONG_CNT" : "동수",
                    "KAPT_BCOMPANY" : "시공사",
                    "KAPT_ACOMPANY" : "시행사",
                    "KAPT_TEL" : "관리사무소연락처",
                    "KAPT_FAX" : "관리사무소팩스",
                    "KAPT_URL" : "홈페이지주소",
                    "CODE_APT" : "단지분류",

                    "CODE_MGR" : "일반관리방식",
                    "KAPT_MGR_CNT" : "일반관리인원",
                    "KAPT_CCOMPANY" : "일반관리계약업체",

                    "CODE_SEC" : "경비관리방식",
                    "KAPTD_SCNT" : "경비관리인원",
                    "KAPTD_SEC_COM" : "경비관리계약업체",

                    "CODE_CLEAN" : "청소관리방식",
                    "KAPTD_CLCNT" : "청소관리인원",
                    "CODE_GARBAGE" : "음식물처리방법",

                    "CODE_DISINF" : "소독관리방식",
                    "KAPTD_DCNT" : "연간소독횟수",
                    "DISPOSAL_TYPE" : "소독방법",

                    "KAPTD_PCNT" : "지상주차장대수",
                    "KAPTD_PCNTU" : "지하주차장대수",

                    "KAPTD_CCCNT" : "cctv대수",
                    "WELFARE_FACILITY" : "부대복리시설",
                    "KAPTD_ECAPA" : "수전용량",
                    "CODE_EMGR" : "전기안전관리자법정선임여부",
                    "CODE_WSUPPLY" : "급수방식",

                    "CODE_STR" : "건물구조",
                    "CODE_ECON" : "세대전기계약방식",
                    "CODE_FALARM" : "화재수신반방식",

                    "CODE_ELEV" : "승강기관리형태",
                    "KAPTD_ECNTP" : "승객용승강기",
                    "KAPTD_PCNT" : "화물용승강기",
                    "KAPTD_DCNT" : "비상승강기",

                    "CODE_NET" : "주차관제홈네트워크",

                    "KAPTD_WTIMEBUS" : "버스정류장",
                    "CONVENIENT_FACILITY" : "편의시설",
                    "EDUCATION_FACILITY" : "교육시설",

                    "CODE_HALL" : "복도유형",
                    "KAPT_USEDATE" : "사용승인일",
                    "KAPT_MAREA" : "주거전용면적",

                    "SUBWAY_STATION" : "인근지하철역",
                    "SUBWAY_LINE" : "인근지하철호선",
                    "KAPTD_WTIMESUB" : "지하철까지시간",
                    "KAPT_CODE" : "아파트코드",
                      }


                세대1이름={
                    "KAPT_CODE" : "전용면적60이하아파트코드",
                    "KAPTDA_CNT": "전용면적60이하세대수",
                 }
                세대2이름={
                    "KAPT_CODE" :"전용면적60이상85이하아파트코드",
                    "KAPTDA_CNT": "전용면적60이상85이하세대수"
                }
                세대3이름={
                    "KAPT_CODE" :"전용면적85이상135이하아파트코드",
                    "KAPTDA_CNT": "전용면적85이상135이하세대수"
                }
                세대4이름={
                    "KAPT_CODE" :"전용면적135초과아파트코드",
                    "KAPTDA_CNT": "전용면적135초과세대수"
                }

                법정동주소 ={"ADDR" : "법정동주소" }
                도로명주소 = {"ADDR" : "도로명주소"}

                # “Normalize” semi-structured JSON data into a flat table
                # string or list of strings,
                # http://pandas.pydata.org/pandas-docs/stable/generated/pandas.io.json.json_normalize.html
                # https://stackoverflow.com/a/40100205
                from pandas.io.json import json_normalize
                매치정보_df = json_normalize(매치정보).rename(index=str, columns=매치이름)
                세부정보_df = json_normalize(세부정보).rename(index=str, columns=세부이름).\
                    drop(["아파트코드"], axis=1)
                세대_1 = json_normalize(세대정보[0]).drop(['AREA_GBN'], axis=1).rename(index=str, columns=세대1이름)
                세대_2 = json_normalize(세대정보[1]).drop(['AREA_GBN'], axis=1).rename(index=str, columns=세대2이름)
                세대_3 = json_normalize(세대정보[2]).drop(['AREA_GBN'], axis=1).rename(index=str, columns=세대3이름)
                세대_4 = json_normalize(세대정보[3]).drop(['AREA_GBN'], axis=1).rename(index=str, columns=세대4이름)
                세대수1=세대_1.get_value(0, 0, takeable=True)
                세대수2=세대_2.get_value(0, 0, takeable=True)
                세대수3=세대_3.get_value(0, 0, takeable=True)
                세대수4=세대_4.get_value(0, 0, takeable=True)
                세대list = [세대수1,세대수2,세대수3,세대수4]
                nlist = list(map(lambda x : 0 if  x is None else x ,세대list))
                number =0
                for n in nlist:
                    number +=n

                세대정보_df = pd.concat([세대_1, 세대_2, 세대_3, 세대_4], axis=1).\
                    assign(세대수=lambda x: number)


                주소 = json_normalize(주소정보)
                if len(주소.index) is 4:
                    구주소 = json_normalize(주소정보[0]).drop(['ADDR_GBN', 'KAPT_CODE'], axis=1).\
                        rename(index=str, columns=법정동주소)
                    신주소 = json_normalize(주소정보[2]).drop(['ADDR_GBN', 'KAPT_CODE'], axis=1).\
                        rename(index=str,columns=도로명주소)
                if len(주소.index) is 2:
                    구주소 = json_normalize(주소정보[0]).drop(['ADDR_GBN', 'KAPT_CODE'], axis=1).\
                        rename(index=str, columns=법정동주소)
                    신주소 = json_normalize(주소정보[1]).drop(['ADDR_GBN', 'KAPT_CODE'], axis=1).\
                        rename(index=str, columns=도로명주소)

                주소정보_df = pd.concat([구주소, 신주소], axis=1)



                apt_info_df = pd.concat([매치정보_df, 세부정보_df, 세대정보_df, 주소정보_df], axis=1).assign(법정동코드=lambda x: bjdCode)\
                    .reindex(columns=순서)

                frames = [aptinfo_list_df, apt_info_df]

                aptinfo_list_df = pd.concat(frames)
                # for deceving server.
                # https://urllib3.readthedocs.io/en/latest/user-guide.html#request-data
                # headers = {}
                # headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
                # req = urllib.request.Request(URL, data=data, headers = headers)
                # resp = urllib.request.urlopen(req)
                # respData = resp.read()
                #
                # print(respData)
                # saveFile = open('withHeaders.txt','w')
                # saveFile.write(str(respData))
                # saveFile.close()
            except Exception as e:
                print(str(e))

            #
            # # print(apt_info_df)
            # if cnt == 0:
            #     aptinfo_list_df = apt_info_df
            #
            #     cnt += 1
            # else:
            #     frames = [aptinfo_list_df, apt_info_df]
            #
            #     aptinfo_list_df = pd.concat(frames)
            #     cnt += 1

        return aptinfo_list_df
