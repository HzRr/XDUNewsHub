from flask import Flask, request

from Utils.database import select_news_data, is_content_sql_injection, count_news_data
from config import API_HOST, API_PORT


app = Flask('XDUNewsHubAPI')
app.json.ensure_ascii = False


order_by_map = {
    1: 'id',
    2: 'datetime',
    3: 'title',
    4: 'site_name',
}

order_map = {
    1: 'DESC',
    2: 'ASC'
}


def handle_order(order) -> str:
    orders = []
    while order != 0:
        orders += [order_by_map[order % 10] + ' ' + order_map[int(order / 10) % 10]]
        order = int(order / 100)
    return ', '.join(orders)


@app.route('/')
def index():
    return 'Hello, World!'


@app.route('/get_news', methods=['GET', 'POST'])
def get_news():
    resp = {
        'code': 200,
        'msg': None,
        'total_news': 0,
        'queried_items': []
    }

    num = request.args.get('num')
    start_index = request.args.get('start_index')
    filter_str = request.args.get('filter_str')
    order = request.args.get('order')

    num = 10 if num is None else int(num)
    start_index = 0 if start_index is None else int(start_index)
    filter_str = '' if filter_str is None else filter_str
    order = 12 if order is None else int(order)

    if is_content_sql_injection(filter_str):
        resp['code'] = 400
        resp['msg'] = 'filter_str is invalid'
        return resp

    if filter_str == '':
        filter_str = 'true'
    else:
        filter_str = f"title LIKE '%{filter_str}%' OR site_name LIKE '%{filter_str}%'"

    if len(str(order)) % 2 != 0:
        resp['code'] = 400
        resp['msg'] = 'order is invalid'
        return resp
    else:
        order_str = handle_order(order)

    if start_index < 0:
        resp['code'] = 400
        resp['msg'] = 'start_index is invalid'
        return resp
    if num < 0:
        resp['code'] = 400
        resp['msg'] = 'num is invalid'
        return resp

    limit_str = f'{num} OFFSET {start_index}'

    news_data_list = select_news_data(filter_str, order_str, limit_str)

    resp['msg'] = 'success'
    resp['total_news'] = count_news_data()
    for news_data in news_data_list:
        news_data.update({'timestamp': news_data['UNIX_TIMESTAMP(datetime)']})
        news_data.pop('UNIX_TIMESTAMP(datetime)', None)
    resp['queried_items'] = news_data_list

    return resp


if __name__ == '__main__':
    app.run(host=API_HOST, port=API_PORT)
