import requests
from config import url, headers
import json

def get_html(url=url, params=None):
    try:
        response = requests.get(url, headers=headers, params=params, timeout=20)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Ошибка при запросе: {e}")
        return None


def get_html_det(url, headers=None):
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Ошибка при запросе деталей: {e}")
        return None
    
def get_html_persons(url, headers=None, params=None):
    try:
        response=requests.get(url, headers=headers, params=params, timeout=20)
        response.raise_for_status()
        return response.text
    
    except requests.RequestException as e:
        print((f"ОШибка при загрузки физ лиц: {e}"))
        return None
    
def get_html_persons_det(url, headers=None):
   
    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Ошибка при запросе деталей: {e}")
        return None

