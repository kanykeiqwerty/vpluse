import pandas as pd

def save_to_excel(companies_data=None, individuals_data=None, filename='bankruptcy_data.xlsx'):
    
    
    if not companies_data and not individuals_data:
        print("Нет данных для сохранения")
        return
    
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        
        
        if companies_data:
            df_companies = pd.DataFrame(companies_data)
            df_companies.to_excel(writer, sheet_name='Юридические лица', index=False)
            print(f" Юридические лица: {len(companies_data)} записей")
        
       
        if individuals_data:
            df_individuals = pd.DataFrame(individuals_data)
            df_individuals.to_excel(writer, sheet_name='Физические лица', index=False)
            print(f" Физические лица: {len(individuals_data)} записей")
    
    print(f" Данные сохранены в {filename}")