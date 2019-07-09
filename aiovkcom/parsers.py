import html.parser


class AuthPageParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.inputs = {}
        self.url = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'input':
            attrs = dict(attrs)
            if attrs['type'] != 'submit':
                self.inputs[attrs['name']] = attrs.get('value', '')

        if tag == 'form':
            attrs = dict(attrs)
            if attrs.get('method', '') == 'post':
                self.url = attrs.get('action', '')


class AccessPageParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.inputs = {}
        self.url = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'input':
            attrs = dict(attrs)
            if attrs['type'] != 'submit':
                self.inputs[attrs['name']] = attrs.get('value', '')
        elif tag == 'form':
            attrs = dict(attrs)
            self.url = attrs.get('action')
