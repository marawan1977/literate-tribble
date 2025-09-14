import requests
import json
from datetime import datetime

# إعدادات الجلسة
session = requests.Session()
headers = {
    'Host': 'my.te.eg',
    'Connection': 'keep-alive',
    'sec-ch-ua-platform': '"Android"',
    'languageCode': 'en-US',
    'isSelfcare': 'true',
    'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?1',
    'isMobile': 'false',
    'isCoporate': 'false',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'clientType': 'Chrome',
    'Content-Type': 'application/json',
    'channelId': '702',
    'delegatorSubsId': '',
    'Origin': 'https://my.te.eg',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://my.te.eg/echannel/',
}

# طلب إدخال بيانات المستخدم
def get_user_credentials():
    while True:
        account_number = input(":الرجاء إدخال رقم الحساب: ").strip()
        if account_number:
            break
        print("رقم الحساب لا يمكن أن يكون فارغًا!")
    
    while True:
        password = input("الرجاء إدخال كلمة المرور: ").strip()
        if password:
            break
        print("كلمة المرور لا يمكن أن تكون فارغة!")
    
    return account_number, password

# معالجة الرقم لإزالة الأصفار في البداية وإضافة FBB إذا لزم الأمر
def process_account_number(account_number):
    # إزالة أي مسافات أو أحرف غير رقمية
    cleaned = ''.join(c for c in account_number if c.isdigit())
    
    # إزالة الأصفار من البداية
    cleaned = cleaned.lstrip('0')
    
    # إضافة البادئة FBB إذا لم تكن موجودة
    if not cleaned.upper().startswith("FBB"):
        cleaned = "FBB" + cleaned
    
    return cleaned

# الطلب الأول: المصادقة
def authenticate(session, account_number, password):
    auth_url = 'https://my.te.eg/echannel/service/besapp/base/rest/busiservice/v1/auth/userAuthenticate'
    auth_data = {
        "acctId": account_number,
        "password": password,
        "appLocale": "en-US",
        "isSelfcare": "Y",
        "isMobile": "N",
        "recaptchaToken": ""
    }

    print("جاري تسجيل الدخول...")
    auth_response = session.post(auth_url, headers=headers, json=auth_data)
    return auth_response

# الطلب الثاني: استعلام معلومات الاستهلاك
def get_usage_data(session, subscriber_id):
    query_url = 'https://my.te.eg/echannel/service/besapp/base/rest/busiservice/cz/cbs/bb/queryFreeUnit'
    query_data = {
        "subscriberId": subscriber_id,
        "needQueryPoint": True
    }
    return session.post(query_url, headers=headers, json=query_data)

# الطلب الثالث: تحليل استهلاك البيانات
def get_billing_usage(session, subscriber_id):
    billing_url = 'https://my.te.eg/echannel/service/besapp/base/rest/busiservice/cz/v1/resource/getBillingUsage'
    billing_data = {
        "subscriberId": subscriber_id
    }
    return session.post(billing_url, headers=headers, json=billing_data)

# دالة لتحويل الطوابع الزمنية إلى تاريخ مقروء
def timestamp_to_date(timestamp):
    if timestamp == 0:
        return "غير محدد"
    try:
        return datetime.fromtimestamp(timestamp/1000).strftime('%Y-%m-%d %H:%M:%S')
    except:
        return "غير صالح"

