import parser_abstract

class RSParser(parser_abstract.Parser):
    def __init__(self):
        super().__init__()
    
    @property
    def keys(self):
        return ['name', 'artist']
        
    # Returns parsed data (dict of keys) for all rows
    def parse(self, soup):
        results = [s.text.strip() for s in soup.select('.c-list__item > header > h3')]
        
        rows = []
        for r in results:
            rows.append({'name':r.split(',')[1].strip(' ‘').split('’')[0], 'artist':r.split(',')[0]})
        return rows
        
PARSER = RSParser