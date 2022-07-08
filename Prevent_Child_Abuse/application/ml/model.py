import pandas as pd
import numpy as np
import joblib
import xgboost as xgb


report_col_name = ['아동_성별_F', '아동_성별_M', '아동_생년월일_0~1세미만', '아동_생년월일_10~12세', '아동_생년월일_13~15세', '아동_생년월일_16~17세', '아동_생년월일_18~20세',
 '아동_생년월일_1~3세', '아동_생년월일_4~6세', '아동_생년월일_7~9세', '아동_내국인여부_내국인', '아동_내국인여부_무국적', '아동_내국인여부_외국인', '아동_최종학력_고등졸업', '아동_최종학력_고등중퇴',
 '아동_최종학력_대학원이상', '아동_최종학력_대학졸업', '아동_최종학력_대학중퇴', '아동_최종학력_무학', '아동_최종학력_재학중', '아동_최종학력_중등졸업', '아동_최종학력_중등중퇴', '아동_최종학력_초등졸업',
 '아동_최종학력_초등중퇴', '아동_직업유형_고등학교', '아동_직업유형_관리자', '아동_직업유형_군인', '아동_직업유형_기능원 및 관련 기능 종사자', '아동_직업유형_기술공 및 준전문가', '아동_직업유형_기타',
 '아동_직업유형_농림어업숙련종사자', '아동_직업유형_단순노무종사자', '아동_직업유형_무직', '아동_직업유형_사무종사자', '아동_직업유형_서비스 및 판매종사자', '아동_직업유형_어린이집', '아동_직업유형_유치원',
 '아동_직업유형_장치·기계조작 및 조립 종사자', '아동_직업유형_전문가', '아동_직업유형_중학교', '아동_직업유형_초등학교', '아동_거주상태_기타', '아동_거주상태_무상', '아동_거주상태_보증금(전세)+월세',
 '아동_거주상태_보호시설', '아동_거주상태_영구임대아파트  또는 영구임대주택', '아동_거주상태_월세', '아동_거주상태_자택', '아동_거주상태_전세', '아동_친권자유형_양모', '아동_친권자유형_양부',
 '아동_친권자유형_양부모', '아동_친권자유형_친권자 없음', '아동_친권자유형_친모', '아동_친권자유형_친부', '아동_친권자유형_친부모', '아동_친권자유형_후견인 없음', '아동_가족유형_기타',
 '아동_가족유형_동거(사실혼포함)', '아동_가족유형_모자가족(가출)', '아동_가족유형_모자가족(별거)', '아동_가족유형_모자가족(사별)', '아동_가족유형_모자가족(이혼)', '아동_가족유형_미혼부·모가정',
 '아동_가족유형_부자가족(가출)', '아동_가족유형_부자가족(별거)', '아동_가족유형_부자가족(사별)', '아동_가족유형_부자가족(이혼)', '아동_가족유형_소년소녀가정', '아동_가족유형_시설보호',
 '아동_가족유형_위탁가정', '아동_가족유형_입양가정', '아동_가족유형_재혼가정', '아동_가족유형_친부모가정', '아동_가족유형_친인척보호', '아동_다문화가족_다문화', '아동_다문화가족_북한이탈주민',
 '아동_다문화가족_일반', '아동_가구소득구분코_100만원이상-150만원미만', '아동_가구소득구분코_150만원이상-200만원미만', '아동_가구소득구분코_200만원이상-250만원미만', '아동_가구소득구분코_250만원이상-300만원미만',
 '아동_가구소득구분코_300만원이상', '아동_가구소득구분코_50만원미만', '아동_가구소득구분코_50만원이상~100만원미만', '아동_기초생활수급유_비수급권대상', '아동_기초생활수급유_수급권대상',
 '신고_접수경로구분코_112', '신고_접수경로구분코_119', '신고_접수경로구분코_129', '신고_접수경로구분코_1366', '신고_접수경로구분코_기타', '신고_접수경로구분코_내방', '신고_접수경로구분코_방문신고',
 '신고_접수경로구분코_상담원 인지신고', '신고_접수경로구분코_아동보호전문기관일반전화', '신고_접수경로구분코_아동행복지원', '신고_접수경로구분코_아동행복지원  상담원인지신고', '신고_접수경로구분코_아동행복지원  읍면동인지신고',
 '신고_접수경로구분코_인터넷', '신고_접수경로구분코_일반전화', '신고_접수경로구분코_타기관통보', '신고_신고자유형구분_비신고의무자', '신고_신고자유형구분_신고의무자', '신고_집단시설내사건_교육기관',
 '신고_집단시설내사건_기타', '신고_집단시설내사건_시설', '신고_집단시설내사건_어린이집', '신고_집단시설내사건_해당사항없음', '신고_재신고여부_1_없음', '신고_재신고여부_1_있음', '신고_접수유형_아동학대 의심사례',
 '신고_접수유형_일반상담', '신고_접수유형_피해아동보호명령을 통한 인지', '신고_접수유형_학대행위자 법원명령을 통한 인지(임시조치, 보호처분)', '신고_피해아동상태구_아동사망', '신고_피해아동상태구_중상해(의식불명 포함)',
 '신고_피해아동상태구_해당사항없음', '신대_행위자아동관계_계모', '신대_행위자아동관계_계부', '신대_행위자아동관계_기타', '신대_행위자아동관계_기타시설종사자', '신대_행위자아동관계_낯선사람',
 '신대_행위자아동관계_베이비시터(아이돌보미)', '신대_행위자아동관계_부모의 동거인', '신대_행위자아동관계_아동복지시설종사자', '신대_행위자아동관계_아동을 보호ㆍ양육ㆍ교육하거나 그 의무가 있는 자',
 '신대_행위자아동관계_양모', '신대_행위자아동관계_양부', '신대_행위자아동관계_어린이집(보육교직원, 종사자)', '신대_행위자아동관계_외조모', '신대_행위자아동관계_외조부', '신대_행위자아동관계_위탁모',
 '신대_행위자아동관계_위탁부', '신대_행위자아동관계_유치원(교사,교직원, 종사자)', '신대_행위자아동관계_이웃', '신대_행위자아동관계_청소년관련시설종사자', '신대_행위자아동관계_친모', '신대_행위자아동관계_친부',
 '신대_행위자아동관계_친인척', '신대_행위자아동관계_친조모', '신대_행위자아동관계_친조부', '신대_행위자아동관계_학교(교원, 교직원)', '신대_행위자아동관계_학원(강사, 종사자)', '신대_행위자아동관계_형제자매',
 '신대_아동동거여부_동거', '신대_아동동거여부_비동거', '신대_접수유형_동일신고', '신대_접수유형_아동학대 의심사례', '신대_접수유형_응급아동학대의심사례', '신대_접수유형_일반상담', '아특_신체질환및장애',
 '아특_사회성문제', '아특_사회적고립', '아특_뇌병변장애', '아특_언어문제', '아특_안면장애', '아특_신장장애', '아특_심장장애', '아특_시각장애', '아특_간장애', '아특_장루·요루장애',
 '아특_자폐성장애', '아특_충동', '아특_특성없음', '아특_대소변문제', '아특_불안', '아특_양육지식및기술', '아특_부부및가족갈등', '아특_난(難)독해', '아특_인터넷(게임)', '아특_전과력',
 '아특_학교부적응', '아특_뇌전증장애', '아특_과잉행동', '아특_낮은자아존중감', '아특_청각장애', '아특_원치않는아동', '아특_반항', '아특_폭력행동', '아특_기타', '아특_잦은병치례',
 '아특_배우자폭력', '아특_약물', '아특_무력감', '아특_비행집단활동', '아특_흡연', '아특_언어장애', '아특_오락중독', '아특_정신장애', '아특_기타장애', '아특_불건전한또래관', '아특_호흡기장애',
 '아특_경제적어려움', '아특_학습문제', '아특_거짓말', '아특_가출', '아특_존속학대', '아특_성격및기질문제', '아특_음주', '아특_장애의심', '아특_정서문제', '아특_무단결과', '아특_정신질환및장애',
 '아특_잦은결석', '아특_우울', '아특_성문제', '아특_나태(무기력)', '아특_부적절한양육태', '아특_신체발달지연', '아특_급만성질병', '아특_스트레스', '아특_애착문제', '아특_종교문제',
 '아특_주의산만', '아특_틱장애', '아특_도박_게임중독', '아특_알콜남용', '아특_공격성', '아특_지체장애', '아특_어릴적학대경험', '아특_도벽', '아특_허약', '아특_탐식및결식', '아특_늦은귀가',
 '아특_대인관계기피', '아특_위생문제', '아특_영양결핍', '아특_지적장애', '아특_난(難)작문']

