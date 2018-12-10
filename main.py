from flask import Flask, render_template,jsonify, request, redirect
import json
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import os
import random

app=Flask(__name__)
print("Flask Start")

keydata={"type":"buttons","buttons":["응원의 편지","무료급식정보", "편의시설", "취업/일자리", "여가정보","소개"]}
jsonkey=json.dumps(keydata,indent=2,ensure_ascii=False)

@app.route("/")
def main():
    return render_template('permisson_error.html')

@app.route('/keyboard')
def keyboard():
    return jsonkey

@app.route('/message',methods=['POST'])
def message():
    dataRecieve=request.get_json()
    content=dataRecieve['content']
    recognize=dataRecieve['user_key']

    if content==u"소개":
        datasend= {
            "message":{
                "text":"안녕하세요 컴인봇입니다!\n컴인봇은 노숙인의 기본적 인권 보장 및 자립을 돕기 위해 만들어진 채팅봇으로, 아래와 같은 정보를 제공합니다."
                       "\n-상담원 연결\n- 무료급식정보\n- 편의시설\n- 취업/일자리\n- 여가정보\n"
                       "\n저희 컴인봇으로 노숙인 여러분의 생활에 조금이나마 도움이 되었으면 좋겠습니다."
                       "\n - Outside The Lines, 2018 임팩터톤 6조 -"
            },
            "keyboard":
                {
                    "type":"buttons","buttons":["응원의 편지","무료급식정보", "편의시설", "취업/일자리", "여가정보","소개"]
                }
        }

    elif content==u"무료급식정보":
        datasend={
            "message":{
                "text":"어떤 구의 급식소 정보를 원하시나요?(현재는 강북구만 제공이 됩니다.)"
            },
            "keyboard":
                {
                    "type":"buttons", "buttons":["강북구"]
                }
        }

    elif content==u"편의시설":
        datasend = {
            "message": {
                "text": "원하시는 편리시설의 유형을 선택해주세요!"
            },
            "keyboard":
                {
                    "type": "buttons", "buttons": ["상담보호센터", "상담소", "중간쉼터", "쉼터"]
                }
        }

    elif content==u"취업/일자리":
        datasend = {
            "message": {
                "text": "어떤 종류의 일자리를 원하시나요?"
            },
            "keyboard":
                {
                    "type": "buttons", "buttons": ["민간일자리", "공공일자리"]
                }
        }

    elif content==u"여가정보":
        url = 'https://blog.naver.com/PostList.nhn?blogId=gonggangil'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        title = soup.find_all('span', {'class': 'pcol1 itemSubjectBoldfont'})
        titles=""
        num=0
        for i in title:
            titles=titles+"["+str(num+1)+"] "+title[num].text+"\n"
            num+=1
        titles=titles+"\n해당정보는 문화카페 길에서 가져온 정보로, 참여 및 문의는 https://blog.naver.com/PostList.nhn?blogId=gonggangil 로 해주세요!"

        datasend = {
            "message": {
                "text": titles
            },
            "keyboard":
                {
                    "type": "buttons", "buttons": ["응원의 편지","무료급식정보", "편의시설", "취업/일자리", "여가정보","소개"]
                }
        }

    elif content==u'응원의 편지':
        datasend={
            "message":{
                "text": "응원의 편지는 힘든 상황을 함께 버티어내고 다시 일어설 수 있도록"
                        "서로 응원하는 메시지입니다. 응원을 받고 싶으신 분은 편지받기를, 응원을"
                        "하고 싶으신 분은 편지쓰기를 눌러주세요."
                        "\n(욕설, 비방, 명예훼손 및 의도에 맞지 않는 내용은 민/형사상의 책임을"
                        "질 수 있습니다.)"
            },
            "keyboard":
                {
                    "type": "buttons",
                    "buttons": ['편지쓰기','편지받기']
                }
        }
    elif content==u'/취소':
        datasend={
            "message":{
                "text": "응원의 편지 작성을 취소하셨습니다.",
            },
            "keyboard":
                {
                    "type": "buttons", "buttons": ["응원의 편지", "무료급식정보", "편의시설", "취업/일자리", "여가정보", "소개"]
                }
        }

