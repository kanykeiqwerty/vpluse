from datetime import datetime
import json
from bs4 import BeautifulSoup as BS
import html
from fetch import fetch_html
from config import urld, urlpd, headers_variants
from .dop import parse_iso_date, get_publications_count, get_trades_count


def parse_json(html_text):
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
    for item in items:




        case_number = ''
        arbitr_manager = ''
        status_description = ''
        
        status_date = ''

        if 'lastLegalCase' in item and item['lastLegalCase']:
            legal_case = item['lastLegalCase']
            case_number = legal_case.get('number', '')
            arbitr_manager = legal_case.get('arbitrManagerFio', '')
            
            if 'status' in legal_case and legal_case['status']:
                status_obj = legal_case['status']
                status_description = status_obj.get('description', '')
                status_date = status_obj.get('date', '')


        parsed_data.append({
            'guid': item.get('guid'),
            'Полное наименование': BS(html.unescape(item.get('name', '')), 'html.parser').text,
            'ИНН': item.get('inn', ''),
            'ОГРН': item.get('ogrn', ''),
            'Статус': item.get('status', ''),
            'Регион': item.get('region', ''),
            'Адрес': item.get('address', ''),
            'Тип процедуры': status_description, 
            'Номер судебного дела': case_number,
            'Статус дела' : item.get('isActive', ''),
            'Дата завершение производства': parse_iso_date(status_date),
            'ФИО арбитражного управляющего': arbitr_manager,
            'ИНН управляющего': None,
            'Дата внесения данных в ЕГРЮЛ': parse_iso_date(item.get('statusUpdateDate', ''))
            
        })
    
    return parsed_data


def get_company_details(guid):
    
    url_detail = f"{urld}/{guid}"
    
    html_text = fetch_html(url_detail, headers=headers_variants)
    
    if not html_text:
        print(f"Пустой ответ для {guid}")
        return {}

    try:
        item = json.loads(html_text)


        okopf_name = ''
        
        if 'okopf' in item and item['okopf']:
            okopf_name = item['okopf'].get('name', '')
            
        
        
        okved_name = ''
        
        if 'okved' in item and item['okved']:
            okved_name = item['okved'].get('name', '')
           
        return {
            'КПП': item.get('kpp', ''),
            'Уставный капитал': item.get("authorizedCapital", ''),
            'Дата регистрации': parse_iso_date(item.get('dateReg', '')),
            'Правовая форма(ОКОПФ)': okopf_name,
            'Виде деятельности(ОКВЭД)':okved_name,
            
            
            'Кол-во публикаций': get_publications_count(guid, headers=headers_variants),
            'Кол-во торгов':get_trades_count(guid, headers=headers_variants),
            'URL карточки':url_detail,



        }
    except json.JSONDecodeError:
        print(f"Не JSON для {guid}, первые 200 символов: {html_text[:200]}")
        return {}
    except Exception as e:
        print(f"Ошибка обработки данных для {guid}: {e}")
        return {}

