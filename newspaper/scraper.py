import random
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

from django.db.transaction import atomic
from requests import Session
from bs4 import BeautifulSoup
from newspaper.models import Article, Image, Tag, Category, Author
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
        for i in soup.select('article h2 a') if
    not i.get('href').startswith('https://')
    )


def worker(queue: Queue, authors_list):
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
        process(response, url, category_name, authors_list)

        if queue.empty():
            break


@atomic
def process(resp, url, category_name, authors_list):
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

        date = '-'.join(date.split()[0].split('.')[::-1]) + ' ' + date.split()[
            1]
        # breakpoint()
        category, _ = Category.objects.get_or_create(
            name=category_name,
            slug=f"{url.split('/')[-2]}"
        )

        author_dict = random.choice(authors_list)

        write_images(author_dict['foto'], 'media/images/authors')

        author, _ = Author.objects.get_or_create(
            name=author_dict['name'],
            foto=f'images/authors/{author_dict["foto"].split("/")[-1]}'
        )

        article, _ = Article.objects.get_or_create(
            slug=slugify(transliterate.translit(name, reversed=True).
                         lower().replace(' ', '-').
                         replace('є', 'ye').replace('ї', 'yi').replace('і',
                                                                       'i')),
            defaults={
                'base_url': url,
                'title': name,
                'text': text,
                'category': category,
                'date_news': date,
                'description': description,
                'author': author,
                'views': random.randint(0, 100)
            }
        )

        for tag in tags:
            slug = slugify(transliterate.translit(tag, reversed=True).
                           lower().replace(' ', '-').
                           replace('є', 'ye').replace('ї', 'yi').replace('і',
                                                                         'i'))
            t, _ = Tag.objects.get_or_create(
                slug=f"tag-{slug}",
                defaults={'name': tag}
            )
            article.tags.add(t)

        write_images(picture, 'media/images/articles')

        image, _ = Image.objects.get_or_create(
            article=article,
            image=f'images/articles/{picture.split("/")[-1]}',
            base_url=picture
        )


    except Exception as error:
        print(error)


def write_images(picture, path):
    with Session() as session:
        img_response = session.get(picture, timeout=10)
        # breakpoint()
    picture_name = picture.split("/")[-1]
    with open(f'{path}/{picture_name}', 'wb') as file:
        file.write(img_response.content)


def create_authors_list(url):
    print('scraping go on', url)
    try:
        with Session() as s:
            response = s.get(url)
            assert response.status_code == 200, "bad response"
    except Exception as error:
        print('ERROR', error)

    soup = BeautifulSoup(response.text, 'html.parser')

    return [{'name': i.get('alt'), 'foto': i.get('src')
             } for i in soup.select('dl a img')]


def main():
    url = 'https://www.ukrinform.ua'
    authors_list = create_authors_list('https://www.ukrinform.ua/authors')

    category_urls = create_category_urls(url)
    # for dict_ in category_urls[:1]:
    for dict_ in category_urls:

        article_urls = create_article_urls(dict_['url'])

        worker_numb = 10
        # worker_numb = 1

        queue = Queue()

        for url in list(article_urls)[:10]:
            # for url in list(article_urls)[:1]:
            queue.put((url, dict_['category_name']))

        with ThreadPoolExecutor(max_workers=worker_numb) as tpe:
            for _ in range(worker_numb):
                tpe.submit(worker, queue, authors_list)


if __name__ == '__main__':
    main()
