import requests
import json

nu = input('Enter your number: ')
pas = input('Enter your password: ')

url = "https://services.orange.eg/SignIn.svc/SignInUser"

payload = {
    "appVersion": "9.3.0",
    "channel": {
        "ChannelName": "MobinilAndMe",
        "Password": "ig3yh*mk5l42@oj7QAR8yF"
    },
    "dialNumber": nu,
    "isAndroid": True,
    "lang": "ar",
    "password": pas,
}

headers = {
    'User-Agent': "okhttp/4.10.0",
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip",
    'Content-Type': "application/json; charset=UTF-8"
}

try:
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    response.raise_for_status()  
    
    response_data = response.json()
    
    if 'SignInUserResult' not in response_data or 'AccessToken' not in response_data['SignInUserResult']:
        print('❌ Check Number And Password')
        exit()
        
    tok = response_data['SignInUserResult']['AccessToken']
    print("✅ Logged in successfully")
    
except requests.exceptions.RequestException:
    print("❌ Check Number And Password")
    exit()

url = "https://services.orange.eg/APIs/Profile/api/BasicAuthentication/Generate"

payload = {
    "ChannelName": "MobinilAndMe",
    "ChannelPassword": "ig3yh*mk5l42@oj7QAR8yF",
    "Dial": nu,
    "Language": "ar",
    "Module": "0",
    "Password": pas,
}

headers = {
    'User-Agent': "okhttp/4.10.0",
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip",
    'Content-Type': "application/json; charset=UTF-8",
    'AppVersion': "9.3.0",
    'OsVersion': "14",
    'IsAndroid': "true",
    'IsEasyLogin': "false",
    'Token': tok,
}

try:
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    response.raise_for_status()
    
    response_data = response.json()
    
    if 'Token' not in response_data:
        print('❌ Failed to generate authentication token')
        exit()
        
    too = response_data['Token']
    print("✅ Generated Token successfully")
    
except requests.exceptions.RequestException:
    print("❌ Check Number And Password")
    exit()
    
url = "https://services.orange.eg/APIs/Ramadan2024/api/RamadanOffers/Fawazeer/Submit"

payload = {
  "Dial": nu,
  "Language": "ar",
  "Token": too,
  "Answers": [
    {
      "QuestionId": 414,
      "AnswerId": 2191
    },
    {
      "QuestionId": 415,
      "AnswerId": 2193
    },
    {
      "QuestionId": 416,
      "AnswerId": 2200
    },
    {
      "QuestionId": 417,
      "AnswerId": 2203
    },
    {
      "QuestionId": 418,
      "AnswerId": 2206
    }
  ]
}

headers = {
  'User-Agent': "Mozilla/5.0 (Linux; Android 12; CPH2471 Build/SP1A.210812.016; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/139.0.7258.158 Mobile Safari/537.36",
  'Accept': "application/json, text/plain, */*",
  'Accept-Encoding': "gzip, deflate, br, zstd",
  'Content-Type': "application/json",
  'sec-ch-ua-platform': "\"Android\"",
  'sec-ch-ua': "\"Not;A=Brand\";v=\"99\", \"Android WebView\";v=\"139\", \"Chromium\";v=\"139\"",
  'sec-ch-ua-mobile': "?1",
  'Origin': "https://services.orange.eg",
  'X-Requested-With': "com.orange.mobinilandmf",
  'Sec-Fetch-Site': "same-origin",
  'Sec-Fetch-Mode': "cors",
  'Sec-Fetch-Dest': "empty",
  'Referer': f"https://services.orange.eg/Pages/fawazeer/game?dial={nu}&language=ar&token=c3a25678-dfca-4fd6-b1e0-74cd634f2ccf",
  'Accept-Language': "ar,en-US;q=0.9,en;q=0.8",
  'Cookie': "_gcl_au=1.1.1229268570.1753885594; _ga=GA1.1.601782415.1753885596; _fbp=fb.1.1753885597593.53264191434224724; _hjSessionUser_1095495=eyJpZCI6ImViOGNiZjI5LTgzZDEtNTdhZC04NTViLWY4MjMxMzQzNTliMSIsImNyZWF0ZWQiOjE3NTM4ODU1OTgwNDMsImV4aXN0aW5nIjp0cnVlfQ==; TS017d0201=013f7f7848c274ed69e9b9e257053dcd372386c31c2c99b32e51c827b068b27c2640e73c10b6df80b4fc7312d559fd03710e52302b; _hjSession_1095495=eyJpZCI6ImEwZGIxMTAzLWNlZjYtNGUyOS05YmNlLTM2ZDkyOWM2NTE1NSIsImMiOjE3NTc4NzA5NzA3OTYsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; TS017d0201030=017dc66eb575cbbab74792266f1ad092da47145fa30f0898d1fd8c929baa9a52ca33fe737e19a49ad085a3687d09f0a1e4cfdedfe2; TS017d0201028=017dc66eb5b88c2958782a408954a5a5a8af2a67670f0898d1fd8c929baa9a52ca33fe737e7f440d4c59f26b1fc87fd02cb97c3901; TSe0af757a027=08c2b1ecf4ab2000d3c7d4f23415fe80eb095a39b16606c03732769be5187b3b944097b4e275fef408a28ccf7b11300047c0352e3dad81bcab7a1ebadce08cccadba9485a88bec144f229bfbbb4e1d5240d4733a0ef8908fc2762bf8a69beb71; _ga_N3RCS60YKM=GS2.1.s1757870929$o17$g1$t1757871123$j26$l0$h0"
}

response = requests.post(url, data=json.dumps(payload), headers=headers)

response = requests.post(url, data=json.dumps(payload), headers=headers)

try:
    result = response.json()
    
    
    ErrorDescription = result.get("ErrorDescription")

    if ErrorDescription == "AlreadyRedeemedGiftToday":
        print("⚠️ لقد أخذت العرض من قبل")
    elif ErrorDescription == "FawazeerSuccess":
        print("✅ تم إضافة العرض بنجاح")
    else:
        print("❓ رد غير متوقع:", ErrorDescription)

except Exception as e:
    print("خطأ في قراءة الرد:", e)
    print("النص الخام:", response.text)