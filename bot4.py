import requests
import json
import time
import threading
from colorama import Fore, init

init(autoreset=True)

number_owner = "01062559814"  
password_owner = "Mahmoud@1"
number_member1 = "01092140306"  
password_member1 = "Pp0$$$$$"
number_member2 = "01044230528"  
password_member2 = "Ahmed1@.~"

def log():
    url = "https://mobile.vodafone.com.eg/auth/realms/vf-realm/protocol/openid-connect/token"
    payload = {
        'username': number_owner,
        'password': password_owner,
        'grant_type': "password",
        'client_secret': "a2ec6fff-0b7f-4aa4-a733-96ceae5c84c3",
        'client_id': "my-vodafone-app"
    }
    headers = {
        'User-Agent': "okhttp/4.9.3",
        'Accept': "application/json, text/plain, */*",
        'Accept-Encoding': "gzip",
        'x-agent-operatingsystem': "V12.5.13.0.RJQMIXM",
        'clientId': "xxx",
        'x-agent-device': "lime",
        'x-agent-version': "2024.10.1",
        'x-agent-build': "562"
    }

    r1 = requests.post(url, data=payload, headers=headers).json()

    if 'access_token' not in r1:
        print(Fore.RED + "❌ Login failed. Check your number or password.")
        return None

    access_token1 = "Bearer " + r1['access_token']
    print(Fore.GREEN + "✅ Login successful!")
    time.sleep(3)

    # Change the first member's quota from 1300 to 5200
    print(Fore.CYAN + "🔄 Changing  member quota to 1300")

    url = "https://web.vodafone.com.eg/services/dxl/cg/customerGroupAPI/customerGroup"
    payload = {
        "name": "FlexFamily",
        "type": "QuotaRedistribution",
        "category": [
            {"value": "523", "listHierarchyId": "PackageID"},
            {"value": "47", "listHierarchyId": "TemplateID"},
            {"value": "523", "listHierarchyId": "TierID"},
            {"value": "percentage", "listHierarchyId": "familybehavior"}
        ],
        "parts": {
            "member": [
                {"id": [{"value": number_owner, "schemeName": "MSISDN"}], "type": "Owner"},
                {"id": [{"value": number_member1, "schemeName": "MSISDN"}], "type": "Member"}
            ],
            "characteristicsValue": {
                "characteristicsValue": [
                    {"characteristicName": "quotaDist1", "value": "10", "type": "percentage"}
                ]
            }
        }
    }
    headers = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 11; M2010J19SG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.85 Mobile Safari/537.36",
        'Accept': "application/json",
        'Content-Type': "application/json",
        'sec-ch-ua': "\"Chromium\";v=\"94\", \"Google Chrome\";v=\"94\", \";Not A Brand\";v=\"99\"",
        'msisdn': number_owner,
        'Accept-Language': "AR",
        'sec-ch-ua-mobile': "?1",
        'Authorization': access_token1,
        'x-dtpc': "5$160966758_702h19vRCUAEMOMIIASTHWKLEMFNIHJNUTANVVK-0e0",
        'clientId': "WebsiteConsumer",
        'sec-ch-ua-platform': "\"Android\"",
        'Origin': "https://web.vodafone.com.eg",
        'Sec-Fetch-Site': "same-origin",
        'Sec-Fetch-Mode': "cors",
        'Sec-Fetch-Dest': "empty",
        'Referer': "https://web.vodafone.com.eg/spa/familySharing",
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    print(Fore.MAGENTA + "📤 Quota redistribution response:")
    print(response.text)
    print("⏳ Waiting 5 minutes...")
    time.sleep(300)
    
    print(Fore.CYAN + "📨 Sending invitation to the second member...")
    url = "https://web.vodafone.com.eg/services/dxl/cg/customerGroupAPI/customerGroup"
    payload = {
        "name": "FlexFamily",
        "type": "SendInvitation",
        "category": [
            {"value": "523", "listHierarchyId": "PackageID"},
            {"value": "47", "listHierarchyId": "TemplateID"},
            {"value": "523", "listHierarchyId": "TierID"},
            {"value": "percentage", "listHierarchyId": "familybehavior"}
        ],
        "parts": {
            "member": [
                {"id": [{"value": number_owner, "schemeName": "MSISDN"}], "type": "Owner"},
                {"id": [{"value": number_member2, "schemeName": "MSISDN"}], "type": "Member"}
            ],
            "characteristicsValue": {
                "characteristicsValue": [
                    {"characteristicName": "quotaDist1", "value": "10", "type": "percentage"}
                ]
            }
        }
    }
    headers = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 11; M2010J19SG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.85 Mobile Safari/537.36",
        'Accept': "application/json",
        'Content-Type': "application/json",
        'sec-ch-ua': "\"Chromium\";v=\"94\", \"Google Chrome\";v=\"94\", \";Not A Brand\";v=\"99\"",
        'msisdn': number_owner,
        'Accept-Language': "AR",
        'sec-ch-ua-mobile': "?1",
        'Authorization': access_token1,
        'x-dtpc': "5$160966758_702h19vRCUAEMOMIIASTHWKLEMFNIHJNUTANVVK-0e0",
        'clientId': "WebsiteConsumer",
        'sec-ch-ua-platform': "\"Android\"",
        'Origin': "https://web.vodafone.com.eg",
        'Sec-Fetch-Site': "same-origin",
        'Sec-Fetch-Mode': "cors",
        'Sec-Fetch-Dest': "empty",
        'Referer': "https://web.vodafone.com.eg/spa/familySharing",
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    print(Fore.MAGENTA + "📤 Invitation response:")
    print(response.text)
    print("⏳ Waiting 3 seconds...")
    time.sleep(3)
    
