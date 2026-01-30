from datetime import datetime
import json
from bs4 import BeautifulSoup as BS
import html
from fetch import fetch_html
from config import urld, urlpd, headers_variants
from .dop import parse_iso_date, get_publications_count, get_trades_count


def parse_person(html_text):
    if not html_text:
        print("html_text пустой")
        return []

    try:
        data = json.loads(html_text)
    except Exception as e:
        print("НЕ JSON! Вот первые 500 символов:")
        print(html_text[:500])
        raise
    
    print("JSON keys:", data.keys())
    items = data.get('pageData', [])
    print("pageData len:", len(items))
    
    parsed_data = []
    seen_ids = set()
    for item in items:
        guid = item.get('guid')
        if not guid:
            continue
        if guid in seen_ids:
            continue

        seen_ids.add(guid)




        case_number = ''
        arbitr_manager = ''
        status_description = ''
        
        

        if 'lastLegalCase' in item and item['lastLegalCase']:
            legal_case = item['lastLegalCase']
            case_number = legal_case.get('number', '')
            arbitr_manager = legal_case.get('arbitrManagerFio', '')
            
            if 'status' in legal_case and legal_case['status']:
                status_obj = legal_case['status']
                status_description = status_obj.get('description', '')
                
        

        parsed_data.append({
            'guid': guid,
            'ФИО': item.get('fio', ''),
            'СНИЛС': item.get('snils', ''),
            
            
            'Регион': item.get('region', ''),
            'Адрес проживания': item.get('address', ''),
            'Тип процедуры': status_description, 
            'Номер дела': case_number,
            
            
            'Управляющий': arbitr_manager,
           
            
        })
    
    return parsed_data



def get_persons_details(guid):
    url_detail = f"{urlpd}/{guid}/individual-entrepreneurs?limit=1&offset=0"
    html_text = fetch_html(url_detail, headers=headers_variants)

    if not html_text:
        print(f"Пустой ответ для {guid}")
        return {}

    try:
        data = json.loads(html_text)

        items = data.get('pageData', [])
        if not items:
            print(f"Нет ИП данных для {guid}")
            return {}

        item = items[0]  

        status = item.get('status', {}) or {}
        okved = item.get('okved', {}) or {}

        return {
            'ОГРНИП': item.get('ogrnip', ''),
            'Статус ИП': status.get('name', ''),
            'Вид деятельности': okved.get('name', ''),
            'Дата регистрации ИП': parse_iso_date(item.get('dateReg', '')),
            'Дата прекращения деятельности': parse_iso_date(status.get('date', '')),
            'Статус банкротства': status.get('isActive', ''),
            
            
            'URL карточки': url_detail,
        }

    except json.JSONDecodeError:
        print(f"Не JSON для {guid}, первые 200 символов: {html_text[:200]}")
        return {}
    except Exception as e:
        print(f"Ошибка обработки данных для {guid}: {e}")
        return {}

    

def get_more_persons_details(guid):
    """Получение полной информации по guid"""
    url_detail = f"{urlpd}/{guid}"
    html_text = fetch_html(url_detail, headers=headers_variants)
    
    if not html_text:
        print(f"Пустой ответ для {guid}")
        return {}

    try:
        item = json.loads(html_text)

        return{
            'Дата рождения': parse_iso_date(item.get('birthdateBankruptcy', '')), 
            'Место рождения': item.get('birthplaceBankruptcy', ''),
        }


    except json.JSONDecodeError:
        print(f"Не JSON для {guid}, первые 200 символов: {html_text[:200]}")
        return {}
    except Exception as e:
        print(f"Ошибка обработки данных для {guid}: {e}")
        return {}
    


