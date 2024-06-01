import json
import requests

def get_access_token():
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=i2EVEdXSA0AIDOp2GWm5Kjxm&client_secret=zdVpEb1x8gYAKnhoskPHdAYlFLDVGPhg"

    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")


def chat(content):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token=" + get_access_token()

    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": content
            }
        ]
    })

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()['result']

def rag_for_trip(keywords):
    result = None
    content = "请你根据知识库信息，为具有关键词特征的人进行旅游和购物推荐。" + " ".join(keywords.split())  # 在关键词前加提示语句
    result = chat(keywords)
    return result

if __name__ == '__main__':
    string = rag_for_trip("夏天去哪里比较好")
    print(string)

