import requests
import json

API_URL = ''


def getPdfpath(data):
    try:
        response = requests.post(API_URL, data=data,
                             headers={"Content-Type": "application/x-www-form-urlencoded","Cookie":""})
        if response.status_code == 200:
            data = response.text
            # JSON 변환
            try:
                # eval을 통해 파이썬의 딕셔너리로 먼저 처리
                dict_string = data.replace("{", "").replace("}", "")
                dict_string = dict_string.split(", ")
                dict_data = {}
                for item in dict_string:
                    if "=" in item:
                        key, value = item.split("=")
                        dict_data[key] = value
                    else:
                        key = item.split("=")[0]
                        dict_data[key] = None
                # 딕셔너리를 JSON으로 변환
                json_string = json.dumps(dict_data, ensure_ascii=False)
                return json.loads(json_string)
            except Exception as e:
                print("JSON 변환에 실패했습니다:", e)
        else:
            print(response.status_code)
    except Exception as e:
        print("JSON 변환에 실패했습니다:", e)
