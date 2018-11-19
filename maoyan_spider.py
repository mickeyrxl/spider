import json
import re
from multiprocessing.pool import Pool
import requests
from requests import RequestException


# handle one page
def get_page(url):
    # avoid 403 forbidden, set headers
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.'
                             '0.3538.77 Safari/537.36'}
    response = requests.get(url, headers=headers)
    try:
        if response.status_code == 200:
            return response.content.decode('utf-8')
        else:
            return None
    except RequestException:
        return None

# parse html using regular expression
# return an iter by yield
def parse_html(html):
    pattern = re.compile('<dd>.*?"name".*?">(.*?)</a>.*?"star">(.*?)</p>.*?"releasetime">(.*?)</p>', re.S)
    data = re.findall(pattern, html)
    for item in data:
        yield {
            'name': item[0],
            'actors': item[1][3:],
            'date': item[2][5:]
        }


def save_to_file(data):
    with open('expectance.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False)+'\n')


def main(offset):
    url = 'http://maoyan.com/board/6?offset='+str(offset)
    html = get_page(url)
    for item in parse_html(html):
        save_to_file(item)

# multiprocessing pool
if __name__ == '__main__':
    pool = Pool()
    pool.map(main, [i*10 for i in range(10)])
    pool.close()
