from bs4 import BeautifulSoup
import requests
import click
from unidecode import unidecode
import logging
logging.basicConfig(level=logging.DEBUG)


def fetch_html(url):
    return requests.Session().get(url).content


def make_soup(html):
    return BeautifulSoup(html, 'html.parser')


# Ensure all chars are ASCII
def process(data):
    for d in data:
        for key in d:
            #logging.debug('Processing {}'.format(d[key]))
            d[key] = unidecode(d[key])
    return data


@click.command()
@click.argument('htmlfile')
@click.argument('parserpy')
@click.option('--csvfile', default=None, help='csv output file path')
def main(htmlfile, parserpy, csvfile):
    soup = None
    with open(htmlfile, 'r') as html:
        soup = make_soup(html)
    
    logging.info('Importing {}'.format(parserpy))
    parselib = __import__(parserpy)
    parser = parselib.PARSER()
    data = parser.parse(soup)
    data = process(data)
    logging.debug(data)
    logging.info('Parsed {} rows'.format(len(data)))
    
    if csvfile:
        import csv
        with open(csvfile, 'w', newline='') as file:
            logging.info('Writing to {}'.format(csvfile))
            writer = csv.DictWriter(file, delimiter=',', fieldnames=list(data[0]))
            writer.writeheader()
            writer.writerows(data)
        logging.info('Write complete')


if __name__ == '__main__':
    main()