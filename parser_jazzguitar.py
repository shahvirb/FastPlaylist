# For https://www.jazzguitar.be/blog
import parser_abstract

class JazzGuitarBeParser(parser_abstract.Parser):
    def __init__(self):
        super().__init__()
    
    @property
    def keys(self):
        return ['name', 'artist']
        
    # Returns parsed data (dict of keys) for all rows
    def parse(self, soup):
        # Get all albumListTitles
        albumListTitles = [s.text.split('.')[-1].split(' – ') for s in soup.select('.inner-post-entry > h2')]
        
        rows = []
        for alt in albumListTitles:
            rows.append({'name':alt[1], 'artist':alt[0]})
        return rows
        
PARSER = JazzGuitarBeParser