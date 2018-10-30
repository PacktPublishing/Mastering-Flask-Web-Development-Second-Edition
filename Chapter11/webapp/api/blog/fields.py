try:
    # Try python3
    from html.parser import HTMLParser
except Exception as e:
    # Nop python2
    from HTMLParser import HTMLParser

from flask_restful import fields


class HTMLStripper(HTMLParser):
    fed = list()

    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = HTMLStripper()
    s.feed(html)

    return s.get_data()


class HTMLField(fields.Raw):
    def format(self, value):
        return strip_tags(str(value))
