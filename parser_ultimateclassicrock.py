# For https://ultimateclassicrock.com
import parser_abstract

class UCR(parser_abstract.Parser):
    def __init__(self):
        super().__init__()
    
    @property
    def keys(self):
        return ['name', 'artist']
        
    # Returns parsed data (dict of keys) for all rows
    def parse(self, soup):
        results = soup.select('.list-post > ul > li > header')
        
        rows = []
        for r in results:
            rows.append({'name':r.select_one('h2').text.strip("'"), 'artist':r.select_one('small').text})
        return rows
        
PARSER = UCR