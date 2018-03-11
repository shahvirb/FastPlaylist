# For http://www.albumoftheyear.org
import parser_abstract

class AOTYParser(parser_abstract.Parser):
    def __init__(self):
        super().__init__()
    
    @property
    def keys(self):
        return ['name', 'artist']
        
    # Returns parsed data (dict of keys) for all rows
    def parse(self, soup):
        # Get all albumListTitles
        albumListTitles = [s.text.split(' - ') for s in soup.select('h2.albumListTitle > span > a')]
        
        rows = []
        for alt in albumListTitles:
            rows.append({'name':alt[1], 'artist':alt[0]})
        return rows
        
PARSER = AOTYParser