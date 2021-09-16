# -*- coding: UTF-8 -*-
import requests as req
import json
import os
from base64 import b64encode
from nacl import encoding, public

app_num=os.getenv('APP_NUM')
if app_num == '':
    app_num='1'
drone_server=os.getenv('DRONE_SERVER')
drone_token=os.getenv('DRONE_TOKEN')
drone_repo=os.getenv('DRONE_REPO')
#ms_token=os.getenv('MS_TOKEN')
#client_id=os.getenv('CLIENT_ID')
#client_secret=os.getenv('CLIENT_SECRET')
Auth=r'Bearer '+drone_token
#geturl=drone_server+r'/api/repos/'+drone_repo+r'/secrets/public-key'
#puturl=rdrone_server+r'/api/repos/'+drone_repo+r'/secrets/MS_TOKEN'

#微软refresh_token获取
def getmstoken(ms_token,appnum):
    headers={'Content-Type':'application/x-www-form-urlencoded'
            }
    data={'grant_type': 'refresh_token',
          'refresh_token': ms_token,
          'client_id':client_id,
          'client_secret':client_secret,
          'redirect_uri':'http://localhost:53682/'
         }
    html = req.post('https://login.microsoftonline.com/common/oauth2/v2.0/token',data=data,headers=headers)
    jsontxt = json.loads(html.text)
    if 'refresh_token' in jsontxt:
        print(r'账号/应用 '+str(appnum)+' 的微软密钥获取成功')
    else:
        print(r'账号/应用 '+str(appnum)+' 的微软密钥获取失败'+'\n'+'请检查secret里 CLIENT_ID , CLIENT_SECRET , MS_TOKEN 格式与内容是否正确，然后重新设置')
    refresh_token = jsontxt['refresh_token']
    access_token = jsontxt['access_token']
    return refresh_token
#是否要保存access，以降低微软token刷新率???

#token上传
def setsecret(mstoken,puturl,appnum):
    headers={'Accept': 'application/vnd.github.v3+json','Authorization': Auth}
    data_str=r'{"data": "'+mstoken+r'", "pull_request": false}'
    putstatus=req.patch(puturl,headers=headers,data=data_str)
    if putstatus.status_code >= 300:
        print(r'账号/应用 '+str(appnum)+' 的微软密钥上传失败，请检查secret里 DRONE_TOKEN 格式与设置是否正确')
    else:
        print(r'账号/应用 '+str(appnum)+' 的微软密钥上传成功')
    return putstatus
    
#调用 
for a in range(1, int(app_num)+1):
    client_id=os.getenv('CLIENT_ID_'+str(a))
    client_secret=os.getenv('CLIENT_SECRET_'+str(a))
    ms_token=os.getenv('MS_TOKEN_'+str(a))
    if a == 1:
        puturl=drone_server+r'/api/repos/'+drone_repo+r'/secrets/MS_TOKEN'
    else:
        puturl=drone_server+r'/api/repos/'+drone_repo+r'/secrets/MS_TOKEN_'+str(a)
    setsecret(getmstoken(ms_token,a),puturl,a)
