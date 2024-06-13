import json
import requests


def get_access_token():
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=pkxUh545AQffqjCMgQTqr05h&client_secret=4fqXninKKgavWAhWPQQS5OfGoV2evpQP"

    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")


def chat(content):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token=" + get_access_token()
    prompt = "你是一个旅游推荐助手，请结合用户发言用30字左右的话语进行武汉地区的旅游推荐，用户发言是："
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": prompt + content
            }
        ]
    })

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return str(response.json()['result']).replace("\n", ' ')


def rag_for_trip(keywords):
    result = None
    content = "请你根据知识库信息，为具有关键词特征的人进行旅游和购物推荐。" + " ".join(keywords.split())  # 在关键词前加提示语句
    result = chat(keywords)
    return result
