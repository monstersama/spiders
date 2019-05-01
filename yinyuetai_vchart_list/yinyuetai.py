'''
音悦台音悦V榜，总榜
'''
import json
import time

import requests
import re
import os

from requests import RequestException


def get_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
                      " Chrome/73.0.3683.103 Safari/537.36"
    }
    try:
        response = requests.get(url, timeout=30, headers=headers) #对速度做个限制防止反爬
        if response.status_code == 200:
            return response.text
        return "something wrong"
    except RequestException:
        return None


def get_info(html):
    re_html = re.compile(
        r'''class="score_box">(.*?)</h3>.*?asc-data.*?>(.*?)</span>.*?class="top_num">(.*?)</.*?<img src="(.*?)".*?class="mvname".*?>(.*?)<.*?</em>(.*?)发布时间：(.*?)</p>''',
        re.S)
    re_result = re.findall(re_html, html)
    re_filter_html = re.compile(r'[\s]*<[^>]*>[\s]*', re.S)
    for result in re_result:
        yield {
            'score': re_filter_html.sub('', result[0]),
            'scorech': re_filter_html.sub('', result[1]),
            'rank': result[2],
            'image': result[3],
            'mvname': result[4],
            'aritsts': re_filter_html.sub('', result[5]),
            'publishdata': result[6],
        }


def save_image(content):
    imgs_path = 'imgs'
    img_name = '{}/{}.jpg'.format(imgs_path, content.get('mvname'))
    if not os.path.exists(imgs_path):
        os.makedirs(imgs_path)
    with open(img_name, 'wb+') as f:
        f.write(requests.get('http:' + content.get('image')).content)


def save_to_json(content):
    with open('mv_info.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def run(page):
    url = 'http://vchart.yinyuetai.com/vchart/trends?area=ALL&page=%s' % page
    html = get_page(url)
    contents = get_info(html)
    for content in contents:
        print(content)
        save_image(content)
        save_to_json((content))


if __name__ == '__main__':
    for page in range(1, 4):
        run(page)
        time.sleep(2)
