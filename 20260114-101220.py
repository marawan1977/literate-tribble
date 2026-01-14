import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import requests
import re
import base64
import hashlib
import xml.etree.ElementTree as ET
import hmac

# استبدل TOKEN_HERE بتيليجرام بوت توكين الخاص بك
TOKEN = "8124076327:AAHk0AwnXMdu7z5LAeJjW9FXGuhq26GcFdM"
bot = telebot.TeleBot(TOKEN)

# تخزين البيانات
user_action = {}
BOT_DEACTIVATION_MESSAGE = "⛔ البوت غير نشط حاليًا، يرجى المحاولة لاحقًا."

# ========== دوال المساعدة ==========
def validate_phone(phone):
    """التحقق من صحة رقم الهاتف المصري"""
    return re.match(r'^01[0125][0-9]{8}$', phone)

def validate_email(email):
    """التحقق من صحة البريد الإلكتروني"""
    return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)

def is_bot_active():
    """التحقق من حالة البوت"""
    return True

def show_progress(chat_id):
    """إظهار رسالة تقدم"""
    try:
        msg = bot.send_message(chat_id, "⏳ جاري المعالجة...")
        return msg.message_id
    except:
        return None

# ========== دوال Etisalat ==========
def activate_etisalat_social_email(email, password, chat_id):
    """
    تفعيل 500 ميجا سوشيال باستخدام البريد الإلكتروني وكلمة المرور
    """
    show_progress(chat_id)
    
    try:
        def make_headers(token):
            return {
                'Host': "mab.etisalat.com.eg:11003",
                'User-Agent': "okhttp/5.0.0-alpha.11",
                'Connection': "Keep-Alive",
                'Accept': "text/xml",
                'Accept-Encoding': "gzip",
                'Content-Type': "text/xml; charset=UTF-8",
                'applicationVersion': "2",
                'applicationName': "MAB",
                'Authorization': f"Basic {token}",
                'Language': "ar",
                'APP-BuildNumber': "10650",
                'APP-Version': "33.1.0",
                'OS-Type': "Android",
                'OS-Version': "13",
                'APP-STORE': "GOOGLE",
                'C-Type': "4G",
                'Is-Corporate': "false",
                'ADRUM_1': "isMobile:true",
                'ADRUM': "isAjax:true"
            }

        def login_and_get_number(email, password):
            tok = f"{email}:{password}"
            token = base64.b64encode(tok.encode()).decode()
            headers = make_headers(token)

            login = """<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>
            <loginRequest>
                <deviceId></deviceId>
                <firstLoginAttempt>false</firstLoginAttempt>
                <modelType></modelType>
                <osVersion></osVersion>
                <platform>Android</platform>
                <udid></udid>
            </loginRequest>"""
            
            r = requests.post(
                "https://mab.etisalat.com.eg:11003/Saytar/rest/authentication/loginWithPlan",
                data=login, 
                headers=headers, 
                timeout=15
            )

            xml = ET.fromstring(r.text)
            dial = xml.find("dial")
            if dial is None or dial.text is None:
                raise Exception("❌ فشل تسجيل الدخول")
            return dial.text, token

        number, token = login_and_get_number(email, password)
        
        headers = {
            "Authorization": f"Basic {token}",
            "Content-Type": "text/xml; charset=UTF-8",
            "applicationName": "MAB",
            "APP-Version": "30.2.0",
            "OS-Type": "Android",
            'User-Agent': "okhttp/5.0.0-alpha.11",
            "Language": "ar"
        }
        
        # تنظيف رقم الهاتف
        number = number[1:] if number.startswith('0') else number
        
        data = f"""
        <submitOrderRequest>
            <mabOperation></mabOperation>
            <msisdn>{number}</msisdn>
            <operation>REDEEM</operation>
            <productName>DOWNLOAD_GIFT_1_SOCIAL_UNITS</productName>
        </submitOrderRequest>
        """
        
        response = requests.post(
            "https://mab.etisalat.com.eg:11003/Saytar/rest/servicemanagement/submitOrderV2",
            headers=headers,
            data=data,
            timeout=30
        )
        
        if response.status_code != 200:
            return f"❌ خطأ في الخادم (كود {response.status_code})"
        
        if "true" not in response.text:
            return "❌ فشل في التفعيل (قد يكون العرض غير متاح)"
        
        return "✅ تم تفعيل 500 ميجا سوشيال من Etisalat بنجاح! 🎉"
        
    except requests.exceptions.Timeout:
        return "❌ انتهى وقت الانتظار"
    except Exception as e:
        return f"❌ حدث خطأ تقني: {str(e)}"

