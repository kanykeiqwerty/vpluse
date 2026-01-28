
from datetime import datetime
import json
from bs4 import BeautifulSoup as BS
import html
from fetch import get_html_det, get_html_persons_det
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
            'FullName': BS(html.unescape(item.get('name', '')), 'html.parser').text,
            'INN': item.get('inn', ''),
            'OGRN': item.get('ogrn', ''),
            'Status': item.get('status', ''),
            'Region': item.get('region', ''),
            'Address': item.get('address', ''),
            'ProcedureType': status_description, 
            'CaseNumber': case_number,
            'CaseStatus' : item.get('isActive', ''),
            'CaseEndDate': parse_iso_date(status_date),
            'ArbitrationManagerName': arbitr_manager,
            'ArbitrationManagerINN': None,
            'ManagerAppointmentDate': parse_iso_date(item.get('statusUpdateDate', ''))
            
        })
    
    return parsed_data


def get_company_details(guid):
    
    url_detail = f"{urld}/{guid}"
    
    html_text = get_html_det(url_detail, headers=headers_variants)
    
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
            'KPP': item.get('kpp', ''),
            'AuthorizedCapital': item.get("authorizedCapital", ''),
            'RegistrationDate': parse_iso_date(item.get('dateReg', '')),
            'LegalForm': okopf_name,
            'OKVED':okved_name,
            
            
            'PublicationsCount': get_publications_count(guid, headers=headers_variants),
            'TradesCount':get_trades_count(guid, headers=headers_variants),
            'SourceURL':url_detail,



        }
    except json.JSONDecodeError:
        print(f"Не JSON для {guid}, первые 200 символов: {html_text[:200]}")
        return {}
    except Exception as e:
        print(f"Ошибка обработки данных для {guid}: {e}")
        return {}


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
    for item in items:




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
            'guid': item.get('guid'),
            'FullName': item.get('fio', ''),
            'SNILS': item.get('snils', ''),
            
            
            'Region': item.get('region', ''),
            'ResidenceAddress': item.get('address', ''),
            'ProcedureType': status_description, 
            'CaseNumber': case_number,
            
            
            'ArbitrationManagerName': arbitr_manager,
           
            
        })
    
    return parsed_data



def get_persons_details(guid):
    url_detail = f"{urlpd}/{guid}/individual-entrepreneurs?limit=1&offset=0"
    html_text = get_html_persons_det(url_detail, headers=headers_variants)

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
            'EntrepreneurOGRNIP': item.get('ogrnip', ''),
            'RegistrationDate': parse_iso_date(item.get('dateReg', '')),
            'TerminationDate': parse_iso_date(status.get('date', '')),
            'BankruptcyStatus': status.get('isActive', ''),
            'EntrepreneurStatus': status.get('name', ''),
            'OKVED': okved.get('name', ''),
            'SourceURL': url_detail,
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
    html_text = get_html_persons_det(url_detail, headers=headers_variants)
    
    if not html_text:
        print(f"Пустой ответ для {guid}")
        return {}

    try:
        item = json.loads(html_text)

        return{
            'BirthDate': parse_iso_date(item.get('birthdateBankruptcy', '')), 
            'BirthPlace': item.get('birthplaceBankruptcy', ''),
        }


    except json.JSONDecodeError:
        print(f"Не JSON для {guid}, первые 200 символов: {html_text[:200]}")
        return {}
    except Exception as e:
        print(f"Ошибка обработки данных для {guid}: {e}")
        return {}
    


