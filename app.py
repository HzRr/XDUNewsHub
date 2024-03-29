import streamlit as st
import requests

from Struct import NewsData
from config import PAGE_NEWS_LIMIT, GET_NEWS_API_URL

import datetime


st.set_page_config(page_title="XDUNewsHub",
                   layout="wide",
                   menu_items={
                       'Get Help': 'https://github.com/HzRr/XDUNewsHub/issues',
                       'Report a bug': 'https://github.com/HzRr/XDUNewsHub/issues',
                       'About': '# XDUNewsHub'
                   })


def build_news_table(news_data_list: list[NewsData]):
    # 开始构建HTML字符串
    html_str = """
    <style>
        .news-table {
            width: 100%;
            border-collapse: collapse;
        }
        .news-table th, .news-table td {
            text-align: left;
            padding: 8px;
            /* 删除表格边框 */
            border: none;
        }
        .news-table th {border-bottom: 2px solid #000;}
        .news-table th {border-top: 2px solid #000;}
    </style>
    <table class="news-table">
        <thead>
            <tr>
                <th>新闻标题</th>
                <th>来源</th>
                <th>日期</th>
            </tr>
        </thead>
        <tbody>
    """

    for news_data in news_data_list:
        formatted_time = datetime.datetime.fromtimestamp(news_data.timestamp).strftime("%Y-%m-%d")
        html_str += f"""<tr style="color: #4B4B4B;">
        <td><a style="color: #4B4B4B; text-decoration: none;" href="{news_data.url}">{news_data.title}</a></td>
        <td><a style="color: #4B4B4B; text-decoration: none;" href="{news_data.site_url}">{news_data.site_name}</a></td>
        <td>{formatted_time}</td></tr>"""

    html_str += """
        </tbody>
    </table>
    """

    # 使用st.markdown渲染HTML，确保unsafe_allow_html=True
    st.markdown(html_str, unsafe_allow_html=True)


def update_news_table(queried_items: list) -> None:
    news_data_list = []
    for item in queried_items:
        news_data = NewsData()
        news_data.url = item['url']
        news_data.title = item['title']
        news_data.timestamp = item['timestamp']
        news_data.site_name = item['site_name']
        news_data.site_url = item['site_url']

        news_data_list.append(news_data)

    build_news_table(news_data_list)


def query_news(post_params: dict) -> list:
    raw_resp = requests.post(GET_NEWS_API_URL, params=post_params)
    if raw_resp.status_code == 200:
        # TODO: print total_news, page_news_num
        resp = raw_resp.json()
        return resp['queried_items']
    else:
        # TODO: else condition
        print(raw_resp)
        pass


params = {
    "num": PAGE_NEWS_LIMIT,
}

update_news_table(query_news(params))