def activate_etisalat_social_number(phone_number, chat_id):
    """
    تفعيل 500 ميجا سوشيال باستخدام رقم الهاتف فقط
    """
    show_progress(chat_id)
    
    try:
        E_KEY = "MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAMPHzaCIoXe5oWoWGzTaRM7PYm4FpzxX5V2sclFixgA4IYjXLP0in1mKgeTjRy2PuqSH/kdQaTV0HujtCZtOXaECAwEAAQ=="
        
        def calculate_hmac_sha512(data, key):
            try:
                key_bytes = key.encode('utf-8')
                data_bytes = data.encode('utf-8')
                mac = hmac.new(key_bytes, data_bytes, hashlib.sha512)
                return mac.hexdigest()
            except Exception as e:
                return None

        def get_hcaptcha_token_placeholder():
            return "P1_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.haJwZACjZXhwzmj-QTCncGFzc2tlecUEOssAouAqS6SlftrvTiSZYpbcEGKpumcHUPCxygexZXAOOMBOvWA-9rheI5NWUtFbzJmrjRdo9ZtmydQfHFH6K0lzn_cO7Va1_nhc891gVtaJWqzFq3NuCo2ePhFUSgBHc4mlzUSz9cIRBIjB2cLxNUlo1GXWyUSUPaT4Znza4H_4ljma3zRHQUvgA56x2kiNpTp_d_vK09D0gs3818gE-M7K8ZsXVCGL5xN7qkwy-GjKeJrZ4Gd0vG5Rkn8Om9GH5jGEvPK_QRwlZH8S5rLNcCg4_zLHLrksDLsxju0gahjBxGiCVbynqsjc0jGuP9T2IuZ91dmGthF4O6KVwtiHgs85YyFOx6uyYTWW_ytLC37qShI6XTtEmzbwEn96AjDTqjJ8VzoJ-eUt_VFVOY0fN62fbEjhEkJ0FODdukeGx70-navCKrINiSJLwFj727dkw-awbXsz6Fahb_Ap2E2JQHpoAe_Oj7AhlExQUj5qohyYd3SEksXPNcAw39q9JOvsAFh_JDRMHwNAs6OqqQ0KJS0INEWTLUBnpz2JQdwMn3qXX9OHY18SnwONPdSGG8NZv8-5liAnnj9vN-cD314Ot5xK9fAo6r8fYxtxY6xLHdbcWDXxoZ0KARCvIW6EMwNhWLOT_p32nuBNCEVIcV74ecG9yMw6LmzQE4t0dOlbOabbG97qu7N0HdAY3-ekobXrgpb-MP1johRbF9VcVfW5_4-PtMzvt2ncp-8CXMptqtM2ygQtRUTKe1Ax8KffeyXqboc2PFG3uPZG3hRehN5XM1-y5ALs7whH_gHFCOWcuPxoyz6kpKCopvhzqVKFbm-MF6qL4XVi8dMWHWYus4-3MSrRL6p2G3MJD6glGyIeZVWcZ-onZloB8ZPNy9M-NR7MAg0AAVvwt9E7AXb3El4ThNlVLFhn7X3vRzG38djARNowLUQot3yzwNFJ6yqoiNihIvNfTitw-02mfsP-Kn8tW2wNP1TjRYwqpOPBgTphhrk_Wc5OZBhc_2MnTbTO5SjD6i2jz-rDZXKf6C093CMjeDJBy9sPquXiz2BfS2TXUe8WtPEMdvZOYxtXoqqH11rbLiXkBDoEdwuw9YYv9gAoNaqYwR7cD6uYf759gaTbjDpaVHIT6n_iIf6gWOvbvu-oPOPKQabni0cQoJes1YKRqFoGF5B1uswepDxwcwwXQUKEC3puewNqI9JZpOeZKuazyik-B65pgAS_Yu2BDBlAyHPkpeWCMoo4sNFl3can705kzfICu-v_wQ7SOILSTGZwYURJXwvb-CcKEStsQxOh2YBPwC46ZEVoB0Nvdf7_vvUKHfE3vfNZVTXHqyxaHoc4_miYwHKBY8dCra6p-dqxi_MFZZMl-qkONRjlIkVps3bVc4jz5zljzU9fpdRWCvknYhdvdq78g-Ly0t4YFA4HmnqnMnQVOhbDfEG-omtyqDM1MThmMDE1qHNoYXJkX2lkzgMxg28.6G26dfld5GB5nus9npccGO70_6tLdncTtMc0D1xqVSI"

        def generate_base_headers_list():
            return [
                ("applicationVersion", "2"),
                ("applicationName", "MAB"),
                ("Language", "ar"),
                ("APP-BuildNumber", "10664"),
                ("APP-Version", "33.5.0"),
                ("OS-Type", "Android"),
                ("OS-Version", "15"),
                ("APP-STORE", "GOOGLE"),
                ("C-Type", "WIFI"),
                ("Is-Corporate", "false")
            ]

        def send_otp_request(phone, udid, hcaptcha_token):
            try:
                url = "https://mab.etisalat.com.eg:11003/Saytar/rest/quickAccess/sendVerCodeQuickAccessV4"
                url_path_to_sign = "/Saytar/rest/quickAccess/sendVerCodeQuickAccessV4"
                
                body_xml = f"""<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>
        <sendVerCodeQuickAccessRequest>
          <dial>{phone}</dial>
          <hCaptchaToken>{hcaptcha_token}</hCaptchaToken>
          <udid>{udid}</udid>
        </sendVerCodeQuickAccessRequest>"""
                
                base_headers_list = generate_base_headers_list()
                header_string_to_sign = ",".join([f"{k} {v}" for k, v in base_headers_list])
                
                header_sig = calculate_hmac_sha512(header_string_to_sign, E_KEY)
                url_sig = calculate_hmac_sha512(url_path_to_sign, E_KEY)
                body_sig = calculate_hmac_sha512(body_xml, E_KEY)
                
                if not all([header_sig, url_sig, body_sig]):
                     return False, "❌ فشل في حساب التواقيع اللازمة."

                headers = {
                    "Accept": "text/xml", "Content-Type": "text/xml; charset=UTF-8",
                    "Host": "mab.etisalat.com.eg:11003", "Connection": "Keep-Alive",
                    "User-Agent": "okhttp/5.0.0-alpha.11",
                }
                headers.update(dict(base_headers_list))
                headers["headerSignature"] = header_sig
                headers["urlSignature"] = url_sig
                headers["bodySignature"] = body_sig
                
                response = requests.post(url, headers=headers, data=body_xml, timeout=15)
                
                if response.status_code == 200:
                    if "true" in response.text.lower() or "success" in response.text.lower():
                         return True, "✅ تم إرسال الكود بنجاح"
                    else:
                        try:
                            root = ET.fromstring(response.text)
                            reason_element = root.find("reason")
                            if reason_element is not None:
                                return False, f"❌ فشل إرسال الكود: {reason_element.text}"
                        except Exception: pass
                        return False, f"❌ فشل إرسال الكود: {response.text[:100]}"
                else:
                    return False, f"❌ فشل إرسال الكود: {response.status_code}"
                    
            except Exception as e:
                return False, f"❌ خطأ في إرسال الكود: {e}"

        # تحقق من صحة رقم الهاتف
        if not re.match(r'^01[0125][0-9]{8}$', phone_number):
            return "❌ رقم الهاتف غير صحيح"

        cleaned_phone = phone_number[1:]  # إزالة الصفر الأول
        
        udid = "089754765cc425f6"
        hcaptcha_token = get_hcaptcha_token_placeholder()
        
        # إرسال رمز التحقق
        success_send, message_send = send_otp_request(cleaned_phone, udid, hcaptcha_token)
        
        if not success_send:
            return message_send
        
        # تخزين البيانات مؤقتاً لاستخدامها في الخطوة التالية
        user_action[chat_id] = {
            'action': 'etisalat_social_number',
            'phone_number': cleaned_phone,
            'udid': udid
        }
        
        return {
            'status': 'need_verification',
            'message': '✅ تم إرسال كود التحقق إلى رقمك. يرجى إدخال الكود (6 أرقام):',
            'phone_number': cleaned_phone,
            'udid': udid
        }
        
    except Exception as e:
        return f"❌ حدث خطأ: {str(e)}"

