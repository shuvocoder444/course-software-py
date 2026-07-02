import logging

import requests

from .models import AttendenceSetting

# লগ ট্র্যাকিং সেটআপ (কোনো এরর হলে যাতে কনসোলে দেখা যায়)
logger = logging.getLogger(__name__)

def send_sms(phone_number, message_text):
    """
    JBD IT SMS Gateway এর মাধ্যমে এসএমএস পাঠানোর গ্লোবাল হেল্পার ফাংশন।
    ব্যবহার: send_sms("01712345678", "আপনার ওটিপি কোড হলো ১২৩৪")
    """
    try:
        # ডাটাবেজ থেকে লেটেস্ট টোকেন এবং সেন্ডার আইডি (website_name) তুলে আনা
        settings = AttendenceSetting.objects.first()

        if not settings or not settings.send_id_token:
            logger.error("SMS Failed: Attendance Settings অথবা send_id_token ডাটাবেজে পাওয়া যায়নি।")
            return False, "Settings or Token not configured."

        # JBD IT SMS API Endpoint (আপনার প্রোভাইড করা ডকুমেন্টেশন অনুযায়ী)
        api_url = "https://sms.jbdit.com.bd/smsapi"

        # নাম্বার ফরম্যাট ভ্যালিডেশন (প্রয়োজন হলে সামনে 880 যোগ করার লজিক)
        clean_phone = str(phone_number).strip()
        if not clean_phone.startswith('880') and clean_phone.startswith('01'):
            clean_phone = '88' + clean_phone

        # API-তে পাঠানোর জন্য ডাটা প্যাকিং
        payload = {
            "api_key": settings.send_id_token,      # আপনার send_id_token-ই API Key[cite: 3]
            "type": "text",
            "contacts": clean_phone,
            "senderid": settings.website_name,       # website_name-ই Sender ID[cite: 3]
            "msg": message_text
        }

        # JBD IT সার্ভারে POST রিকোয়েস্ট পাঠানো
        response = requests.post(api_url, data=payload, timeout=10)
        response_data = response.json()

        # রেসপন্স চেক করা (API রিটার্ন স্ট্যাটাস কোড বা সাকসেস মেসেজ অনুযায়ী)
        if response.status_code == 200 and response_data.get("status") == "success":
            logger.info(f"SMS Successfully Sent to {clean_phone}")
            return True, "Success"
        else:
            error_msg = response_data.get("message", "Unknown API Error")
            logger.error(f"SMS API Error: {error_msg}")
            return False, error_msg

    except requests.exceptions.RequestException as req_err:
        logger.error(f"SMS Network Error: {str(req_err)}")
        return False, f"Network Error: {str(req_err)}"

    except Exception as e:
        logger.error(f"SMS Unexpected Error: {str(e)}")
        return False, str(e)
