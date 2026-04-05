import json
import requests

BOT_TOKEN = "8555752277:AAFrP1pMnEdOW9TUVK2PM9_XoGNZzv01VCw"
WEBAPP_URL = "https://guanggaohb.asia/MiniAPP"

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print("发送失败:", e)

def send_menu(chat_id):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    keyboard = {
        "inline_keyboard": [
            [
                {"text": "📁 打开资源站", "web_app": {"url": WEBAPP_URL}},
                {"text": "❓ 帮助", "callback_data": "help"}
            ]
        ]
    }
    payload = {
        "chat_id": chat_id,
        "text": "欢迎使用资源站！点击下方按钮打开应用：",
        "reply_markup": json.dumps(keyboard)
    }
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print("发送菜单失败:", e)

def handle_callback(callback_query):
    chat_id = callback_query["message"]["chat"]["id"]
    data = callback_query.get("data")
    if data == "help":
        help_text = "📖 帮助\n\n点击「打开资源站」进入应用，可上传/下载文件。"
        send_message(chat_id, help_text)
    answer_url = f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery"
    requests.post(answer_url, json={"callback_query_id": callback_query["id"]})

def main(request):
    try:
        body = request.get_json()
    except:
        return {"statusCode": 200, "body": "ok"}
    if not body:
        return {"statusCode": 200, "body": "ok"}
    
    if "message" in body:
        msg = body["message"]
        chat_id = msg["chat"]["id"]
        text = msg.get("text", "")
        if text == "/start":
            send_menu(chat_id)
        elif text == "/menu":
            send_menu(chat_id)
        else:
            send_message(chat_id, "请使用菜单按钮打开资源站。发送 /start 显示菜单。")
    
    if "callback_query" in body:
        handle_callback(body["callback_query"])
    
    return {"statusCode": 200, "body": "ok"}