def complete_etisalat_social_number(phone_number, udid, verification_code, chat_id):
    """
    إكمال عملية تفعيل 500 ميجا سوشيال باستخدام الرقم فقط
    """
    show_progress(chat_id)
    
    try:
        E_KEY = "MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAMPHzaCIoXe5oWoWGzTaRM7PYm4FpzxX5V2sclFixgA4IYjXLP0in1mKgeTjRy2PuqSH/kdQaTV0HujtCZtOXaECAwEAAQ=="
        
        def calculate_hmac_sha512(data, key):
            try:
                key_bytes = key.encode('utf-8')
                data_bytes = data.encode('utf-8')
                mac = hmac.new(key_bytes, data_bytes, hashlib.sha512)
                return mac.hexdigest()
            except Exception as e:
                return None

        def generate_base_headers_list():
            return [
                ("applicationVersion", "2"),
                ("applicationName", "MAB"),
                ("Language", "ar"),
                ("APP-BuildNumber", "10664"),
                ("APP-Version", "33.5.0"),
                ("OS-Type", "Android"),
                ("OS-Version", "15"),
                ("APP-STORE", "GOOGLE"),
                ("C-Type", "WIFI"),
                ("Is-Corporate", "false")
            ]

        def verify_otp_request(phone, udid, otp_code):
            try:
                url = "https://mab.etisalat.com.eg:11003/Saytar/rest/quickAccess/verifyCodeQuickAccess"
                url_path_to_sign = "/Saytar/rest/quickAccess/verifyCodeQuickAccess"
                
                body_xml = f"""<?xml version='1.0' encoding='UTF-8' standalone='yes'?>
        <verifyCodeQuickAccessRequest>
          <dial>{phone}</dial>
          <udid>{udid}</udid>
          <verCode>{otp_code}</verCode>
        </verifyCodeQuickAccessRequest>"""
                
                base_headers_list = generate_base_headers_list()
                header_string_to_sign = ",".join([f"{k} {v}" for k, v in base_headers_list])
                
                header_sig = calculate_hmac_sha512(header_string_to_sign, E_KEY)
                url_sig = calculate_hmac_sha512(url_path_to_sign, E_KEY)
                body_sig = calculate_hmac_sha512(body_xml, E_KEY)
                
                if not all([header_sig, url_sig, body_sig]):
                     return False, "❌ فشل في حساب التواقيع اللازمة."

                headers = {
                    "Accept": "text/xml", "Content-Type": "text/xml; charset=UTF-8",
                    "Host": "mab.etisalat.com.eg:11003", "Connection": "Keep-Alive",
                    "User-Agent": "okhttp/5.0.0-alpha.11",
                }
                headers.update(dict(base_headers_list))
                headers["headerSignature"] = header_sig
                headers["urlSignature"] = url_sig
                headers["bodySignature"] = body_sig
                
                response = requests.post(url, headers=headers, data=body_xml, timeout=15)
                
                if response.status_code == 200:
                    try:
                        root = ET.fromstring(response.text)
                        pass_element = root.find("pass") 
                        if pass_element is not None and pass_element.text:
                            return True, pass_element.text
                        else:
                            reason_element = root.find("reason") 
                            if reason_element is not None:
                                 return False, f"❌ فشل التحقق: {reason_element.text}"
                            return False, "❌ فشل التحقق (الكود المدخل غير صحيح)"
                    except Exception as e:
                        return False, f"❌ فشل تحليل استجابة التحقق: {e}"
                else:
                    return False, f"❌ فشل التحقق من الكود: {response.status_code}"

            except Exception as e:
                return False, f"❌ خطأ في التحقق من الكود: {e}"

        def login_with_otp_token(phone, udid, temp_password):
            try:
                session = requests.Session()
                url = "https://mab.etisalat.com.eg:11003/Saytar/rest/quickAccess/loginQuickAccessWithPlan"
                url_path_to_sign = "/Saytar/rest/quickAccess/loginQuickAccessWithPlan"
                
                body_xml = f"""<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>
        <loginWlQuickAccessRequest>
          <firstLoginAttempt>true</firstLoginAttempt>
          <modelType>SM-A155F</modelType>
          <osVersion>15</osVersion>
          <platform>Android</platform>
          <wlUdid>{udid}</wlUdid>
        </loginWlQuickAccessRequest>"""
                
                auth_string_raw = f"{phone},{udid}:{temp_password}"
                auth_string_b64 = base64.b64encode(auth_string_raw.encode()).decode()
                
                base_headers_list = generate_base_headers_list()
                header_string_to_sign = ",".join([f"{k} {v}" for k, v in base_headers_list])
                
                header_sig = calculate_hmac_sha512(header_string_to_sign, E_KEY)
                url_sig = calculate_hmac_sha512(url_path_to_sign, E_KEY)
                body_sig = calculate_hmac_sha512(body_xml, E_KEY)

                if not all([header_sig, url_sig, body_sig]):
                     return None, None, None, "❌ فشل في حساب التواقيع اللازمة."
                
                headers = {
                    "Accept": "text/xml", "Authorization": f"Basic {auth_string_b64}",
                    "Content-Type": "text/xml; charset=UTF-8", "Host": "mab.etisalat.com.eg:11003",
                    "Connection": "Keep-Alive", "User-Agent": "okhttp/5.0.0-alpha.11",
                }
                headers.update(dict(base_headers_list))
                headers["headerSignature"] = header_sig
                headers["urlSignature"] = url_sig
                headers["bodySignature"] = body_sig
                
                response = session.post(url, headers=headers, data=body_xml, timeout=15)
                
                if response.status_code == 200 and "true" in response.text:
                    cookie = response.headers.get("Set-Cookie", "").split(";")[0] if response.headers.get("Set-Cookie") else None
                    bearer_token = response.headers.get("auth")
                    
                    try:
                        root = ET.fromstring(response.text)
                        msisdn = root.find("dial").text
                    except Exception: 
                        msisdn = None
                        
                    if cookie and bearer_token and msisdn:
                         return cookie, bearer_token, msisdn, session, "✅ تسجيل الدخول ناجح"
                    
                    return None, None, None, None, "❌ نجح الطلب ولكن لم يتم العثور على الكوكيز أو التوكن"

                return None, None, None, None, f"❌ فشل تسجيل الدخول: {response.status_code}"

            except Exception as e:
                return None, None, None, None, f"❌ خطأ في تسجيل الدخول: {e}"

        def generate_headers_from_token(cookie, bearer_token):
            headers = {
                'Host': "mab.etisalat.com.eg:11003",
                'User-Agent': "okhttp/5.0.0-alpha.11", 
                'Content-Type': "text/xml; charset=UTF-8",
                'Accept': "text/xml", 
                'applicationVersion': "3", 
                'applicationName': "MAB",
                'Language': "ar",
                'OS-Type': "Android",
                'OS-Version': "15", 
                'APP-BuildNumber': "10664", 
                'APP-Version': "33.5.0", 
                'Is-Corporate': "false",
                'Cookie': cookie,
                'auth': f"Bearer {bearer_token}",
            }
            return headers

        def activate_social_gift(number, cookie, bearer_token, session):
            try:
                msisdn = number.lstrip("0") if number.startswith("0") else number
                msisdn = ''.join(filter(str.isdigit, msisdn))
                
                url = "https://mab.etisalat.com.eg:11003/Saytar/rest/servicemanagement/submitOrderV2"
                
                headers = generate_headers_from_token(cookie, bearer_token)
                
                data = f"""
                <submitOrderRequest>
                    <mabOperation></mabOperation>
                    <msisdn>{msisdn}</msisdn>
                    <operation>REDEEM</operation>
                    <productName>DOWNLOAD_GIFT_1_SOCIAL_UNITS</productName>
                </submitOrderRequest>
                """
                
                response = session.post(url, headers=headers, data=data, timeout=30)
                response.raise_for_status() 

                if "true" in response.text.lower():
                    return "✅ تم تفعيل 500 ميجا سوشيال بنجاح! 🎉"
                else:
                    try:
                        error_root = ET.fromstring(response.text)
                        reason = error_root.find("reason").text
                        if reason: return f"❌ فشل التفعيل: {reason}"
                    except Exception: pass
                    return f"❌ فشل في التفعيل: {response.text[:100]}"

            except requests.exceptions.HTTPError as e:
                try:
                    error_root = ET.fromstring(e.response.text)
                    reason = error_root.find("reason").text
                    return f"❌ فشل التفعيل: {reason}"
                except:
                     return f"❌ فشل التفعيل: خطأ HTTP {e.response.status_code}."
            except requests.exceptions.Timeout:
                return "❌ انتهى وقت الانتظار"
            except Exception as e:
                return f"❌ خطأ تقني غير متوقع: {str(e)}"

        # التحقق من كود التحقق
        success_verify, result_verify = verify_otp_request(phone_number, udid, verification_code)
        
        if not success_verify:
            return result_verify
        
        temp_password = result_verify
        
        # تسجيل الدخول
        cookie, bearer_token, msisdn, session, login_message = login_with_otp_token(phone_number, udid, temp_password)
        
        if not (cookie and bearer_token and msisdn):
            return login_message
        
        # تفعيل الباقة
        final_result = activate_social_gift(msisdn, cookie, bearer_token, session)
        
        return final_result

    except Exception as e:
        return f"❌ حدث خطأ: {str(e)}"

