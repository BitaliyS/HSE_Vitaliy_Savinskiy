import requests
from datetime import datetime
from bs4 import BeautifulSoup

# Переменная для хранения данных
data = {}


def get_cbr(date="01.10.2025"):
    url = f"https://www.cbr.ru/currency_base/daily/?UniDbQuery.Posted=True&UniDbQuery.To={date}"
    headers = {'User-Agent': 'Mozilla/5.0'}

    r = requests.get(url, headers=headers)
    html = r.text

    # Парсим HTML с помощью BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    usd_rate = 0
    dkk_rate = 0

    # Ищем таблицу
    table = soup.find('table')
    if table:
        # Ищем строки в таблице
        rows = table.find_all('tr')

        for row in rows:
            cells = row.find_all('td')
            if len(cells) >= 5:
                # Смотрим на ячейки
                code = cells[1].get_text().strip()
                name = cells[3].get_text().strip()
                rate = cells[4].get_text().strip()

                # Ищем USD
                if code == 'USD':
                    usd_rate = float(rate.replace(',', '.'))

                # Ищем DKK
                if code == 'DKK':
                    dkk_rate = float(rate.replace(',', '.'))

    # Сохраняем
    date_obj = datetime.strptime(date, '%d.%m.%Y')
    data[date_obj] = {'USD': usd_rate, 'DKK': dkk_rate}

    print(f"{date}: USD={usd_rate}, DKK={dkk_rate}")


def main():
    get_cbr("01.10.2025")
    get_cbr("30.09.2025")


if __name__ == "__main__":
    main()
