# For http://www.progarchives.com
import parser_abstract

class ProgArchivesParser(parser_abstract.Parser):
    def __init__(self):
        super().__init__()
    
    @property
    def keys(self):
        return ['name', 'artist']
        
    # Returns parsed data (dict of keys) for all rows
    def parse(self, soup):
        # Get all albums
        albums = [s.text for s in soup.select('td > a > strong')]
        
        # Get all artists
        artists = [s.text for s in soup.select('td > a[href^="artist"]')]
        
        rows = []
        assert len(albums) == len(artists)
        for i in range(len(albums)):
            rows.append({'name':albums[i], 'artist':artists[i]})
        return rows
        
PARSER = ProgArchivesParser
