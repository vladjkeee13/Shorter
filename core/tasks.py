from django.utils import timezone

from ManagingURLs.celery import app
from core.models import Url

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup


@app.task
def delete_old_urls():

    urls = Url.objects.all()
    for url in urls:
        if url.expiration_date < timezone.now():
            url.delete()

    return "completed deleting urls at {}".format(timezone.now())


@app.task
def parse_original_url(url_id):

    url = Url.objects.get(id=url_id)
    req = Request(url.url, headers={'User-Agent': 'Mozilla/5.0'})

    try:
        web_byte = urlopen(req).read()
        soup = BeautifulSoup(web_byte, 'html.parser')
        text = soup.find_all(['span', 'p', 'h1', 'h2', 'h3', 'h4'])

        if text:
            text_2 = ''
            for elem in text:
                if len(elem.get_text()) > 0:
                    text_2 = elem.get_text()
                    break
            url.text = text_2
            url.save()
        return 'text was added successfully'

    except:
        return "no text for url({})".format(url.id)