#-----------------------------------(여기서부터 2nd)
    elif content==u"강북구":
        url="http://openapi.seoul.go.kr:8088/6d4b4f69576c756b333544584a7942/xml/GbFreeMealOrgan/1/1000/"
        req = requests.get(url)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')

        name=soup.find_all('fac_nm')
        addr=soup.find_all('addr')
        tel=soup.find_all('tel')
        num=0
        freefood=""
        for i in name:
            freefood=freefood+name[num].text+"\n"+"서울특별시 강북구 "+addr[num].text+"\n"+tel[num].text+"\n\n"
            num+=1

        datasend = {
            "message": {
                "text": freefood
            },
            "keyboard":
                {
                    "type": "buttons", "buttons": ["응원의 편지","무료급식정보", "편의시설", "취업/일자리", "여가정보","소개"]
                }
        }

    elif content==u"상담보호센터":
        datasend = {
            "message": {
                "text": "▶ 다시서기\n→ ​주소 : 용산구 한강대로92길 6 (갈월동 14-30)\n→ ​연락처 : 02-777-5217\n\n"
                        "▶ 만나샘\n→ ​주소 : 용산구 후암로57길 45 (동자동 35-80)\n→ ​연락처 : 02-757-7598\n\n"
                        "▶ 구세군브릿지센터\n→ ​주소 : 서대문구 서소문로 57-1 (합동 13-0)\n→ ​연락처 : 02-363-9199\n\n"
                        "▶ 햇살보금자리\n→ ​주소 : 영등포구 국회대로54길 41-16 (영등포2가 28-150)\n→ ​연락처 : 02-2636-8182​\n\n"
                        "▶ 옹달샘​\n→ ​주소 : 영등포구 경인로94길 6 (문래동1가 13) 2층\n→ ​연락처 : 02-2068-9113​"
            },
            "keyboard":
                {
                    "type": "buttons", "buttons": ["응원의 편지","무료급식정보", "편의시설", "취업/일자리", "여가정보","소개"]
                }
        }

    elif content==u"상담소":
        datasend = {
            "message": {
                "text": "▶ 서울시 희망지원센터\n→ ​주소 : 서울시 중구 청파로 426 (봉래동2가 122) 파출소앞\n→ ​연락처 : 02-777-0564 / 02-365-0386\n\n"
                        "▶ 영등포역​\n ​주소 : 영등포역에 위치\n→ ​연락처 : 02-2676-3727\n\n"
            },
            "keyboard":
                {
                    "type": "buttons", "buttons": ["응원의 편지","무료급식정보", "편의시설", "취업/일자리", "여가정보","소개"]
                }
        }

    elif content==u"중간쉼터":
        datasend = {
            "message": {
                "text": "▶ 보현의집\n→ ​주소 : 영등포구 버드나루로 24 (영등포2가 94-31) 2층\n→ ​연락처 : 02-2069-1600­∼4"
            },
            "keyboard":
                {
                    "type": "buttons", "buttons": ["응원의 편지","무료급식정보", "편의시설", "취업/일자리", "여가정보","소개"]
                }
        }

    elif content==u"쉼터":
        datasend = {
            "message": {
                "text": "쉼터를 선택하셨습니다. 지역을 선택해주세요."
            },
            "keyboard":
                {
                    "type": "buttons", "buttons": ["쉼터-강동구", "쉼터-강북구", "쉼터-관악구","쉼터-구로구", "쉼터-금천구", "쉼터-은평구", "쉼터-성동구", "쉼터-영등포구", "쉼터-종로구", "쉼터-종로구", "쉼터-중랑구"]
                }
        }



    elif content==u"쉼터-강동구":
        datasend = {
            "message": {
                "text": "\n▶강동복지관쉼터\n→​주소:강동구진황도로23길7(천호동555)\n→​연락처:02-2041-7851\n"
            },
            "keyboard":
                {
                    "type": "buttons", "buttons": ["응원의 편지","무료급식정보", "편의시설", "취업/일자리", "여가정보","소개"]
                }
        }

    elif content==u"쉼터-강북구":
        datasend = {
            "message": {
                "text": "▶그리스도의공동체,겨자씨들의둥지\n→​주소:강북구수유로21길10(수유3동1-50)\n→​연락처:​02-999-3932\n"
            },
            "keyboard":
                {
                    "type": "buttons", "buttons": ["응원의 편지","무료급식정보", "편의시설", "취업/일자리", "여가정보","소개"]
                }
        }

    elif content==u"쉼터-관악구":
        datasend = {
            "message": {
                "text": "▶대한성공회살림터\n→​주소:관악구국회단지길67(봉천동635-665)\n→​연락처:​02-875-3474\n※자녀만있으면입소가능(나이제한없음),한부모가정(부자.모자가정입소가능)\n"
            },
            "keyboard":
                {
                    "type": "buttons", "buttons": ["응원의 편지","무료급식정보", "편의시설", "취업/일자리", "여가정보","소개"]
                }
        }

    elif content==u"쉼터-구로구":
        datasend = {
            "message": {
                "text": "▶구로노인복지관\n→​주소:구로구새말로16길7(구로동25-1)\n→​연락처:​02-838-4600\n▶길가온혜명\n→​주소:구로구오리로22나길14(궁동142-2)\n→​연락처:​02-891-5732\n"
            },
            "keyboard":
                {
                    "type": "buttons", "buttons": ["응원의 편지","무료급식정보", "편의시설", "취업/일자리", "여가정보","소개"]
                }
        }

    elif content==u"쉼터-금천구":
        datasend = {
            "message": {
                "text": "▶혜명노인센터\n→​주소:금천구금하로29길36(시흥동241-7)\n→​연락처:​02-891-5732\n※60세이상의노인노숙인\n▶청담복지관광명의집\n→​주소:금천구금하로29길36(시흥동241-7)\n→​연락처:02-806-1377\n"
            },
            "keyboard":
                {
                    "type": "buttons", "buttons": ["응원의 편지","무료급식정보", "편의시설", "취업/일자리", "여가정보","소개"]
                }
        }

    elif content==u"쉼터-은평구":
        datasend = {
            "message": {
                "text": "▶천애원희망의집\n→​주소:은평구녹번로7-7(녹번동82-17)\n→​연락처:​02-952-4564\n※일반노숙인입소불가,장애인남성쉼터\n▶흰돌회\n→​주소:은평구가좌로7가길12(응암동731-17)\n→​연락처:​​​02-372-5905\n※노숙인모자가정(자녀나이제한:남아12살미만,여아18살미만)자활쉼터이므로어머니가근로자여야입소할수있음\n▶인덕희망의집\n→​주소:은평구통일로75길6-8(대조동187-30)\n→​연락처:​​​02-387-8834\n▶은평복지관쉼터\n→​주소:은평구가좌로11길5-14(신사동231-5)\n→​연락처:​​​02-307-1181\n▶사랑의집\n→​주소:지방소재\n→​연락처:​​​031-829-8291\n"
            },
            "keyboard":
                {
                    "type": "buttons", "buttons": ["응원의 편지","무료급식정보", "편의시설", "취업/일자리", "여가정보","소개"]
                }
        }

    elif content==u"쉼터-동대문구/서대문구":
        datasend = {
            "message": {
                "text": "▶가나안쉼터\n→​주소:동대문구답십리로3길18(전농동620-46)\n→​연락처:​02-964-1558\n※남성노숙인쉼터\n▶다일작은천국\n→​주소:동대문구서울시립대로57(전농동497-77)\n→​연락처:​02-2213-8004\n▶서대문사랑방\n→​주소:서대문구경기대로81(충정로2가43)\n→​연락처:​02-312-7225\n▶열린여성센터\n→​주소:서대문구홍제내2길66-10(홍제동334-70)\n→​연락처:​02-704-5395\n▶일죽쉼터\n→​주소:서대문구명지대1다길2(남가좌동5-23)\n→​연락처:070-4355-2030​​​\n"
            },
            "keyboard":
                {
                    "type": "buttons", "buttons": ["응원의 편지","무료급식정보", "편의시설", "취업/일자리", "여가정보","소개"]
                }
        }

    elif content==u"쉼터-성동구":
        datasend = {
            "message": {
                "text": "▶비전트레이닝센터\n→​주소:성동구자동차시장길48(용답동250-1)\n→​연락처:​02-2243-9183\n※장기노숙쉼터로알콜,정신질환자등의재활치료가능\n▶게스트하우스\n→​주소:성동구가람길125(송정동73-36)\n→​연락처:​02-2215-9251\n※시립노숙인쉼터\n▶성수삼일내일의집\n→​주소:성동구성덕정길101-1(성수2가339-88)\n→​연락처:​02-497-6333\n※노숙인모자가정(나이제한:남자아이15살미만)\n"
            },
            "keyboard":
                {
                    "type": "buttons", "buttons": ["응원의 편지","무료급식정보", "편의시설", "취업/일자리", "여가정보","소개"]
                }
        }

    elif content==u"쉼터-성북구":
        datasend = {
            "message": {
                "text": "▶아침을여는집\n→​주소:성북구보문로137(보문동2가49)\n→​연락처:​02-924-1010\n▶십자가선교회\n→​주소:성북구정릉로6가길24-1(정릉동955-11)\n→​연락처:​02-941-2503\n▶정릉복지관쉼터\n→​주소:성북구솔샘로5길92(정릉동산293)\n→​연락처:​02-909-0434\n▶장위복지관쉼터\n→​주소:성북구한천로89길18(장위동107-5)\n→​연락처:​​​02-916-5064\n▶아가페의집\n→​주소:성북구오패산로21(하월곡동96-113)\n→​연락처:​​​02-942-9193\n※여성노숙인쉼터\n"
            },
            "keyboard":
                {
                    "type": "buttons", "buttons": ["응원의 편지","무료급식정보", "편의시설", "취업/일자리", "여가정보","소개"]
                }
        }

    elif content==u"쉼터-영등포구":
        datasend = {
            "message": {
                "text": "▶광야홈리스센터\n→​주소:영등포구경인로100길3(영등포동423-37)\n→​연락처:​​​02-2636-3373\n▶행복한우리집\n→​주소:영등포구국회대로54길37-6(영등포동29-74)\n→​연락처:​​​02-2675-4379\n▶두레사랑의쉼터\n→​주소:영등포구버드나루로14가길14(당산동121-156)\n→​연락처:​​​02-2677-5281\n▶영등포보현의집\n→​주소:영등포구버드나루로24(영등포2가94-31)2층\n→​연락처:​​​02-2069-1600\n▶중간쉼터(남자쉼터)\n→​주소:영등포구버드나루로24(영등포2가94-31)1층\n→​연락처:​​​02-2069-1600\n"
            },
            "keyboard":
                {
                    "type": "buttons", "buttons": ["응원의 편지","무료급식정보", "편의시설", "취업/일자리", "여가정보","소개"]
                }
        }

    elif content==u"쉼터-종로구":
        datasend = {
            "message": {
                "text": "▶수송보현의집\n→​주소:종로구율곡로18(수송동31-1)\n→​연락처:​​​02-737-4894\n※만18세이상∼만65세미만성인남성노숙인\n"
            },
            "keyboard":
                {
                    "type": "buttons", "buttons": ["응원의 편지","무료급식정보", "편의시설", "취업/일자리", "여가정보","소개"]
                }
        }

    elif content==u"쉼터-중구":
        datasend = {
            "message": {
                "text": "▶화엄동산\n→​주소:중구동호로17길75(신당동825-6)\n→​연락처:​​​02-2642-1363\n※여성노숙인쉼터\n"
            },
            "keyboard":
                {
                    "type": "buttons", "buttons": ["응원의 편지","무료급식정보", "편의시설", "취업/일자리", "여가정보","소개"]
                }
        }

    elif content==u"쉼터-중랑구":
        datasend = {
            "message": {
                "text": "▶신내복지관쉼터\n→​주소:중랑구봉화산로153(상봉동481)\n→​연락처:​​​02-3421-2707\n"
            },
            "keyboard":
                {
                    "type": "buttons", "buttons": ["응원의 편지","무료급식정보", "편의시설", "취업/일자리", "여가정보","소개"]
                }
        }

    elif content==u"쉼터":
        datasend = {
            "message": {
                "text": "쉼터를 선택하셨습니다. 지역을 선택해주세요."
            },
            "keyboard":
                {
                    "type": "buttons", "buttons": ["쉼터-강동구", "쉼터-강북구", "쉼터-관악구","쉼터-구로구", "쉼터-금천구", "쉼터-은평구", "쉼터-성동구", "쉼터-영등포구", "쉼터-영등포구", "쉼터-종로구", "쉼터-종로구", "쉼터-중랑구"]
                }
        }


    elif content == u"공공일자리":
        url = 'http://m.cafe.daum.net/bridge9199/cLZb'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find_all('span', {'class': 'txt_detail'})
        titles = ""
        num = 0
        for i in title:
            titles = titles + "[" + str(num + 1) + "] " + title[num].text + "\n"
            num += 1
        titles = titles + "\n해당정보는 서울노숙인일자리지원센터에서 가져온 정보로, 참여 및 문의는 http://cafe.daum.net/bridge9199/cLZb 로 해주세요!"
        datasend = {
            "message": {
                "text": titles
            },
            "keyboard":
                {
                    "type": "buttons", "buttons": ["응원의 편지","무료급식정보", "편의시설", "취업/일자리", "여가정보","소개"]
                }
        }

    elif content==u"민간일자리":
        url = 'http://m.cafe.daum.net/bridge9199/cHcA'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find_all('span', {'class': 'txt_detail'})

        titles = ""
        num = 0
        for i in title:
            titles = titles + "[" + str(num + 1) + "] " + title[num].text + "\n"
            num += 1
        titles = titles + "\n해당정보는 서울노숙인일자리지원센터에서 가져온 정보로, 참여 및 문의는 http://cafe.daum.net/bridge9199/cHcA 로 해주세요!"
        datasend = {
            "message": {
                "text": titles
            },
            "keyboard":
                {
                    "type": "buttons", "buttons": ["응원의 편지","무료급식정보", "편의시설", "취업/일자리", "여가정보","소개"]
                }
        }

    elif content== u'편지쓰기':
        datasend={
            "message": {
                "text": "편지쓰기를 선택하셨습니다."
                        "\n잠시 어려운 상황에 빠진 분들께"
                        "다시 일어날 수 있도록 편지를 작성해주세요!"
                        "\n취소하고 싶으신 경우 /취소 라고 입력해주세요(500자 내)"
            }
        }

    elif content==u'편지받기':
        path_dir='./letters'
        file_list=os.listdir(path_dir)
        endoflist=len(file_list)
        randomfile=random.randint(0,endoflist-1)

        with open('./letters/'+file_list[randomfile]) as j:
            dictdata=json.load(j)
            code=dictdata['code']
            letter=dictdata['letter']

        datasend = {
            "message": {
                "text": code+' 님의 편지입니다.'
                        '\n----------------'
                        '\n'+letter+
                        '\n----------------\n'
                        '욕설, 비방, 명예훼손 및 의도에 맞지 않는 내용일 경우 상담원을 통해 '
                        '편지 내용과 작성자를 알려주시면 조치해드리겠습니다.'
                        '(해당 편지를 복사해서 상담원에게 보내주세요.)'
            },
            "keyboard":
                {
                    "type": "buttons", "buttons": ["응원의 편지", "무료급식정보", "편의시설", "취업/일자리", "여가정보", "소개"]
                }
        }


    
    else:
        letter=content
        today=str(datetime.now())
        filename = recognize + today
        length=len(letter)

        if length<=500 and length>0:
            newletter={
                "recognize":recognize,
                "letter": letter,
                "written_date": str(today),
                "code": filename
            }
            jsonletter=json.dumps(newletter, indent=2, ensure_ascii=False)

            f=open('./letters/'+filename+'.json','w')
            f.write(jsonletter)
            f.close()

            datasend = {
                "message": {
                    "text": letter+"\n\n내용의 편지가 등록되었습니다. 서로 함께 힘내요! 감사합니다."
                },
                "keyboard":
                    {
                        "type": "buttons", "buttons": ["응원의 편지","무료급식정보", "편의시설", "취업/일자리", "여가정보","소개"]
                    }
            }
        else:
            datasend = {
                "message":{
                    "text": "500자를 넘기셨습니다."
                            "\nOverflow Error"
                },
                "keyboard":
                    {
                        "type": "buttons", "buttons": ["응원의 편지", "무료급식정보", "편의시설", "취업/일자리", "여가정보", "소개"]
                    }
            }


    return jsonify(datasend)

if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)