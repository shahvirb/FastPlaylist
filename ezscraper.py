from bs4 import BeautifulSoup
import requests
import click
import coloredlogs
from unidecode import unidecode
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def fetch_html(url):
    return requests.Session().get(url).content


def make_soup(html):
    return BeautifulSoup(html, 'html.parser')


# Ensure all chars are ASCII
def process(data):
    for d in data:
        for key in d:
            #logger.debug('Processing {}'.format(d[key]))
            d[key] = unidecode(d[key])
    return data


def parse_soup(parserpy, soup):
    logger.info('Importing {}'.format(parserpy))
    parselib = __import__(parserpy)
    parser = parselib.PARSER()
    data = parser.parse(soup)
    data = process(data)
    for line in data:
        logger.info(line)
    logger.info('Parsed {} rows'.format(len(data)))
    return data


@click.command()
@click.argument('parserpy')
@click.option('--htmlfile', default=None, help='HTML file path')
@click.option('--url', default=None, help='URL to fetch HTML')
@click.option('--csvfile', default=None, help='csv output file path')
def main(parserpy, htmlfile, url, csvfile):
    coloredlogs.install()
    #logger.addHandler(logging.StreamHandler())

    if url:
        data = parse_url(parserpy, url)
    if htmlfile:
        data = parse_html_file(htmlfile)

    if csvfile:
        import csv
        with open(csvfile, 'w', newline='') as file:
            logger.info('Writing to {}'.format(csvfile))
            writer = csv.DictWriter(file, delimiter=',', fieldnames=list(data[0]))
            writer.writeheader()
            writer.writerows(data)
        logger.info('Write complete')


def parse_html_file(parserpy, htmlfile):
    logger.info(f'Opening {htmlfile}')
    with open(htmlfile, 'r', encoding='utf8') as html:
        soup = make_soup(html)
    data = parse_soup(parserpy, soup)
    return data


def parse_url(parserpy, url):
    logger.info(f'Fetching {url}')
    html = fetch_html(url)
    soup = make_soup(html)
    data = parse_soup(parserpy, soup)
    return data


if __name__ == '__main__':
    main()