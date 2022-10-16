from bs4 import BeautifulSoup
from requests import Session


def create_authors_list(url):

    print('scraping go on', url)
    try:
        with Session() as s:
            response = s.get(url)
            assert response.status_code == 200, "bad response"
    except Exception as error:
        print('ERROR', error)


    soup = BeautifulSoup(response.text, 'html.parser')
    breakpoint()
    return ...


if __name__ == '__main__':
    create_authors_list('https://www.ukrinform.ua/authors')

