import cloudscraper
from bs4 import BeautifulSoup

def get_data(name):

    print("[+] Fetching data...")
    url = "https://www.dateas.com/es/consulta_cuit_cuil"
    params = { 'name': name, 'cuit':'', 'tipo':'personas-fisicas' }
    scraper = cloudscraper.create_scraper()
    response = scraper.post(url, params)
    soup = BeautifulSoup(response.text, 'lxml')
    items = []

    rows = soup.find('table', {'class': 'data-table'}).find_all('tr')
    for row in rows:
        item = row.find_all('a', {'class': None})
        if len(item) > 0:
            items.append({'name': item[0].text, 'dni': item[1].text})
    return items
        

if __name__ == "__main__":

    while True:
        name = input("[?] Enter a name: ")
        data = get_data(name)
        print("\n")
        for d in data:
            print(f'{d["name"]} - {d["dni"]}')
        c = input("\n[?] Search another? Y/n")
        if c.lower() == 'n':
            break