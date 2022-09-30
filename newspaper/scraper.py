from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from requests import Session
from bs4 import BeautifulSoup


def create_urls_list(link):
    print('create_urls_list')
    with Session() as session:
        print('Session')
        response = session.get(link)
        # print(response)
        assert response.status_code == 200, 'bad response'

    soup = BeautifulSoup(response.content, 'html.parser')
    # breakpoint()
    # print(soup)
    return (i.get('href') for i in soup.select(".c-card__link"))


def worker(queue: Queue):
    while queue:
        url = queue.get()
        print('scraping go on', url)
        try:
            with Session() as s:
                response = s.get(url)
                assert response.status_code == 200, "bad response"
        except Exception as error:
            print('ERROR', error)

        process(response)


def process(resp):
    soup = BeautifulSoup(resp.text)
    # breakpoint()
    name = soup.select('h1')[0].text.strip()
    picture = soup.select('picture img')[0].get('src')
    print(name)
    print(picture)
    # breakpoint()



def main():
    url = 'https://tsn.ua/news'

    urls_list = create_urls_list(url)
    # print(urls_list)
    worker_numb = 1
    queue = Queue()

    for url in list(urls_list)[:5]:
        queue.put(url)
    # print(queue.qsize())
    for _ in range(worker_numb):
        with ThreadPoolExecutor() as tpe:
            tpe.submit(worker, queue)


if __name__ == '__main__':
    main()