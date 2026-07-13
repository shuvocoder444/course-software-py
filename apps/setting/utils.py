import logging

import requests

from .models import AttendenceSetting

# লগ ট্র্যাকিং সেটআপ
logger = logging.getLogger(__name__)

def send_sms(phone_number, message_text):
    """
    JBD IT New JSON SMS API এর মাধ্যমে এসএমএস পাঠানোর গ্লোবাল হেল্পার ফাংশন।
    """
    try:
        # ডাটাবেজ থেকে লেটেস্ট টোকেন এবং সেন্ডার আইডি (website_name) তুলে আনা
        settings = AttendenceSetting.objects.first()

        if not settings or not settings.send_id_token:
            logger.error("SMS Failed: Attendance Settings অথবা send_id_token ডাটাবেজে পাওয়া যায়নি।")
            return False, "Settings or Token not configured."

        # 🟢 JBD IT এর নতুন সঠিক API এন্ডপয়েন্ট ইউআরএল
        api_url = "https://sms.jbdit.net/api/http/sms/send"

        # নাম্বার ফরম্যাট ভ্যালিডেশন (প্রয়োজন হলে সামনে 880 যোগ করার লজিক)
        clean_phone = str(phone_number).strip()
        if not clean_phone.startswith('880') and clean_phone.startswith('01'):
            clean_phone = '88' + clean_phone

        # 🟢 নতুন রিকোয়েস্ট হেডার (JSON ডেটার জন্য)
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        # 🟢 নতুন এপিআই অনুযায়ী ডাটা স্ট্রাকচার (Payload)
        payload = {
            "api_token": settings.send_id_token,      # আপনার send_id_token-ই api_token
            "recipient": clean_phone,                #contacts এর বদলে recipient
            "sender_id": settings.website_name,       # senderid এর বদলে sender_id
            "type": "plain",                          # text এর বদলে plain
            "message": message_text                   # msg এর বদলে message
        }

        # 🟢 ডেটা json=payload হিসেবে POST করা হচ্ছে
        response = requests.post(api_url, json=payload, headers=headers, timeout=10)

        # ডিবাগিং প্রিন্ট: টার্মিনালে চেক করার জন্য
        print("--- SMS GATEWAY DEBUG START ---")
        print("Status Code:", response.status_code)
        print("Response Text:", response.text)
        print("--- SMS GATEWAY DEBUG END ---")

        response_data = response.json()

        # নতুন এপিআই এর রেসপন্স চেক করা
        if response.status_code == 200 and response_data.get("status") == "success":
            logger.info(f"SMS Successfully Sent to {clean_phone}")
            return True, "Success"
        else:
            error_msg = response_data.get("error_message") or response_data.get("message") or "Unknown API Error"
            logger.error(f"SMS API Error: {error_msg}")
            return False, error_msg

    except requests.exceptions.RequestException as req_err:
        logger.error(f"SMS Network Error: {str(req_err)}")
        return False, f"Network Error: {str(req_err)}"

    except Exception as e:
        logger.error(f"SMS Unexpected Error: {str(e)}")
        return False, str(e)
