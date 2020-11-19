from html.parser import HTMLParser

class TSDMResultParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.result = None
        self.found = False

    def handle_starttag(self, tag: str, attrs: list) -> None:
        if tag == 'div' and ('id', 'messagetext') in attrs:
            self.found = True

    def handle_data(self, data: str) -> None:
        if self.found and self.lasttag == 'p':
            self.result, self.found = data, False
    
    def feed(self, feed: str) -> str:
        HTMLParser.feed(self, feed)
        return self.result