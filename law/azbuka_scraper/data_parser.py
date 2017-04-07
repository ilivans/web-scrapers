# coding=utf-8
from HTMLParser import HTMLParser
from urllib import urlopen


class DataParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self._url = ''
        self._is_path = False
        self._is_a = False
        self._is_preview = False
        self._is_trash = False
        self._path = []
        self._name = []
        self._preview = []

    def handle_starttag(self, tag, attrs):
        if tag == 'ul':
            if ('class', 'breadcrumb') in attrs:
                self._is_path = True
        if tag == 'div':
            if ('id', 'doc_text') in attrs:
                self._is_preview = True
        if tag == 'h2':
            self._is_trash = True
        if tag == 'p':
            if ('style', 'text-align:right;') in attrs:
                self._is_trash = True
        if tag == 'a':
            self._is_a = True
        if tag == 'img':
            self._is_preview = False

    def handle_endtag(self, tag):
        if tag == 'ul':
            self._is_path = False
        if tag == 'a':
            self._is_a = False
        if tag == 'h2':
            self._is_trash = False
        if tag == 'p':
            self._is_trash = False

    def handle_data(self, data):
        data = data.replace('\t', ' ')
        if self._is_path:
            if self._is_a:
                self._path.append(data)
            else:
                self._name.append(data)
        if self._is_preview and not self._is_trash:
            self._preview.append(data)

    def get_data(self, url):
        self._url = url
        page = urlopen(self._url).read().decode('utf-8')
        self.feed(page)

        if not self._name:
            print '*** WARNING ***'
            print 'missed name: ' + self._url
            open('err_log.txt', 'a').write('missed name: ' + self._url + '\n')
        if not self._preview:
            print '*** WARNING ***'
            print 'missed preview: ' + self._url
            open('err_log.txt', 'a').write('missed preview: ' + self._url + '\n')
        if not self._path:
            print '*** WARNING ***'
            print 'missed path: ' + self._url
            open('err_log.txt', 'a').write('missed path: ' + self._url + '\n')
        preview = ' '.join(self._preview).strip()
        if len(preview) < 300:
            print '*** WARNING ***'
            print 'short preview: ' + self._url
            open('err_log.txt', 'a').write('short preview: ' + self._url + '\n')
        else:
            preview = preview[:300]
            preview = preview[:preview.rfind(' ')]

        return [''.join(self._name).strip(), self._url, preview, ' > '.join(self._path[1:]).strip()]