reabuse_col_name = ['아동_성별_F', '아동_성별_M', '아동_생년월일_0~1세미만', '아동_생년월일_10~12세', '아동_생년월일_13~15세', '아동_생년월일_16~17세', '아동_생년월일_18~20세',
 '아동_생년월일_1~3세', '아동_생년월일_4~6세', '아동_생년월일_7~9세', '아동_내국인여부_내국인', '아동_내국인여부_무국적', '아동_내국인여부_외국인', '아동_최종학력_고등졸업', '아동_최종학력_고등중퇴',
 '아동_최종학력_무학', '아동_최종학력_재학중', '아동_최종학력_중등졸업', '아동_최종학력_중등중퇴', '아동_최종학력_초등졸업', '아동_최종학력_초등중퇴', '아동_직업유형_고등학교', '아동_직업유형_관리자',
 '아동_직업유형_기능원 및 관련 기능 종사자', '아동_직업유형_기술공 및 준전문가', '아동_직업유형_기타', '아동_직업유형_농림어업숙련종사자', '아동_직업유형_단순노무종사자', '아동_직업유형_무직',
 '아동_직업유형_사무종사자', '아동_직업유형_서비스 및 판매종사자', '아동_직업유형_어린이집', '아동_직업유형_유치원', '아동_직업유형_장치·기계조작 및 조립 종사자', '아동_직업유형_전문가',
 '아동_직업유형_중학교', '아동_직업유형_초등학교', '아동_거주상태_기타', '아동_거주상태_무상', '아동_거주상태_보증금(전세)+월세', '아동_거주상태_보호시설', '아동_거주상태_영구임대아파트  또는 영구임대주택',
 '아동_거주상태_월세', '아동_거주상태_자택', '아동_거주상태_전세', '아동_친권자유형_양모', '아동_친권자유형_양부', '아동_친권자유형_양부모', '아동_친권자유형_친권자 없음', '아동_친권자유형_친모',
 '아동_친권자유형_친부', '아동_친권자유형_친부모', '아동_친권자유형_후견인 없음', '아동_가족유형_기타', '아동_가족유형_동거(사실혼포함)', '아동_가족유형_모자가족(가출)', '아동_가족유형_모자가족(별거)',
 '아동_가족유형_모자가족(사별)', '아동_가족유형_모자가족(이혼)', '아동_가족유형_미혼부·모가정', '아동_가족유형_부자가족(가출)', '아동_가족유형_부자가족(별거)', '아동_가족유형_부자가족(사별)',
 '아동_가족유형_부자가족(이혼)', '아동_가족유형_소년소녀가정', '아동_가족유형_시설보호', '아동_가족유형_위탁가정', '아동_가족유형_입양가정', '아동_가족유형_재혼가정', '아동_가족유형_친부모가정',
 '아동_가족유형_친인척보호', '아동_다문화가족_다문화', '아동_다문화가족_북한이탈주민', '아동_다문화가족_일반', '아동_가구소득구분코_100만원이상-150만원미만', '아동_가구소득구분코_150만원이상-200만원미만',
 '아동_가구소득구분코_200만원이상-250만원미만', '아동_가구소득구분코_250만원이상-300만원미만', '아동_가구소득구분코_300만원이상', '아동_가구소득구분코_50만원미만', '아동_가구소득구분코_50만원이상~100만원미만',
 '아동_기초생활수급유_비수급권대상', '아동_기초생활수급유_수급권대상', '아동_보호조치유형_1.0', '신고_접수경로구분코_112', '신고_접수경로구분코_119', '신고_접수경로구분코_129', '신고_접수경로구분코_1366',
 '신고_접수경로구분코_기타', '신고_접수경로구분코_내방', '신고_접수경로구분코_방문신고', '신고_접수경로구분코_상담원 인지신고', '신고_접수경로구분코_아동보호전문기관일반전화', '신고_접수경로구분코_아동행복지원',
 '신고_접수경로구분코_아동행복지원  상담원인지신고', '신고_접수경로구분코_아동행복지원  읍면동인지신고', '신고_접수경로구분코_인터넷', '신고_접수경로구분코_일반전화', '신고_접수경로구분코_타기관통보',
 '신고_신고자유형구분_비신고의무자', '신고_신고자유형구분_신고의무자', '신고_집단시설내사건_교육기관', '신고_집단시설내사건_기타', '신고_집단시설내사건_시설', '신고_집단시설내사건_어린이집',
 '신고_집단시설내사건_해당사항없음', '신고_접수유형_아동학대 의심사례', '신고_접수유형_피해아동보호명령을 통한 인지', '신고_접수유형_학대행위자 법원명령을 통한 인지(임시조치, 보호처분)', '신고_신고접수구분_경찰접수',
 '신고_신고접수구분_아동보호전문기관접수', '신고_피해아동상태구_아동사망', '신고_피해아동상태구_중상해(의식불명 포함)', '신고_피해아동상태구_해당사항없음', '신대_행위자아동관계_계모',
 '신대_행위자아동관계_계부', '신대_행위자아동관계_기타', '신대_행위자아동관계_기타시설종사자', '신대_행위자아동관계_낯선사람', '신대_행위자아동관계_베이비시터(아이돌보미)', '신대_행위자아동관계_부모의 동거인',
 '신대_행위자아동관계_아동복지시설종사자', '신대_행위자아동관계_아동을 보호ㆍ양육ㆍ교육하거나 그 의무가 있는 자', '신대_행위자아동관계_양모', '신대_행위자아동관계_양부', '신대_행위자아동관계_어린이집(보육교직원, 종사자)',
 '신대_행위자아동관계_외조모', '신대_행위자아동관계_외조부', '신대_행위자아동관계_위탁모', '신대_행위자아동관계_위탁부', '신대_행위자아동관계_유치원(교사,교직원, 종사자)', '신대_행위자아동관계_이웃',
 '신대_행위자아동관계_청소년관련시설종사자', '신대_행위자아동관계_친모', '신대_행위자아동관계_친부', '신대_행위자아동관계_친인척', '신대_행위자아동관계_친조모', '신대_행위자아동관계_친조부',
 '신대_행위자아동관계_학교(교원, 교직원)', '신대_행위자아동관계_학원(강사, 종사자)', '신대_행위자아동관계_형제자매', '신대_아동동거여부_동거', '신대_아동동거여부_비동거', '신대_접수유형_동일신고',
 '신대_접수유형_아동학대 의심사례', '신대_접수유형_응급아동학대의심사례', '조사_집단시설내사건_교육기관', '조사_집단시설내사건_시설', '조사_집단시설내사건_어린이집', '조사_위험_점수_1.0',
 '조사_위험_점수_2.0', '조사_위험_점수_3.0', '조사_위험_점수_4.0', '조사_위험_점수_5.0', '조사_위험_점수_6.0', '조사_위험_점수_7.0', '조사_위험_점수_8.0', '조사_위험_점수_9.0',
 '조대_특별관리유형_가족재결합 평가도구 사용', '조대_특별관리유형_공동모금회사업', '조대_특별관리유형_아동인권지킴이단', '조대_특별관리유형_종단연구', '판단_학대발생빈도_1개월에 한번',
 '판단_학대발생빈도_1년에 한번', '판단_학대발생빈도_1주일에 한번', '판단_학대발생빈도_2-3개월에 한번', '판단_학대발생빈도_2~3일에 한번', '판단_학대발생빈도_2년에 한번', '판단_학대발생빈도_2주일에 한번',
 '판단_학대발생빈도_3년에 한번', '판단_학대발생빈도_6개월에 한번', '판단_학대발생빈도_거의 매일', '판단_학대발생빈도_일회성', 'New_Call_Count_1', 'New_Call_Count_10', 'New_Call_Count_11',
 'New_Call_Count_12', 'New_Call_Count_13', 'New_Call_Count_14', 'New_Call_Count_15', 'New_Call_Count_16', 'New_Call_Count_17', 'New_Call_Count_2',
 'New_Call_Count_3', 'New_Call_Count_4', 'New_Call_Count_5', 'New_Call_Count_6', 'New_Call_Count_7', 'New_Call_Count_8', 'New_Call_Count_9', '조사_조사완료여부',
 '조대_재신고여부_1', '조대_동일신고여부', '조대_아동동거여부', '판단_유형_신체', '판단_유형_정서', '판단_유형_성', '판단_유형_방임', '아특_공격성', '아특_거짓말', '아특_장애의심',
 '아특_배우자폭력', '아특_장루·요루장애', '아특_기타장애', '아특_나태(무기력)', '아특_언어문제', '아특_뇌전증장애', '아특_청각장애', '아특_늦은귀가', '아특_어릴적학대경험', '아특_기타',
 '아특_우울', '아특_학습문제', '아특_언어장애', '아특_성문제', '아특_부적절한양육태', '아특_호흡기장애', '아특_양육지식및기술', '아특_뇌병변장애', '아특_잦은결석', '아특_틱장애',
 '아특_인터넷(게임)', '아특_알콜남용', '아특_폭력행동', '아특_영양결핍', '아특_자폐성장애', '아특_위생문제', '아특_정신질환및장애', '아특_부부및가족갈등', '아특_대인관계기피', '아특_존속학대',
 '아특_주의산만', '아특_약물', '아특_대소변문제', '아특_안면장애', '아특_도박_게임중독', '아특_탐식및결식', '아특_난(難)독해', '아특_흡연', '아특_사회적고립', '아특_정서문제', '아특_지체장애',
 '아특_무력감', '아특_반항', '아특_심장장애', '아특_경제적어려움', '아특_학교부적응', '아특_급만성질병', '아특_불건전한또래관', '아특_잦은병치례', '아특_지적장애', '아특_신체질환및장애', '아특_과잉행동',
 '아특_애착문제', '아특_정신장애', '아특_신체발달지연', '아특_스트레스', '아특_낮은자아존중감', '아특_오락중독', '아특_신장장애', '아특_허약', '아특_음주', '아특_도벽', '아특_시각장애',
 '아특_불안', '아특_간장애', '아특_무단결과', '아특_사회성문제', '아특_종교문제', '아특_원치않는아동', '아특_비행집단활동', '아특_난(難)작문', '아특_충동', '아특_가출', '아특_전과력', '아특_특성없음',
 '아특_성격및기질문제', '아조_분리조치', '아조_원가정보호', '아조_가정복귀', '아조_사망', '아조_기타_1', '행조_고소/고발/사', '행조_모니터링', '행조_아동과의분리', '행조_사건처리만나지', '행조_만나지못함']

