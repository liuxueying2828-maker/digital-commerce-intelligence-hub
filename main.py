import os
import requests

WEBHOOK_URL = os.getenv("FEISHU_WEBHOOK_URL")

def send_to_feishu(text):
    payload = {
        "msg_type": "text",
        "content": {
            "text": text
        }
    }

    response = requests.post(WEBHOOK_URL, json=payload)
    print(response.status_code)
    print(response.text)

if __name__ == "__main__":
    send_to_feishu("测试成功：AI Morning Brief 已经可以推送到飞书啦。")