# دالة لعرض معلومات الاستهلاك
def display_usage_data(response_data):
    """عرض تفاصيل استهلاك الباقات والخدمات"""
    if not response_data.get('body'):
        print("لا توجد بيانات استهلاك متاحة.")
        return

    print("تفاصيل معلومات الاستهلاك:")
    

    for package in response_data['body']:
        # معلومات الباقة الأساسية
        print(f"\n⦿ اسم الباقة: {package.get('offerName', 'غير معروف')}")
        print(f"├─ نوع الخدمة: {package.get('freeUnitTypeName', 'غير معروف')}")
        print(f"├─ نوع الباقة: {package.get('freeUnitTypeId', 'غير معروف')}")
        print(f"├─ الكمية الإجمالية: {package.get('total', 0)}")
        print(f"├─ الكمية المستهلكة: {package.get('used', 0)}")
        print(f"├─ الكمية المتبقية: {package.get('remain', 0)}")
        print(f"└─ تاريخ الانتهاء: {timestamp_to_date(package.get('expireTime', 0))}")

        # تفاصيل الأجزاء (إن وجدت)
        if package.get('freeUnitBeanDetailList'):
            print("\nتفاصيل الأجزاء:")
            for detail in package['freeUnitBeanDetailList']:
                print(f"\n▶ {detail.get('offeringName', 'غير معروف')}")
                print(f"  ├─ النوع: {detail.get('originType', 'غير معروف')}")
                print(f"  ├─ الكمية الأولية: {detail.get('initialAmount', 0)}")
                print(f"  ├─ الكمية الحالية: {detail.get('currentAmount', 0)}")
                print(f"  ├─ تاريخ الانتهاء: {timestamp_to_date(detail.get('expireTime', 0))}")
                print(f"  └─ أيام متبقية: {detail.get('remainingDaysForRenewal', 0)} يوم")

def display_billing_usage(billing_data):
    """عرض تحليل استهلاك البيانات حسب الفئات"""
    if not billing_data.get('body', {}).get('lastCycle'):
        print("لا توجد بيانات تحليل استهلاك متاحة.")
        return

    print("تحليل استهلاك البيانات:")
    last_cycle = billing_data['body']['lastCycle']

    # معلومات الدورة
    print("\nآخر دورة استهلاك:")
    print(f"الفترة من {last_cycle.get('consumptionStartDate', 'غير معروف')} إلى "
          f"{last_cycle.get('consumptionEndDate', 'غير معروف')}")
    print(f"نسبة الاستهلاك: {last_cycle.get('consumptionPercentage', 0)}%")

    # فئات الاستهلاك
    CATEGORIES = [
        ('بث الفيديو', 'streamingVideoPercentage'),
        ('المحتوى التنزيل', 'contentDownPercentage'),
        ('المحتوى الرفع', 'contentUpPercentage'),
        ('الألعاب', 'gamingPercentage'),
        ('التواصل الاجتماعي', 'socialPercentage'),
        ('التصفح', 'webPercentage'),
        ('أخرى', 'othersPercentage')
    ]

    print("\nتفاصيل الاستهلاك:")
    for name, key in CATEGORIES:
        print(f"▸ {name}: {last_cycle.get(key, 0)}%")

# التنفيذ الرئيسي
def main():
    # الحصول على بيانات المستخدم
    account_number, password = get_user_credentials()
    
    # معالجة رقم الحساب
    processed_account = process_account_number(account_number)
    
    
    # المصادقة
    auth_response = authenticate(session, processed_account, password)
    
    if auth_response.status_code != 200:
        print(f"\nفشل المصادقة. كود الحالة: {auth_response.status_code}")
        print(auth_response.text)
        return
    
    auth_data = auth_response.json()
    
    # استخراج البيانات المهمة من رد المصادقة
    token = auth_data['body']['token']
    subscriber_id = auth_data['body']['subscriber']['subscriberId']
    
    # إضافة التوكن إلى رؤوس الطلب التالية
    headers['csrftoken'] = token
    
    # استعلام معلومات الاستهلاك
    query_response = get_usage_data(session, subscriber_id)
    
    if query_response.status_code != 200:
        print(f"\nفشل استعلام معلومات الاستهلاك. كود الحالة: {query_response.status_code}")
        print(query_response.text)
        return
    
    usage_data = query_response.json()
    display_usage_data(usage_data)
    
    # تحليل استهلاك البيانات
    billing_response = get_billing_usage(session, subscriber_id)
    
    if billing_response.status_code != 200:
        print(f"\nفشل تحليل استهلاك البيانات. كود الحالة: {billing_response.status_code}")
        print(billing_response.text)
        return
    
    billing_data = billing_response.json()
    display_billing_usage(billing_data)
    
    print("\n[تم الانتهاء بنجاح]")

if __name__ == "__main__":
    main()