import requests
import json

url = "https://bankrot.fedresurs.ru/backend/prsnbankrupts"

headers = {
    "User-Agent": "Browser",
    "Accept": "application/json, text/plain, */*",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://bankrot.fedresurs.ru/bankrupts",  
    "Origin": "https://bankrot.fedresurs.ru",
}

print("="*80)
print("ТЕСТ СТРУКТУРЫ ДАННЫХ ФИЗИЧЕСКИХ ЛИЦ")
print("="*80)
print(f"\nURL: {url}\n")

try:
    response = requests.get(url, headers=headers, timeout=20)
    print(f"✓ Статус: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ JSON валидный")
        print(f"✓ Ключи в ответе: {list(data.keys())}\n")
        
        if 'pageData' in data:
            print(f"✓ Найдено записей: {len(data['pageData'])}\n")
            
            if len(data['pageData']) > 0:
                print("="*80)
                print("ПРИМЕР ПЕРВОЙ ЗАПИСИ:")
                print("="*80)
                person = data['pageData'][0]
                print(json.dumps(person, ensure_ascii=False, indent=2))
                
                print("\n" + "="*80)
                print("ДОСТУПНЫЕ ПОЛЯ:")
                print("="*80)
                for key in person.keys():
                    value = person.get(key)
                    if isinstance(value, dict):
                        print(f"  {key}: (объект) → {list(value.keys())}")
                    elif isinstance(value, list):
                        print(f"  {key}: (список)")
                    else:
                        print(f"  {key}: {value}")
                
                # Тест детального API
                guid = person.get('guid')
                if guid:
                    print("\n" + "="*80)
                    print("ТЕСТ ДЕТАЛЬНОГО API")
                    print("="*80)
                    print(f"GUID: {guid}\n")
                    
                    detail_url = f"https://fedresurs.ru/backend/persons/{guid}"
                    headers_detail = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                        'Accept': 'application/json, text/plain, */*',
                        'Referer': 'https://fedresurs.ru/',
                        'Origin': 'https://fedresurs.ru',
                    }
                    
                    response2 = requests.get(detail_url, headers=headers_detail, timeout=10)
                    print(f"Статус: {response2.status_code}")
                    
                    if response2.status_code == 200:
                        detail_data = response2.json()
                        print(f"\n✅ ДЕТАЛЬНЫЙ API РАБОТАЕТ!\n")
                        print("Детальная информация:")
                        print(json.dumps(detail_data, ensure_ascii=False, indent=2))
                        
                        print("\n" + "="*80)
                        print("ПОЛЯ В ДЕТАЛЬНОМ API:")
                        print("="*80)
                        for key in detail_data.keys():
                            print(f"  {key}")
                    else:
                        print(f"❌ Детальный API вернул: {response2.status_code}")
                        print(f"Попробуйте другой URL или детальный API не нужен")
        else:
            print("⚠️ pageData отсутствует в ответе")
            
    else:
        print(f"❌ Ошибка: {response.status_code}")
        print(response.text[:500])
        
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*80)