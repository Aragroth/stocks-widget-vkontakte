import vk_api

from assets import table_body, table_object, set_interval
from config import companies_to_watch, widget_token, seconds_between_iterations
from stocks_api import StocksAPI

vk_session = vk_api.VkApi(token=widget_token)
vk = vk_session.get_api()

market_data = StocksAPI(companies_to_watch)
market_data.make_icons(vk)

for _ in set_interval(seconds_between_iterations):
    # формируем запрос, который описывает формат виджета

    body_start = "\"body\": ["

    for company_meta in market_data.get_top_companies():
        body_start += table_body.format(*company_meta)

    final_table = table_object.format(body_start)

    t = vk.appWidgets.update(type="table", code=final_table)
