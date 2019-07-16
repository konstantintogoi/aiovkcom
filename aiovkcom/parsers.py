from collections import defaultdict
import html.parser


class AuthPageParser(html.parser.HTMLParser):
    """Authorization page parser."""

    @property
    def form(self):
        return self.url, self.inputs

    def __init__(self):
        super().__init__()
        self.inputs = {}
        self.url = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'input':
            attrs = defaultdict(str, attrs)
            if attrs['type'] != 'submit':
                self.inputs[attrs['name']] = attrs['value']

        if tag == 'form':
            attrs = defaultdict(str, attrs)
            if attrs['method'] == 'post':
                self.url = attrs['action']


class AccessPageParser(html.parser.HTMLParser):
    """Access page parser."""

    @property
    def form(self):
        return self.url, self.inputs

    def __init__(self):
        super().__init__()
        self.inputs = {}
        self.url = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'input':
            attrs = defaultdict(str, attrs)
            if attrs['type'] != 'submit':
                self.inputs[attrs['name']] = attrs['value']

        elif tag == 'form':
            attrs = defaultdict(str, attrs)
            if attrs['method'] == 'post':
                self.url = attrs['action']
