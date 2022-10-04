from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from requests import Session
from bs4 import BeautifulSoup
from newspaper.models import Article, Image, Tag
from django.utils.text import slugify
import transliterate


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
    return (
        f"https://www.ukrinform.ua{i.get('href')}"
        for i in soup.select('article h2 a')
    )


def worker(queue: Queue):
    while True:
        url = queue.get()
        print('scraping go on', url)
        try:
            with Session() as s:
                response = s.get(url)
                assert response.status_code == 200, "bad response"
        except Exception as error:
            print('ERROR', error)
        # with Lock():
        process(response, url)

        if queue.empty():
            break


def process(resp, url):
    try:
        soup = BeautifulSoup(resp.text, 'html.parser')
        # breakpoint()
        picture = soup.select(".newsImage")[0].get('src')

        # breakpoint()
        name = soup.select("h1")[0].text.strip()
        text = soup.select(".newsText")[0].text.strip()
        tags = [i.text.strip() for i in soup.select(".tags a")]




        article, _ = Article.objects.get_or_create(
            slug=transliterate.translit(name, reversed=True).
            replace(' ', '-').replace('є', 'ye').replace('ї', 'yi'),
            defaults={
                'base_url': url,
                'title': name,
                'text': text,
            }
        )

        for tag in tags:
            t, _ = Tag.objects.get_or_create(
                slug=tag,
                defaults={'name': tag}
            )
            article.tags.add(t)

        with Session() as session:
            img_response = session.get(picture, timeout=10)
            # breakpoint()
        picture_name = picture.split("/")[-1]
        with open(f'media/images/{picture_name}', 'wb') as file:
            file.write(img_response.content)

        image, _ = Image.objects.get_or_create(
            article=article,
            image=f'images/{picture_name}',
            base_url=picture
        )

    except Exception as error:
        print(error)


def main():
    url = 'https://www.ukrinform.ua/rubric-culture/block-lastnews'
    # url = 'https://www.telegraf.in.ua/topviews.html'
    # url = 'https://tsn.ua/news'

    urls_list = create_urls_list(url)
    print(urls_list)

    worker_numb = 5
    # worker_numb = 1

    queue = Queue()


    for url in list(urls_list):
    # for url in list(urls_list)[:1]:
        queue.put(url)
    # print(queue.qsize())

    with ThreadPoolExecutor(max_workers=worker_numb) as tpe:
        for _ in range(worker_numb):
            tpe.submit(worker, queue)


if __name__ == '__main__':
    main()