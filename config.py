url='https://bankrot.fedresurs.ru/backend/cmpbankrupts'
urld='https://fedresurs.ru/backend/companies'
urlpd='https://fedresurs.ru/backend/persons'
urlp='https://bankrot.fedresurs.ru/backend/prsnbankrupts'


headers = {
    "User-Agent": "Browser",
    "Accept": "application/json, text/plain, */*",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://bankrot.fedresurs.ru/bankrupts",  
    "Origin": "https://bankrot.fedresurs.ru",
}

PAGE_SIZE=15

headers_variants = {
    
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://fedresurs.ru/',
    'Origin': 'https://fedresurs.ru',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
}

