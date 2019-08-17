# For https://bestclassicbands.com
import parser_abstract

class BCBandsParser(parser_abstract.Parser):
    def __init__(self):
        super().__init__()
    
    @property
    def keys(self):
        return ['name', 'artist']
        
    # Returns parsed data (dict of keys) for all rows
    def parse(self, soup):
        # Get all albumListTitles
        albumListTitles = [s.text.split(')')[-1].split('by') for s in soup.select('.article-content > p > strong')]
        
        rows = []
        for alt in albumListTitles:
            rows.append({'name':alt[0].replace('“', '').replace('”', '').strip(), 'artist':alt[1].strip()})
        return rows
        
PARSER = BCBandsParser