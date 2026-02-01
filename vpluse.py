from fetch import fetch_html
from parser.list1 import parse_json, get_company_details, get_more_companies_details
from parser.list2 import parse_person, get_persons_details, get_more_persons_details
from ex import save_to_excel
from config import url, urlp, PAGE_SIZE, headers
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch_companies():
    
    print("ЗАГРУЗКА ЮРИДИЧЕСКИХ ЛИЦ")
    companies_data = []
    offset = 0
    
    while True:
        full_url = f"{url}?limit={PAGE_SIZE}&offset={offset}"
        try:
            html_text = fetch_html(full_url, headers=headers)
            parsed_data = parse_json(html_text)
        except Exception as e:
            print(f"Ошибка при загрузке или парсинге компаний: {e}")
            break
        
        print("RAW RESPONSE LENGTH:", len(html_text) if html_text else None)
        print("PARSED:", len(parsed_data))
        
        if not parsed_data:
            print("Больше данных нет, выходим")
            break
        
        companies_data.extend(parsed_data)
        offset += PAGE_SIZE
        print(f"Загружено всего: {len(companies_data)} компаний")
        
        if len(companies_data) >= 1000:
            break
    
    # print(f"\nВсего загружено компаний: {len(companies_data)}")
    return companies_data


def fetch_individuals():
    
    print("ЗАГРУЗКА ФИЗИЧЕСКИХ ЛИЦ")
    individuals_data = []
    offset = 0
    
    while True:
        full_url = f"{urlp}?isActiveLegalCase=null&limit={PAGE_SIZE}&offset={offset}"
        try:
            html_text = fetch_html(full_url, headers=headers)
            parsed_data = parse_person(html_text)
        except Exception as e:
            print(f"Ошибка при загрузке или парсинге физлиц: {e}")
            break
        
        print("RAW RESPONSE LENGTH:", len(html_text) if html_text else None)
        print("PARSED:", len(parsed_data))
        
        if not parsed_data:
            print("Больше данных нет, выходим")
            break
        
        individuals_data.extend(parsed_data)
        offset += PAGE_SIZE
        print(f"Загружено всего: {len(individuals_data)} физлиц")
        
        if len(individuals_data) >= 1000:
            break
    
    # print(f"\nВсего загружено физлиц: {len(individuals_data)}")
    return individuals_data


def load_company_details(company):
    
    guid = company.get('guid')
    if not guid:
        return
    
    try:
        company.update(get_more_companies_details(guid))
        company.update(get_company_details(guid))
    except Exception as e:
        print(f"Ошибка при загрузке деталей компании {guid}: {e}")


def load_all_company_details(companies_data):
    
    print(f"\nНачинаем загрузку деталей для {len(companies_data)} компаний...")
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(load_company_details, comp) for comp in companies_data]
        for i, _ in enumerate(as_completed(futures), 1):
            print(f"[{i}/{len(companies_data)}] компания обработана")
    
    print(f"Загружено деталей компаний: {len(companies_data)}")


def load_person_details(individual):
    
    guid = individual.get('guid')
    if not guid:
        return
    
    try:
        details1 = get_more_persons_details(guid)
        details2 = get_persons_details(guid)
        individual.update(details1)
        individual.update(details2)
    except Exception as e:
        print(f"Ошибка при загрузке деталей физлица {guid}: {e}")


def load_all_individual_details(individuals_data):
    
    print(f"\nНачинаем загрузку деталей для {len(individuals_data)} физлиц...")
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(load_person_details, ind) for ind in individuals_data]
        for i, _ in enumerate(as_completed(futures), 1):
            print(f"[{i}/{len(individuals_data)}] физлицо обработано")
    
    print(f"Загружено деталей физлиц: {len(individuals_data)}")


def main():
    print("main started")
    start_time = time.time()
    
    companies_data = []
    individuals_data = []
    
    try:
        
        print("ЗАГРУЗКА СПИСКОВ")
        
        
        with ThreadPoolExecutor(max_workers=2) as executor:
            future_companies = executor.submit(fetch_companies)
            future_individuals = executor.submit(fetch_individuals)
            
            companies_data = future_companies.result()
            individuals_data = future_individuals.result()
        
        print(f"ИТОГО ЗАГРУЖЕНО:")
        print(f"  Компаний: {len(companies_data)}")
        print(f"  Физлиц: {len(individuals_data)}")
        
        
        
        
        print("ЗАГРУЗКА ДЕТАЛЕЙ")
        
        
        with ThreadPoolExecutor(max_workers=2) as executor:
            future_comp_details = executor.submit(load_all_company_details, companies_data)
            future_ind_details = executor.submit(load_all_individual_details, individuals_data)
            
            future_comp_details.result()
            future_ind_details.result()
        
    except KeyboardInterrupt:
        print("\n\nЗагрузка прервана пользователем")
    except Exception as e:
        print(f"\n\nПроизошла ошибка: {e}")
        import traceback
        traceback.print_exc()
    finally:
        
        
        print("СОХРАНЕНИЕ ДАННЫХ")
        
        print(f"Компаний: {len(companies_data)}")
        print(f"Физлиц: {len(individuals_data)}")
        
        save_to_excel(
            companies_data=companies_data if companies_data else None,
            individuals_data=individuals_data if individuals_data else None
        )
        
        elapsed_time = time.time() - start_time
        print(f"\nГотово. Время выполнения: {elapsed_time:.2f} секунд")


