from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from requests import Session
from bs4 import BeautifulSoup
from newspaper.models import Article, Image, Tag, Category
from django.utils.text import slugify
import transliterate


def create_category_urls(link):
    print('create_category_urls')
    with Session() as session:
        print('Session')
        response = session.get(link)
        # print(response)
        assert response.status_code == 200, 'bad response'

    soup = BeautifulSoup(response.content, 'html.parser')
    # breakpoint()

    return [
        {'url': f"https://www.ukrinform.ua{i.get('href')}/block-lastnews",
         'category_name': i.text.strip()}
        for i in soup.select('.leftMenu a')
    ]


def create_article_urls(link):
    print('create_article_urls')
    with Session() as session:
        print('Session')
        response = session.get(link)
        # print(response)
        assert response.status_code == 200, 'bad response'

    soup = BeautifulSoup(response.content, 'html.parser')
    # breakpoint()

    return (
        f"https://www.ukrinform.ua{i.get('href')}"
        for i in soup.select('article h2 a') if not i.get('href').startswith('https://')
    )

def worker(queue: Queue):
    while True:
        url, category_name = queue.get()
        print('scraping go on', url)
        try:
            with Session() as s:
                response = s.get(url)
                assert response.status_code == 200, "bad response"
        except Exception as error:
            print('ERROR', error)
        # with Lock():
        process(response, url, category_name)

        if queue.empty():
            break


def process(resp, url, category_name):
    try:
        soup = BeautifulSoup(resp.text, 'html.parser')
        # breakpoint()
        picture = soup.select(".newsImage")[0].get('src')

        # breakpoint()
        name = soup.select("h1")[0].text.strip()
        description = soup.select('.newsHeading')[0].text.strip()
        text = soup.select(".newsText p")
        text = ''.join([f'<p>{item.text.strip()}</p>' for item in text])
        # breakpoint()
        tags = [i.text.strip() for i in soup.select(".tags a")]
        date = soup.select(".newsDate")[0].text.strip()

        date = '-'.join(date.split()[0].split('.')[::-1]) + ' ' + date.split()[1]
        # breakpoint()
        category, _ = Category.objects.get_or_create(
            name=category_name,
            slug=f"{url.split('/')[-2]}"
        )

        article, _ = Article.objects.get_or_create(
            slug=slugify(transliterate.translit(name,reversed=True).
                    lower().replace(' ','-').
                    replace('є', 'ye').replace('ї', 'yi').replace('і', 'i')),
            defaults={
                'base_url': url,
                'title': name,
                'text': text,
                'category': category,
                'date_news': date,
                'description': description
            }
        )

        for tag in tags:
            slug = slugify(transliterate.translit(tag,reversed=True).
                    lower().replace(' ','-').
                    replace('є', 'ye').replace('ї', 'yi').replace('і', 'i'))
            t, _ = Tag.objects.get_or_create(
                slug=f"tag-{slug}",
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
    url = 'https://www.ukrinform.ua'
    # url = 'https://www.ukrinform.ua/rubric-culture/block-lastnews'
    # url = 'https://www.telegraf.in.ua/topviews.html'
    # url = 'https://tsn.ua/news'
    category_urls = create_category_urls(url)
    # for dict_ in category_urls[:1]:
    for dict_ in category_urls:

        article_urls = create_article_urls(dict_['url'])
     
        worker_numb = 5
        # worker_numb = 1

        queue = Queue()


        for url in list(article_urls)[:10]:
        # for url in list(article_urls)[:1]:
            queue.put((url, dict_['category_name']))


        with ThreadPoolExecutor(max_workers=worker_numb) as tpe:
            for _ in range(worker_numb):
                tpe.submit(worker, queue)


if __name__ == '__main__':
    main()
