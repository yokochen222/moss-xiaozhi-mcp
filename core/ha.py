import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv('HA_ADDRESS')
HA_TOKEN = os.getenv('HA_AUTH_TOKEN')

# 发送请求到Home Assistant
def ha_requet(url, method = 'GET', data = {}):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {HA_TOKEN}'
    }
    full_url = BASE_URL + url
    response = requests.request(method, full_url, headers=headers, json=data)
    
    # 检查响应状态
    if response.status_code != 200:
        return {"error": f"HTTP {response.status_code}: {response.text}"}
    
    # 尝试解析 JSON
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError as e:
        return {"error": f"JSON 解析错误: {e}", "raw_response": response.text}