mydict = {"아동_성별": ['F', 'M'],
                 "아동_생년월일": ['0~1세미만', '10~12세', '13~15세', '16~17세', '18~20세', '1~3세', '4~6세', '7~9세'],
                 "아동_내국인여부": ['내국인', '무국적', '외국인'],
                 "아동_최종학력": ['고등졸업', '고등중퇴', '무학', '재학중', '중등졸업', '중등중퇴', '초등졸업', '초등중퇴'],
                 "아동_직업유형": ['고등학교','관리자','기능원 및 관련 기능 종사자','기술공 및 준전문가','기타','농림어업숙련종사자','단순노무종사자',
                                    '무직','사무종사자','서비스 및 판매종사자','어린이집','유치원','장치·기계조작 및 조립 종사자','전문가','중학교','초등학교'], 
                 "아동_거주상태": ['기타', '무상', '보증금(전세)+월세', '보호시설', '영구임대아파트  또는 영구임대주택', '월세', '자택', '전세'], 
                 "아동_친권자유형": ['양모', '양부', '양부모', '친권자 없음', '친모', '친부', '친부모', '후견인 없음'], 
                 "아동_가족유형": ['기타','동거(사실혼포함)','모자가족(가출)','모자가족(별거)','모자가족(사별)','모자가족(이혼)','미혼부·모가정',
                                     '부자가족(가출)','부자가족(별거)','부자가족(사별)','부자가족(이혼)','소년소녀가정','시설보호','위탁가정','입양가정',
                                     '재혼가정','친부모가정','친인척보호'],
                  "아동_다문화가족": ['다문화', '북한이탈주민', '일반'],
                 "아동_가구소득구분코": ['100만원이상-150만원미만','150만원이상-200만원미만','200만원이상-250만원미만','250만원이상-300만원미만',
                                         '300만원이상','50만원미만','50만원이상~100만원미만'], 
                 "아동_기초생활수급유": ['비수급권대상', '수급권대상'], 
                 "아동_보호조치유형": ['1.0'], 
                 "신고_접수경로구분코": ['112','119','129','1366','기타','내방','방문신고','상담원 인지신고',
                                         '아동보호전문기관일반전화','아동행복지원','아동행복지원  상담원인지신고','아동행복지원  읍면동인지신고',
                                         '인터넷','일반전화','타기관통보'], 
                 "신고_신고자유형구분": ['비신고의무자', '신고의무자'], 
                 "신고_집단시설내사건_": ['교육기관', '기타', '시설', '어린이집', '해당사항없음'], 
                 "신고_접수유형": ['아동학대 의심사례', '피해아동보호명령을 통한 인지', '학대행위자 법원명령을 통한 인지(임시조치, 보호처분)'], 
                 "신고_신고접수구분": ['경찰접수', '아동보호전문기관접수'], 
                 "신고_피해아동상태구": ['아동사망', '중상해(의식불명 포함)', '해당사항없음'], 
                 "신대_행위자아동관계": ['계모','계부','기타','기타시설종사자','낯선사람','베이비시터(아이돌보미)','부모의 동거인','아동복지시설종사자',
                                         '아동을 보호ㆍ양육ㆍ교육하거나 그 의무가 있는 자','양모','양부','어린이집(보육교직원, 종사자)','외조모',
                                         '외조부','위탁모','위탁부','유치원(교사,교직원, 종사자)','이웃','청소년관련시설종사자','친모',
                                         '친부','친인척','친조모','친조부','학교(교원, 교직원)','학원(강사, 종사자)','형제자매'], 
                 "신대_아동동거여부": ['동거', '비동거'], 
                 "신대_접수유형": ['동일신고', '아동학대 의심사례', '응급아동학대의심사례'], 
                 "조사_집단시설내사건": ['교육기관', '시설', '어린이집'], 
                 "조사_위험": ['점수_1.0','점수_2.0','점수_3.0','점수_4.0','점수_5.0','점수_6.0',
                                 '점수_7.0','점수_8.0','점수_9.0'], 
                 "조대_특별관리유형": ['가족재결합 평가도구 사용', '공동모금회사업', '아동인권지킴이단', '종단연구'], 
                 "판단_학대발생빈도": ['1개월에 한번','1년에 한번','1주일에 한번','2-3개월에 한번',
                                         '2~3일에 한번','2년에 한번','2주일에 한번','3년에 한번','6개월에 한번',
                                         '거의 매일','일회성'],
                 "New_Call_Count": ['1','10','11','12','13','14','15','16','17','2',
                                     '3','4','5','6','7','8','9'],
                 "조사_조사완료여부": [1,0],
                 "조대_재신고여부_1": [0,1],
                 "조대_동일신고여부": [0,1],
                 "조대_아동동거여부": [1,0],
                 "판단_유형": ['신체', '정서', '성', '방임']} 