def delete():
    print(Fore.GREEN + "\n🎉 All operations completed successfully!")
    print("👨‍💻 Developer: Mhmd Naser")

    url = "https://mobile.vodafone.com.eg/auth/realms/vf-realm/protocol/openid-connect/token"
    payload = {
        'username': number_owner,
        'password': password_owner,
        'grant_type': "password",
        'client_secret': "a2ec6fff-0b7f-4aa4-a733-96ceae5c84c3",
        'client_id': "my-vodafone-app"
    }
    headers = {
        'User-Agent': "okhttp/4.9.3",
        'Accept': "application/json, text/plain, */*",
        'Accept-Encoding': "gzip",
        'x-agent-operatingsystem': "V12.5.13.0.RJQMIXM",
        'clientId': "xxx",
        'x-agent-device': "lime",
        'x-agent-version': "2024.10.1",
        'x-agent-build': "562"
    }
    r1 = requests.post(url, data=payload, headers=headers).json()
    access_token1 = "Bearer " + r1['access_token']

    print(Fore.GREEN + "✅ Login successful!")
    print(Fore.CYAN + "🗑️ Deleting the second member...")

    # Delete the second member
    url = "https://web.vodafone.com.eg/services/dxl/cg/customerGroupAPI/customerGroup"
    payload = {
        "name": "FlexFamily",
        "type": "FamilyRemoveMember",
        "category": [{"value": "47", "listHierarchyId": "TemplateID"}],
        "parts": {
            "member": [
                {"id": [{"value": number_owner, "schemeName": "MSISDN"}], "type": "Owner"},
                {"id": [{"value": number_member2, "schemeName": "MSISDN"}], "type": "Member"}
            ],
            "characteristicsValue": {
                "characteristicsValue": [
                    {"characteristicName": "Disconnect", "value": "0"},
                    {"characteristicName": "LastMemberDeletion", "value": "1"}
                ]
            }
        }
    }
    headers = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 11; M2010J19SG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.85 Mobile Safari/537.36",
        'Accept': "application/json",
        'Content-Type': "application/json",
        'sec-ch-ua': "\"Chromium\";v=\"94\", \"Google Chrome\";v=\"94\", \";Not A Brand\";v=\"99\"",
        'msisdn': number_owner,
        'Accept-Language': "AR",
        'sec-ch-ua-mobile': "?1",
        'Authorization': access_token1,
        'x-dtpc': "8$160966758_702h28vFSPMIAKHHWGIIKVDPLHCDFHKOJUBFNJP-0e0",
        'clientId': "WebsiteConsumer",
        'sec-ch-ua-platform': "\"Android\"",
        'Origin': "https://web.vodafone.com.eg",
        'Sec-Fetch-Site': "same-origin",
        'Sec-Fetch-Mode': "cors",
        'Sec-Fetch-Dest': "empty",
        'Referer': "https://web.vodafone.com.eg/spa/familySharing",
    }
    response = requests.patch(url, data=json.dumps(payload), headers=headers)

    print(Fore.MAGENTA + "🗑️ Delete member response:")
    print(response.text)
    print("⏳ Waiting another 5 minutes to avoid ban...")

def login(number, password):
    """Login function"""
    url = "https://mobile.vodafone.com.eg/auth/realms/vf-realm/protocol/openid-connect/token"
    payload = {
        'username': number,
        'password': password,
        'grant_type': 'password',
        'client_secret': 'a2ec6fff-0b7f-4aa4-a733-96ceae5c84c3',
        'client_id': 'my-vodafone-app'
    }
    headers = {
        'User-Agent': 'okhttp/4.9.3',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip',
        'x-agent-operatingsystem': 'V12.5.13.0.RJQMIXM',
        'clientId': 'xxx',
        'x-agent-device': 'lime',
        'x-agent-version': '2024.10.1',
        'x-agent-build': '562'
    }
    try:
        response = requests.post(url, data=payload, headers=headers, timeout=10)
        return response.json()
    except Exception as e:
        print(Fore.RED + f"❌ Login error for number {number}: {str(e)}")
        return None

