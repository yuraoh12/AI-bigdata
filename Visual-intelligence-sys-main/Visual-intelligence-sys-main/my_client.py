import requests, json
import cv2
from collections import OrderedDict
import time
import send_mod

params = {
    'save_txt': 'T' }
url = 'http://127.0.0.1:5000/predict' # 분석서버 타겟 설정 
file_path = './temp.jpg'
data = OrderedDict() # dict 객체 생성

cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, color_frame = cap.read()
    cv2.imwrite('temp.jpg', color_frame)
    if ret:
        time.sleep(1)
        with open(file_path, "rb") as f:
            response = requests.post(url, files={"myfile" : f}, data=params, verify=False)
            print(response.content)
        res = response.json()
        ### 분석끝 ###
        data['name'] = res['results'][0]['name']
        data['class'] = res['results'][0]['class']
        data['conf'] = res['results'][0]['confidence']
        data['x1'] = res['results'][0]['box']['x1']
        data['y1'] = res['results'][0]['box']['y1']
        data['x2'] = res['results'][0]['box']['x2']
        data['y2'] = res['results'][0]['box']['x2']
        #print(data, type(data))
        json_data = json.dumps(data, indent=3)
        #print(json_data, type(json_data))

        last_data = OrderedDict()
        last_data['channel_id'] = send_mod.channel_id()
        last_data['metaInfo'] = data 
        last_data['req_id'] = send_mod.req_id()
        last_data['req_time'] = send_mod.req_time()
        last_data['res_time'] = send_mod.req_time()
        last_data['server_id'] = send_mod.server_id()
        last_data['req_image'] = send_mod.req_image('temp.jpg')
        temp = json.dumps(last_data)
        with open('base64.txt', 'w') as fd:
            fd.write(temp)
        print(last_data)
        last_json_data = json.dumps(last_data, indent=2)
        last_url = 'http://42.29.8.133:12080/kepco/ml_recv'
        response = requests.post(last_url, data=last_json_data)
        print(response.content)

    else:
        break   
cap.release()
cv2.destroyAllWindows()