# ========== معالجات Etisalat Social ==========
@bot.callback_query_handler(func=lambda call: call.data == 'etisalat_social')
def etisalat_social_handler(call):
    """عرض خيارات 500 ميجا سوشيال"""
    if not is_bot_active():
        bot.answer_callback_query(call.id, BOT_DEACTIVATION_MESSAGE, show_alert=True)
        return
        
    keyboard = [
        [InlineKeyboardButton("📧 تفعيل بالميل والباس", callback_data='etisalat_social_email')],
        [InlineKeyboardButton("📱 تفعيل بالرقم فقط", callback_data='etisalat_social_number')],
        [InlineKeyboardButton("🔙 رجوع", callback_data='etisalat')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="📱 *500 ميجا سوشيال - Etisalat*\n\nاختر طريقة التفعيل:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

@bot.callback_query_handler(func=lambda call: call.data == 'etisalat_social_email')
def etisalat_social_email_handler(call):
    """بدء عملية تفعيل بالميل والباس"""
    if not is_bot_active():
        bot.answer_callback_query(call.id, BOT_DEACTIVATION_MESSAGE, show_alert=True)
        return
        
    msg = bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="📧 *تفعيل 500 ميجا سوشيال بالميل والباس*\n\nأرسل البريد الإلكتروني:"
    )
    
    user_action[call.from_user.id] = {'action': 'etisalat_social_email', 'step': 'get_email'}
    bot.register_next_step_handler(msg, process_etisalat_social_email)

def process_etisalat_social_email(message):
    """معالجة البريد الإلكتروني"""
    email = message.text.strip()
    
    if not validate_email(email):
        msg = bot.reply_to(message, "⚠️ البريد الإلكتروني غير صحيح! يرجى إدخال بريد صالح.")
        bot.register_next_step_handler(msg, process_etisalat_social_email)
        return
        
    msg = bot.reply_to(message, "🔑 أدخل كلمة المرور:")
    user_action[message.from_user.id]['step'] = 'get_password'
    user_action[message.from_user.id]['email'] = email
    bot.register_next_step_handler(msg, process_etisalat_social_password)

def process_etisalat_social_password(message):
    """معالجة كلمة المرور"""
    password = message.text.strip()
    user_id = message.from_user.id
    
    if user_id not in user_action or user_action[user_id].get('action') != 'etisalat_social_email':
        bot.reply_to(message, "❌ انتهت الجلسة. يرجى البدء من جديد.")
        return
        
    email = user_action[user_id]['email']
    
    # تنظيف user_action
    del user_action[user_id]
    
    # تنفيذ التفعيل
    result = activate_etisalat_social_email(email, password, message.chat.id)
    
    keyboard = [
        [InlineKeyboardButton("🔄 محاولة أخرى", callback_data='etisalat_social_email')],
        [InlineKeyboardButton("🔙 رجوع", callback_data='etisalat_social')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    bot.send_message(message.chat.id, result, reply_markup=reply_markup)

@bot.callback_query_handler(func=lambda call: call.data == 'etisalat_social_number')
def etisalat_social_number_handler(call):
    """بدء عملية تفعيل بالرقم فقط"""
    if not is_bot_active():
        bot.answer_callback_query(call.id, BOT_DEACTIVATION_MESSAGE, show_alert=True)
        return
        
    msg = bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="📱 *تفعيل 500 ميجا سوشيال بالرقم فقط*\n\nأرسل رقم الهاتف:"
    )
    
    user_action[call.from_user.id] = {'action': 'etisalat_social_number', 'step': 'get_number'}
    bot.register_next_step_handler(msg, process_etisalat_social_number)

def process_etisalat_social_number(message):
    """معالجة رقم الهاتف"""
    number = message.text.strip()
    
    if not validate_phone(number):
        msg = bot.reply_to(message, "⚠️ رقم غير صحيح! يجب أن يبدأ بـ 01 ويتكون من 11 رقماً.")
        bot.register_next_step_handler(msg, process_etisalat_social_number)
        return
        
    result = activate_etisalat_social_number(number, message.chat.id)
    
    if isinstance(result, dict) and result.get('status') == 'need_verification':
        user_action[message.from_user.id]['step'] = 'get_verification'
        user_action[message.from_user.id]['phone_number'] = result['phone_number']
        user_action[message.from_user.id]['udid'] = result['udid']
        
        msg = bot.reply_to(message, result['message'])
        bot.register_next_step_handler(msg, process_etisalat_social_verification)
    else:
        # تنظيف user_action في حالة الخطأ
        if message.from_user.id in user_action:
            del user_action[message.from_user.id]
        
        keyboard = [
            [InlineKeyboardButton("🔄 محاولة أخرى", callback_data='etisalat_social_number')],
            [InlineKeyboardButton("🔙 رجوع", callback_data='etisalat_social')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.send_message(message.chat.id, result, reply_markup=reply_markup)

def process_etisalat_social_verification(message):
    """معالجة كود التحقق"""
    verification_code = message.text.strip()
    user_id = message.from_user.id
    
    if user_id not in user_action or user_action[user_id].get('action') != 'etisalat_social_number':
        bot.reply_to(message, "❌ انتهت الجلسة. يرجى البدء من جديد.")
        return
        
    phone_number = user_action[user_id]['phone_number']
    udid = user_action[user_id]['udid']
    
    # تنظيف user_action
    del user_action[user_id]
    
    # إكمال التفعيل
    result = complete_etisalat_social_number(phone_number, udid, verification_code, message.chat.id)
    
    keyboard = [
        [InlineKeyboardButton("🔄 محاولة أخرى", callback_data='etisalat_social_number')],
        [InlineKeyboardButton("🔙 رجوع", callback_data='etisalat_social')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    bot.send_message(message.chat.id, result, reply_markup=reply_markup)

# ========== معالجات بدء البوت ==========
@bot.message_handler(commands=['start'])
def start_command(message):
    """بدء البوت"""
    if not is_bot_active():
        bot.send_message(message.chat.id, BOT_DEACTIVATION_MESSAGE)
        return
    
    keyboard = [
        [InlineKeyboardButton("📱 اتصالات مصر", callback_data='etisalat')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    bot.send_message(
        message.chat.id,
        'خدمات Etisalat المتاحة:',
        reply_markup=reply_markup
    )

@bot.callback_query_handler(func=lambda call: call.data == 'etisalat')
def etisalat_handler(call):
    """قائمة خدمات اتصالات"""
    if not is_bot_active():
        bot.answer_callback_query(call.id, BOT_DEACTIVATION_MESSAGE, show_alert=True)
        return
        
    keyboard = [
        [InlineKeyboardButton('📱 500 ميجا سوشيال', callback_data='etisalat_social')],
        [InlineKeyboardButton('🔙 رجوع', callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="📱 *خدمات اتصالات مصر*\n\nاختر الخدمة:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

@bot.callback_query_handler(func=lambda call: call.data == 'main_menu')
def main_menu_handler(call):
    """العودة للقائمة الرئيسية"""
    start_command(call.message)

@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    """معالجة الرسائل الأخرى"""
    if message.text == '/start':
        start_command(message)
    else:
        bot.reply_to(message, "❌ أمر غير معروف. استخدم /start للبدء.")

# ========== تشغيل البوت ==========
if __name__ == "__main__":
    print("🚀 بدأ تشغيل البوت...")
    bot.polling(none_stop=True)