if __name__ == "__main__":
    main()




# from fetch import fetch_html
# from parser.list1 import parse_json, get_company_details, get_more_companies_details
# from parser.list2 import parse_person, get_persons_details, get_more_persons_details
# from ex import save_to_excel
# from config import url, urlp, PAGE_SIZE, headers
# import time
# from concurrent.futures import ThreadPoolExecutor, as_completed


# def main():
   
#     print("main started")
   
    
    
#     companies_data = []
    
#     individuals_data = []
    
#     try:
        
#         print("ЗАГРУЗКА ЮРИДИЧЕСКИХ ЛИЦ")
       
        
#         offset = 0
#         while True:
#             full_url = f"{url}?limit={PAGE_SIZE}&offset={offset}"

#             try:
#                 html_text = fetch_html(full_url, headers=headers)
#                 parsed_data = parse_json(html_text)
#             except Exception as e:
#                 print(f"Ошибка при загрузке или парсинге компаний: {e}")
#                 break

#             print("RAW RESPONSE LENGTH:", len(html_text) if html_text else None)
#             print("PARSED:", len(parsed_data))

#             if not parsed_data:
#                 print("Больше данных нет, выходим")
#                 break

#             companies_data.extend(parsed_data)
#             offset += PAGE_SIZE

#             print(f"Загружено всего: {len(companies_data)} компаний")

#             if len(companies_data) >= 15:
#                 break

       
#         print(f"\nНачинаем загрузку деталей для {len(companies_data)} компаний...")
        
#         def load_company_details(company):
#             guid = company.get('guid')
#             if not guid:
#                 return
#             company.update(get_more_companies_details(guid))
#             company.update(get_company_details(guid))
#         with ThreadPoolExecutor(max_workers=4) as executor:
#             futures = [executor.submit(load_company_details, comp) for comp in companies_data]
#             for i, _ in enumerate(as_completed(futures), 1):
#                 print(f"[{i}/{len(companies_data)}] компания обработана")

#         print(f"\n Загружено компаний: {len(companies_data)}")
        
      
        
#         print("ЗАГРУЗКА ФИЗИЧЕСКИХ ЛИЦ")
      
        
#         offset = 0
#         while True:
            
#             full_url = f"{urlp}?isActiveLegalCase=null&limit={PAGE_SIZE}&offset={offset}"

#             try:
                
#                 html_text = fetch_html(full_url, headers=headers)
#                 parsed_data = parse_person(html_text)
#             except Exception as e:
#                 print(f"Ошибка при загрузке или парсинге физлиц: {e}")
#                 break

#             print("RAW RESPONSE LENGTH:", len(html_text) if html_text else None)
#             print("PARSED:", len(parsed_data))

#             if not parsed_data:
#                 print("Больше данных нет, выходим")
#                 break

#             individuals_data.extend(parsed_data)
#             offset += PAGE_SIZE

#             print(f"Загружено всего: {len(individuals_data)} физлиц")

#             if len(individuals_data) >= 15:
#                 break

#         print(f"\nЗагружено физлиц: {len(individuals_data)}")
        
        
#         print(f"\nНачинаем загрузку деталей для {len(individuals_data)} физлиц...")
#         def load_person_details(individual):
#             guid = individual.get('guid')
#             if not guid:
#                 return

#             details1 = get_more_persons_details(guid)
#             details2 = get_persons_details(guid)

#             individual.update(details1)
#             individual.update(details2)
#         MAX_WORKERS = 5 

#         with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
#             futures = [executor.submit(load_person_details, ind) for ind in individuals_data]

#             for i, _ in enumerate(as_completed(futures), 1):
#                 print(f"[{i}/{len(individuals_data)}] физлицо обработано")

#     except KeyboardInterrupt:
#         print("\nЗагрузка прервана пользователем")

#     except Exception as e:
#         print(f"\nПроизошла ошибка: {e}")
#         import traceback
#         traceback.print_exc()

#     finally:
   
#         print("СОХРАНЕНИЕ ДАННЫХ")
        
#         print(f"Компаний: {len(companies_data)}")
#         print(f"Физлиц: {len(individuals_data)}")
        
#         save_to_excel(
#             companies_data=companies_data if companies_data else None,
#             individuals_data=individuals_data if individuals_data else None
#         )
#         print("Готово.")


# if __name__ == "__main__":
#     main()



