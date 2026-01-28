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

