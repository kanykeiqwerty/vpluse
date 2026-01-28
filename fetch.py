import requests
from config import url, headers
import json

import requests

def fetch_html(url, headers=None, params=None, timeout=20, description="данных"):
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=timeout)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Ошибка при загрузке {description}: {e}")
        return None