def accept_invitation(access_token_member):
    """Accept invitation function"""
    url = "https://mobile.vodafone.com.eg/services/dxl/cg/customerGroupAPI/customerGroup"
    payload = {
        "category": [{"listHierarchyId": "TemplateID", "value": "47"}],
        "name": "FlexFamily",
        "parts": {
            "member": [
                {"id": [{"schemeName": "MSISDN", "value": number_owner}], "type": "Owner"},
                {"id": [{"schemeName": "MSISDN", "value": number_member2}], "type": "Member"}
            ]
        },
        "type": "AcceptInvitation"
    }
    headers = {
        'User-Agent': 'okhttp/4.11.0',
        'Connection': 'Keep-Alive',
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json',
        'api_id': 'APP',
        'x-dynatrace': 'MT_3_24_3486379639_64-0_a556db1b-4506-43f3-854a-1d2527767923_0_187_277',
        'Authorization': f"Bearer {access_token_member}",
        'api-version': 'v2',
        'x-agent-operatingsystem': '13',
        'clientId': 'AnaVodafoneAndroid',
        'x-agent-device': 'Xiaomi 21061119AG',
        'x-agent-version': '2024.12.1',
        'x-agent-build': '946',
        'msisdn': number_member2,
        'Accept-Language': 'ar',
        'Content-Type': 'application/json; charset=UTF-8'
    }
    try:
        response = requests.patch(url, data=json.dumps(payload), headers=headers, timeout=10)
        print(Fore.CYAN + f"📩 Invitation accepted successfully! (Response status: {response.status_code})")
        return response
    except Exception as e:
        print(Fore.RED + f"❌ Error accepting invitation: {str(e)}")
        return None

def adjust_quota(access_token_owner):
    """Quota adjustment function"""
    url = "https://web.vodafone.com.eg/services/dxl/cg/customerGroupAPI/customerGroup"
    payload = {
        "name": "FlexFamily",
        "type": "QuotaRedistribution",
        "category": [
            {"value": "523", "listHierarchyId": "PackageID"},
            {"value": "47", "listHierarchyId": "TemplateID"},
            {"value": "523", "listHierarchyId": "TierID"},
            {"value": "percentage", "listHierarchyId": "familybehavior"}
        ],
        "parts": {
            "member": [
                {"id": [{"value": number_owner, "schemeName": "MSISDN"}], "type": "Owner"},
                {"id": [{"value": number_member1, "schemeName": "MSISDN"}], "type": "Member"}
            ],
            "characteristicsValue": {
                "characteristicsValue": [
                    {"characteristicName": "quotaDist1", "value": "40", "type": "percentage"}
                ]
            }
        }
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 11; M2010J19SG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.85 Mobile Safari/537.36',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
        'msisdn': number_owner,
        'Accept-Language': 'AR',
        'sec-ch-ua-mobile': '?1',
        'Authorization': f"Bearer {access_token_owner}",
        'x-dtpc': '5$160966758_702h19vRCUAEMOMIIASTHWKLEMFNIHJNUTANVVK-0e0',
        'clientId': 'WebsiteConsumer',
        'sec-ch-ua-platform': '"Android"',
        'Origin': 'https://web.vodafone.com.eg',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://web.vodafone.com.eg/spa/familySharing'
    }
    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers, timeout=10)
        print(Fore.GREEN + f"🔄 Quota changed to 40% successfully! (Response status: {response.status_code})")
        return response
    except Exception as e:
        print(Fore.RED + f"❌ Error changing quota: {str(e)}")
        return None

def main():
    while True:
        log()
        print(Fore.YELLOW + "\n🔐 Logging in as owner...")
        owner_login = login(number_owner, password_owner)
        if not owner_login or 'access_token' not in owner_login:
            print(Fore.RED + "❌ Owner login failed")
            continue
        owner_token = owner_login['access_token']
        print(Fore.GREEN + f"✅ Owner ({number_owner}) logged in successfully!")
        time.sleep(3)
        print(Fore.YELLOW + "\n🔐 Logging in as first member...")
        member1_login = login(number_member1, password_member1)
        if not member1_login or 'access_token' not in member1_login:
            print(Fore.RED + "❌ First member login failed")
            continue
        member1_token = member1_login['access_token']
        print(Fore.GREEN + f"✅ First member ({number_member1}) logged in successfully!")
        time.sleep(3)
        print(Fore.YELLOW + "\n🔐 Logging in as second member...")
        member2_login = login(number_member2, password_member2)
        if not member2_login or 'access_token' not in member2_login:
            print(Fore.RED + "❌ Second member login failed")
            continue
        member2_token = member2_login['access_token']
        print(Fore.GREEN + f"✅ Second member ({number_member2}) logged in successfully!")
        time.sleep(12)
        print(Fore.YELLOW + "\n⚡ Executing operations simultaneously...")
        t1 = threading.Thread(target=accept_invitation, args=(member2_token,))
        t2 = threading.Thread(target=adjust_quota, args=(owner_token,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        time.sleep(3)
        delete()
        time.sleep(300)

if __name__ == "__main__":
    print("👨‍💻 Developer:Mhmd Naser")
    main()