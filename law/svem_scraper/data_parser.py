# coding=utf-8
from HTMLParser import HTMLParser
from urllib import urlopen


class DataParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self._url = ''
        self._is_tag = False
        self._is_header = False
        self._is_question = False
        self._is_answer = False
        self._is_addition = False
        self._tag = ''
        self._header = ''
        self._question = []
        self._answers = []
        self._additions = []

    def handle_starttag(self, tag, attrs):
        if tag == 'h1':
            self._is_header = True
        if tag == 'div':
            if ('class', 'large') in attrs:
                self._is_question = True
                for key, value in attrs:
                    if key == 'id':
                        self._is_question = False
                        if value.startswith('answer'):
                            self._is_answer = True
                        elif value.startswith('clarify'):
                            self._is_addition = True
                        else:
                            print '*** WARNING ***'
                            print 'unknown div id: ' + self._url
                            open('err_log.txt', 'a').write('unknown div id: ' + self._url + '\n')
        if tag == 'a':
            if ('href', '/'.join(self._url.split('/')[:-2]) + '/') in attrs:
                self._is_tag = True

    def handle_endtag(self, tag):
        if tag == 'h1':
            self._is_header = False
        if tag == 'div':
            self._is_question = self._is_answer = self._is_addition = False
        if tag == 'a':
            self._is_tag = False

    def handle_data(self, data):
        data = data.replace('\t', ' ')
        if self._is_tag:
            self._tag = data
        if self._is_header:
            self._header += ' ' + data
        if self._is_question:
            self._question.append(data)
        if self._is_answer:
            self._answers.append(data)
        if self._is_addition:
            self._additions.append(data)

    def get_data(self, url):
        self._url = url
        page = urlopen(self._url).read().decode('utf-8')
        self.feed(page)
        self._header = self._header.lstrip()
        if self._header == '':
            print '*** WARNING ***'
            print 'missed header: ' + self._url
            open('err_log.txt', 'a').write('missed header: ' + self._url + '\n')
        if not self._question:
            print '*** WARNING ***'
            print 'missed question: ' + self._url
            open('err_log.txt', 'a').write('missed question: ' + self._url + '\n')

        return [self._tag, self._header,
                '\n'.join(self._question), '\n'.join(self._answers), '\n'.join(self._additions)]