# dict_df = pd.DataFrame({ key:pd.Series(value) for key, value in mydict.items() }) 



common_model_url = 'application/model/'

report_log_model_name = 'report_logistic_model.pkl'
report_xgb_model_name = 'report_xgb_model.pkl'
report_forest_model_name = 'report_forest_model.pkl'

report_log_clf = joblib.load(common_model_url + report_log_model_name) 
report_xgb_model = joblib.load(common_model_url + report_xgb_model_name) 
report_forest = joblib.load(common_model_url + report_forest_model_name)

log_model_name = 'logistic_model.pkl'
xgb_model_name = 'xgb_model.pkl'
forest_model_name = 'forest_model.pkl'

log_clf = joblib.load(common_model_url + log_model_name) 
xgb_model = joblib.load(common_model_url + xgb_model_name) 
forest = joblib.load(common_model_url + forest_model_name) 

percent=0

def make_dummy(input_data):
    data = [0 for i in range(len(report_col_name))]
    # 예측 데이터 컬럼과 일치하도록 데이터 리스트 생성
    for i in range(0, len(input_data)):
        for j in range (0, len(report_col_name)):
            if input_data[i] == report_col_name[j]:
                data[j] = 1

    return data

def report_expectation(input_data):
    data = []
    data = make_dummy(input_data)
    
    # Xgboost
    test1 = np.array(data) # np.array형식으로 바꾼다.
    nam = report_col_name
    
    # test를 데이터 프레임 형태로 변환
    test1 =pd.DataFrame(test1.reshape(len(test1) // len(nam), len(nam)), columns=nam)

    # 입력값의 예측값 출력
    prob1 = round(report_xgb_model.predict(test1)[0]*100,2)

    # Logistic regression
    test2 = np.array([data])
    
    report_log_clf.predict_proba(test2)[0][1]
    prob2 = round(report_log_clf.predict_proba(test2)[0][1]*100,2)
    
    # Random forest
    test3 = np.array([data])
    
    report_forest.predict_proba(test3)[0][1]
    prob3 = round(report_forest.predict_proba(test3)[0][1]*100,2)

    return round((prob1+prob2+prob3)/3.0,2)

def make_db_data_dummy(db_data):
    dict_df = pd.DataFrame({ key:pd.Series(value) for key, value in mydict.items() }) 

    Child = db_data
    Child = Child.drop(['개별사건번호', '피해아동대상자', '학대행위자대상','신대_통계거점','결과_조치결과일자','신고_접수일시'],axis=1)
    
    Child_result = Child[['아특_공격성', '아특_거짓말', '아특_장애의심',
       '아특_배우자폭력', '아특_장루요루장애', '아특_기타장애', '아특_나태무기력', '아특_언어문제',
       '아특_뇌전증장애', '아특_청각장애', '아특_늦은귀가', '아특_어릴적학대경험', '아특_기타', '아특_우울',
       '아특_학습문제', '아특_언어장애', '아특_성문제', '아특_부적절한양육태', '아특_호흡기장애', '아특_양육지식및기술',
       '아특_뇌병변장애', '아특_잦은결석', '아특_틱장애', '아특_인터넷게임', '아특_알콜남용', '아특_폭력행동',
       '아특_영양결핍', '아특_자폐성장애', '아특_위생문제', '아특_정신질환및장애', '아특_부부및가족갈등',
       '아특_대인관계기피', '아특_존속학대', '아특_주의산만', '아특_약물', '아특_대소변문제', '아특_안면장애',
       '아특_도박_게임중독', '아특_탐식및결식', '아특_난독해', '아특_흡연', '아특_사회적고립', '아특_정서문제',
       '아특_지체장애', '아특_무력감', '아특_반항', '아특_심장장애', '아특_경제적어려움', '아특_학교부적응',
       '아특_급만성질병', '아특_불건전한또래관', '아특_잦은병치례', '아특_지적장애', '아특_신체질환및장애',
       '아특_과잉행동', '아특_애착문제', '아특_정신장애', '아특_신체발달지연', '아특_스트레스', '아특_낮은자아존중감',
       '아특_오락중독', '아특_신장장애', '아특_허약', '아특_음주', '아특_도벽', '아특_시각장애', '아특_불안',
       '아특_간장애', '아특_무단결과', '아특_사회성문제', '아특_종교문제', '아특_원치않는아동', '아특_비행집단활동',
       '아특_난작문', '아특_충동', '아특_가출', '아특_전과력', '아특_특성없음', '아특_성격및기질문제',
       '아조_분리조치', '아조_원가정보호', '아조_가정복귀', '아조_사망', '아조_기타_1', '행조_고소고발사',
       '행조_모니터링', '행조_아동과의분리', '행조_사건처리만나지', '행조_만나지못함']]

    Child = Child.drop(['아특_공격성', '아특_거짓말', '아특_장애의심',
       '아특_배우자폭력', '아특_장루요루장애', '아특_기타장애', '아특_나태무기력', '아특_언어문제',
       '아특_뇌전증장애', '아특_청각장애', '아특_늦은귀가', '아특_어릴적학대경험', '아특_기타', '아특_우울',
       '아특_학습문제', '아특_언어장애', '아특_성문제', '아특_부적절한양육태', '아특_호흡기장애', '아특_양육지식및기술',
       '아특_뇌병변장애', '아특_잦은결석', '아특_틱장애', '아특_인터넷게임', '아특_알콜남용', '아특_폭력행동',
       '아특_영양결핍', '아특_자폐성장애', '아특_위생문제', '아특_정신질환및장애', '아특_부부및가족갈등',
       '아특_대인관계기피', '아특_존속학대', '아특_주의산만', '아특_약물', '아특_대소변문제', '아특_안면장애',
       '아특_도박_게임중독', '아특_탐식및결식', '아특_난독해', '아특_흡연', '아특_사회적고립', '아특_정서문제',
       '아특_지체장애', '아특_무력감', '아특_반항', '아특_심장장애', '아특_경제적어려움', '아특_학교부적응',
       '아특_급만성질병', '아특_불건전한또래관', '아특_잦은병치례', '아특_지적장애', '아특_신체질환및장애',
       '아특_과잉행동', '아특_애착문제', '아특_정신장애', '아특_신체발달지연', '아특_스트레스', '아특_낮은자아존중감',
       '아특_오락중독', '아특_신장장애', '아특_허약', '아특_음주', '아특_도벽', '아특_시각장애', '아특_불안',
       '아특_간장애', '아특_무단결과', '아특_사회성문제', '아특_종교문제', '아특_원치않는아동', '아특_비행집단활동',
       '아특_난작문', '아특_충동', '아특_가출', '아특_전과력', '아특_특성없음', '아특_성격및기질문제',
       '아조_분리조치', '아조_원가정보호', '아조_가정복귀', '아조_사망', '아조_기타_1', '행조_고소고발사',
       '행조_모니터링', '행조_아동과의분리', '행조_사건처리만나지', '행조_만나지못함'],axis = 1)

    len_dict_df = len(dict_df)
    dict_df = pd.concat([dict_df, Child], axis = 0)
    
    Child1 = Child[['조사_조사완료여부','조대_재신고여부_1','조대_동일신고여부','조대_아동동거여부','판단_유형_신체','판단_유형_정서','판단_유형_성','판단_유형_방임']]
    dict_df = dict_df.drop(['NEW_재학대혐의여부','신고_접수연도','조사_조사완료여부','조대_재신고여부_1','조대_동일신고여부','조대_아동동거여부','판단_유형_신체','판단_유형_정서','판단_유형_성','판단_유형_방임'],axis = 1)

    X = pd.get_dummies(dict_df)
    X = X.reset_index()

    X = X[len_dict_df:].reset_index()

    X = X.drop(['level_0', 'index','NEW_CALL_COUNT','판단_유형_신체','판단_유형_정서','판단_유형_성','판단_유형_방임'],axis=1)


    X = pd.concat([X,Child1,Child_result],axis = 1)
    X = X.astype(str)
    for i in X.columns:
        if (i[-1] == 'e' or i[-1] == 'n' or i[-1] == ' '):
            X = X.drop([i],axis = 1)


    X = X.astype(float)

    # for i in Child.columns:
    #     print(i)
    return X

# 재학대 예측
def model_avg(data):

    # Xgboost
    test1 = np.array(data) # np.array형식으로 바꾼다.
    nam = reabuse_col_name
    
    # test를 데이터 프레임 형태로 변환
    test1 =pd.DataFrame(test1.reshape(len(test1) // len(nam), len(nam)), columns=nam)

    # 입력값의 예측값 출력
    prob1 = round(xgb_model.predict(test1)[0]*100,2)

    # Logistic regression
    test2 = np.array([data])
    
    log_clf.predict_proba(test2)[0][1]
    prob2 = round(log_clf.predict_proba(test2)[0][1]*100,2)
    
    # Random forest
    test3 = np.array([data])
    
    forest.predict_proba(test3)[0][1]
    prob3 = round(forest.predict_proba(test3)[0][1]*100,2)

    return round((prob1+prob2+prob3)/3.0,2)
