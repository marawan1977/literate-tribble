import requests
import urllib3
import re
import json
import hashlib
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def clean_phone_number(number):
    """إزالة جميع الفراغات والأحرف غير الرقمية من رقم الهاتف"""
    return re.sub(r'[^\d]', '', number)

def create_session():
    """إنشاء جلسة مع إعدادات إعادة المحاولة"""
    session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)
    return session

def send_request(session, url, headers, payload):
    """إرسال طلب مع إدارة أفضل للأخطاء"""
    try:
        response = session.post(
            url,
            headers=headers,
            json=payload,
            verify=False,
            timeout=45  # زيادة وقت الانتظار
        )
        response.raise_for_status()  # رفع استثناء لأي حالة خطأ HTTP
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"فشل الاتصال بالخادم: {str(e)}"}
    except json.JSONDecodeError:
        return {"error": "رد غير صحيح من الخادم"}

def activate_watchit():
    print("\n" + "-"*40)
    print("---- تفعيل اشتراك WatchIT ----")
    print("-"*40 + "\n")
    
    raw_number = input("📱 أدخل رقم الهاتف (01xxxxxxxxx): ").strip()
    number = clean_phone_number(raw_number)
    password = input("🔐 أدخل كلمة المرور: ").strip()

    # التحقق من صحة المدخلات
    if not re.fullmatch(r'01[0-9]{9}', number):
        return {"status": "error", "msg": "❌ رقم الهاتف غير صحيح. يجب أن يبدأ بـ 01 ويحتوي على 11 رقماً"}

    if len(password) < 6:
        return {"status": "error", "msg": "❌ كلمة المرور يجب أن تحتوي على 6 أحرف على الأقل"}

    channel = {
        "ChannelName": "MobinilAndMe",
        "Password": "ig3yh*mk5l42@oj7QAR8yF"
    }

    # إنشاء جلسة مع إعدادات الاتصال
    session = create_session()

    # تسجيل الدخول
    print("\n🔐 جاري تسجيل الدخول...")
    login_payload = {
        "appVersion": "8.8.5",  # تحديث نسخة التطبيق
        "channel": channel,
        "dialNumber": number,
        "isAndroid": True,
        "lang": "ar",
        "password": password
    }
    login_headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "User-Agent": "okhttp/4.10.0",
        "x-microservice-name": "APMS"
    }
    login_url = "https://services.orange.eg/SignIn.svc/SignInUser"
    login_response = send_request(session, login_url, login_headers, login_payload)

    if "error" in login_response:
        return {"status": "error", "msg": f"❌ {login_response['error']}"}

    if 'SignInUserResult' not in login_response:
        return {"status": "error", "msg": "❌ هيكل البيانات غير متوقع من الخادم"}

    signin_result = login_response['SignInUserResult']

    if 'ErrorCode' in signin_result and signin_result['ErrorCode'] != 0:
        error_msg = signin_result.get('ErrorDescription', f"كود الخطأ: {signin_result['ErrorCode']}")
        return {"status": "error", "msg": f"❌ {error_msg}"}

    if 'AccessToken' not in signin_result or not signin_result['AccessToken']:
        return {"status": "error", "msg": "❌ فشل في الحصول على رمز الدخول"}

    print("✅ تم تسجيل الدخول بنجاح")

    # توليد التوكن
    print("\n🔑 جاري توليد التوكن...")
    token_payload = {
        "appVersion": "2.9.8",
        "channel": channel,
        "dialNumber": number,
        "isAndroid": True,
        "password": password
    }
    token_headers = {
        "Content-Type": "application/json",
        "User-Agent": "okhttp/4.10.0"
    }
    token_url = "https://services.orange.eg/GetToken.svc/GenerateToken"
    token_response = send_request(session, token_url, token_headers, token_payload)

    if "error" in token_response:
        return {"status": "error", "msg": f"❌ {token_response['error']}"}

    if 'GenerateTokenResult' not in token_response:
        return {"status": "error", "msg": "❌ هيكل التوكن غير متوقع من الخادم"}

    token_result = token_response['GenerateTokenResult']
    ctv = token_result.get('Token', '')

    if not ctv:
        return {"status": "error", "msg": "❌ فشل في الحصول على التوكن"}

    htv_input = f"{ctv},{{.c][o^uecnlkijh*.iomv:QzCFRcd;drof/zx}}w;ls.e85T^#ASwa?=(lk"
    htv = hashlib.sha256(htv_input.encode()).hexdigest().upper()

    # تفعيل الخدمة
    print("\n🎬 جاري تفعيل WatchIT...")
    fulfillment_payload = {
        "ChannelName": channel["ChannelName"],
        "ChannelPassword": channel["Password"],
        "Dial": number,
        "Language": "ar",
        "Password": password,
        "ServiceID": "5"
    }
    fulfillment_headers = {
        "_ctv": ctv,
        "_htv": htv,
        "Content-Type": "application/json;charset=UTF-8",
        "User-Agent": "okhttp/4.10.0"
    }
    fulfillment_url = "https://services.orange.eg/APIs/Entertainment/api/EagleRevamp/Fulfillment"
    fulfillment_response = send_request(session, fulfillment_url, fulfillment_headers, fulfillment_payload)

    if "error" in fulfillment_response:
        return {"status": "error", "msg": f"❌ {fulfillment_response['error']}"}

    if fulfillment_response.get("ErrorCode") == 0:
        return {"status": "success", "msg": "✅ تم الاشتراك بنجاح. ستصلك رسالة تأكيد من 5030"}
    elif fulfillment_response.get("ErrorCode") == 1:
        return {"status": "info", "msg": "ℹ️ أنت مشترك بالفعل في خدمة WatchIT"}
    else:
        error_msg = fulfillment_response.get("ErrorDescription", "فشل غير معروف")
        return {"status": "error", "msg": f"❌ {error_msg}"}

if __name__ == "__main__":
    result = activate_watchit()
    print("\n" + "-"*20)
    print("النتيجة:")
    print(result["msg"])
    print("-"*20)