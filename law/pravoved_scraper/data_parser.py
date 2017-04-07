# coding=utf-8
from HTMLParser import HTMLParser
from urllib import urlopen


class DataParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self._url = ''
        self._is_header = False
        self._is_text = False
        self._is_addition = False
        self._count_text = 0
        self._header = ''
        self._question = []
        self._answers = []
        self._additions = []
        self._quote = False

    def handle_starttag(self, tag, attrs):
        if tag == 'h1':
            if ('itemprop', 'name') in attrs:
                self._is_header = True
        if tag == 'div':
            self._is_addition = False
            if ('itemprop', 'text') in attrs:
                self._is_text = True
                self._count_text += 1
        if tag == 'p':
            if ('class', 'questionAdditions') in attrs:
                self._is_addition = True
        if tag == 'blockquote':
            self._quote = True

    def handle_endtag(self, tag):
        if tag == 'h1':
            self._is_header = False
        if tag == 'div':
            self._is_text = False
        if tag == 'blockquote':
            self._quote = False

    def handle_data(self, data):
        data = data.replace('\t', ' ')
        if self._is_header:
            self._header += ' ' + data
        if self._is_text:
            if self._count_text == 1:
                self._question.append(data)
            else:
                if not self._quote:
                    self._answers.append(data)
        if self._is_addition:
            if not self._quote:
                self._additions.append(data)

    def get_data(self, url):
        self._url = url
        page = urlopen(self._url).read().decode('utf-8')
        self.feed(page)
        self._header = self._header.lstrip()
        if self._header.lstrip() == '':
            print '*** WARNING ***'
            print 'missed header: ' + self._url
            open('err_log.txt', 'a').write('missed header: ' + self._url + '\n')
        if not self._question:
            print '*** WARNING ***'
            print 'missed question: ' + self._url
            open('err_log.txt', 'a').write('missed question: ' + self._url + '\n')

        return [self._header, '\n'.join(self._question), '\n'.join(self._answers), '\n'.join(self._additions)]
