"""
猫眼近期热映电影
python 3.6
"""
import json
import os
import requests
import re
import time
from requests import RequestException


def get_page(url):
    '''
    请求页面
    :param url:
    :return:
    '''
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
                      " Chrome/73.0.3683.103 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=header)
        if response.status_code == 200:
            return response.text
        else:
            return "something wrong"
    except RequestException:
        return None

def get_info(html):
    '''
    提取电影信息
    :param html:
    :return:
    '''
    re_str = re.compile(r'poster-default.*?<img\s+data-src="(.*?)".*?title="(.*?)">.*?orange">(.*?)</div>', re.S)
    infos = re.findall(re_str, html)
    re_html = re.compile(r'<[^>]+>')
    # print(infos)
    for info in infos:
        yield {
            'image': info[0],
            'name': info[1],
            'score': re_html.sub('', info[2])
        }

def write_to_json(content):
    '''
    将热映电影的信息以保存为json格式的信息
    :param content:
    :return:
    '''
    print(type(json.dumps(content)))
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')

def download_image(content):
    '''
    将电影封面保存到imgs目录下
    :param content:
    :return:
    '''
    imgs_path = 'imgs'
    img_name = ('{}/{}.jpg'.format(imgs_path, content.get('name')))
    if os.path.exists(imgs_path):
        pass
    else:
        os.makedirs(imgs_path)
    with open(img_name, 'wb+') as f:
        f.write(requests.get(content.get('image')).content)

def run(offset):
    '''
    开启翻页
    :param offset: 翻页,一次翻页为30
    :return:
    '''
    url = "https://maoyan.com/films?showType=1&offset=%s"%offset
    html = get_page(url)
    print(os.getcwd())
    for i in get_info(html):
        print(i)
        download_image(i)
        write_to_json(i)



if __name__ == "__main__":
    for page in range(0, 2):
        run(offset=page*30)
        time.sleep(1)  # 速度过快会被反爬发现

