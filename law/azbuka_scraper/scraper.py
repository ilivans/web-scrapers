# coding=utf-8
from urllib2 import urlopen
import cPickle
import re
import pandas as pd
import numpy as np
import time

import sys

from data_parser import DataParser


def add_prefix(link):
    return 'http://azbuka.consultant.ru' + link


def scraper():
    root_rubric_links = map(add_prefix,
                       ["/auto/", "/armiya/", "/vyezd/", "/grazhdanstvo/", "/zhilye/", "/prava-potrebiteley/",
                        "/kredity/", "/medicina/", "/nalogi/", "/nasledstvo/", "/obrazovanie/", "/pensii/", "/semya/",
                        "/strahovanie/", "/trud/"])
    all_data = []
    count_root_rubric = 0
    for root_rubric_link in root_rubric_links:
        count_root_rubric += 1
        print 'started rubric {0}/{1}'.format(count_root_rubric, len(root_rubric_links))

        rubric_page = urlopen(root_rubric_link).read()
        rubrics = map(lambda s: list(reversed(add_prefix(s.replace('"', '')).split('>'))) + [None] * 2,
                      re.findall(re.compile('(?<=class="rubric"><a href=")(.+?)(?=</a></div>)'), rubric_page))
        all_data += rubrics
        article_links = map(add_prefix,
                            re.findall(re.compile('(?<=class="document"><a href=")(.+?)(?=")'), rubric_page))

        count_article = 0
        for article_link in article_links:
            count_article += 1
            if count_article % 10 == 0:
                print 'article {0}/{1}'.format(count_article, len(article_links))

            all_data.append(DataParser().get_data(article_link))

            # name, url, preview, path = DataParser().get_data(article_link)
            # print "NAME\n" + name
            # print "URL\n" + url
            # print "PREVIEW\n" + preview
            # print "PATH\n" + path

    pd.DataFrame(all_data, columns=['name', 'url', 'preview', 'path']) \
        .to_csv('../data/azbuka_raw.csv', sep='\t', index=False, encoding='utf-8')

    print 'ENDED'


if __name__ == '__main__':
    scraper()
