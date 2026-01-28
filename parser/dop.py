from datetime import datetime
import json
from bs4 import BeautifulSoup as BS
import html
# from fetch import get_html_det, get_html_persons_det
from config import urld, urlpd, headers_variants

def parse_iso_date(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace('Z', ''))
    except Exception:
        return None
    

import requests

def get_publications_count(guid, headers=None):
    try:
        url = f"https://fedresurs.ru/backend/companies/{guid}/publications?limit=1&offset=0"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        # Важно: смотрим, где лежит общее количество
        # Например, data.get('total') или data.get('totalCount')
        total = data.get('found') or data.get('totalCount') or len(data.get('pageData', []))
        return total
    except Exception as e:
        print(f"Не удалось получить публикации для {guid}: {e}")
        return 0
    

def get_trades_count(guid, headers=None):
    try:
        url = f"https://fedresurs.ru/backend/biddings?bankruptGuid={guid}&limit=1&offset=0"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        # Важно: смотрим, где лежит общее количество
        # Например, data.get('total') или data.get('totalCount')
        total = data.get('found') or data.get('totalCount') or len(data.get('pageData', []))
        return total
    except Exception as e:
        print(f"Не удалось получить публикации для {guid}: {e}")
        return 0
