import requests
from bs4 import BeautifulSoup


class StocksAPI:
    """
    Парсит информацию о бирже с сайта yahoo.com
    """
    headers = {'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko)'
                              'Chrome/39.0.2171.95 Safari/537.36')}

    def __init__(self, companies_to_watch):
        self.companies_to_watch = companies_to_watch
        self.stocks = []
        self.companies_icons = {}

    def get_top_companies(self):
        """
        Возвращает топ компаний по капитализации. Каждое
        возвращаемое значение содержит мета-информацию

        :return: список с информацией о компании на текующий момент
        """
        self.stocks = []

        for company_name, company_short in self.companies_to_watch.items():
            company_info = {'company': company_name}

            data = requests.get(f"https://finance.yahoo.com/quote/{company_short}?p={company_short}&.tsrc=fin-srch",
                                headers=type(self).headers).text
            soup = BeautifulSoup(data, features="html.parser")

            company_info['capitalization'] = soup.select('td[data-test="MARKET_CAP-value"]')[0].text
            company_info['current_price'] = soup.select('span[data-reactid="32"]')[0].text
            company_info['change'] = soup.select('span[data-reactid="33"]')[1].text.split(" ")[1][1:-1]

            self.stocks.append(company_info)

        for top_company in sorted(self.stocks, key=self.sorting_by_capital)[::-1][:3]:
            yield [top_company['company'], self.get_icon_url(top_company['company']),
                   '$' + top_company['capitalization'].split('.')[0] + ' B',
                   '$' + top_company['current_price'], top_company['change']]

    @staticmethod
    def sorting_by_capital(x):
        """Преобразует значение капитализции в число"""
        return float(x['capitalization'][:-1])

    def make_icons(self, vk):
        """
        Загружает картинки компаний из папки icons в вк

        :param vk: api клиент для загрузки изображений
        """
        for comp in self.companies_to_watch:
            url = vk.appWidgets.getGroupImageUploadServer(image_type="24x24")['upload_url']

            files = {'image': open(f'icons/{comp}.png', 'rb')}
            answer = requests.post(url, files=files).json()

            uploaded_image = vk.appWidgets.saveGroupImage(**answer)

            self.companies_icons.update({comp: uploaded_image['id']})

    def get_icon_url(self, company_name):
        """Возвращает идентификатор иконки в вк"""
        return self.companies_icons[company_name]
