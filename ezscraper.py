from bs4 import BeautifulSoup
import requests
import click
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


@click.command()
@click.argument('htmlfile')
@click.argument('parserpy')
@click.option('--csvfile', default=None, help='csv output file path')
def main(htmlfile, parserpy, csvfile):
    logger.addHandler(logging.StreamHandler())
    soup = None
    with open(htmlfile, 'r', encoding='utf8') as html:
        soup = make_soup(html)
    
    logger.info('Importing {}'.format(parserpy))
    parselib = __import__(parserpy)
    parser = parselib.PARSER()
    data = parser.parse(soup)
    data = process(data)
    logger.debug(data)
    logger.info('Parsed {} rows'.format(len(data)))
    
    if csvfile:
        import csv
        with open(csvfile, 'w', newline='') as file:
            logger.info('Writing to {}'.format(csvfile))
            writer = csv.DictWriter(file, delimiter=',', fieldnames=list(data[0]))
            writer.writeheader()
            writer.writerows(data)
        logger.info('Write complete')


if __name__ == '__main__':
    main()