# For https://djmag.com/longreads/dj-mag%E2%80%99s-definitive-electronic-albums-decade
import parser_abstract


class DJMag(parser_abstract.Parser):
    def __init__(self):
        super().__init__()

    @property
    def keys(self):
        return ['name', 'artist']

    # Returns parsed data (dict of keys) for all rows
    def parse(self, soup):
        artists = [div.contents[0].text for div in soup.select('.field--name-field-list-number')]
        names = [div.contents[0].text.strip("'") for div in soup.select('.field--name-field-list-title')]
        rows = []
        for artist, name in zip(artists, names):
            rows.append({'artist': artist, 'name': name})
        return rows


PARSER = DJMag
