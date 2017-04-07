# coding=utf-8
from urllib2 import urlopen
import cPickle
import re
import pandas as pd
import time

import sys

from data_parser import DataParser


def scraper(i):
    tag_links = cPickle.load(open('../data/tag_names_and_links{0}.p'.format(i), 'rb'))

    count_tag = 0
    for tag_name, init_tag_link in tag_links:
        count_tag += 1
        tag_data = []
        count_page = 0

        # print str(i) + ' time: ' + str(int(time.time() - start_time) / 60) + ' min'
        print str(i) + ' started tag {0}/{1} : {2}'.format(count_tag, len(tag_links), tag_name)

        while True:
            count_page += 1
            tag_link = init_tag_link + str(count_page) if count_page != 1 else init_tag_link
            tag_page = urlopen(tag_link).read()
            question_links = map(lambda tail: 'http://pravoved.ru' + tail,
                                 re.findall(re.compile('(?<=target="_blank" href=")(.+?)(?=")', flags=re.DOTALL),
                                            tag_page))
            if not question_links:
                break
            for question_link in question_links:
                tag_data.append([tag_name] + DataParser().get_data(question_link))

                # header, question, answers, additions = DataParser().get_data(question_link)
                # print "HEADER\n" + header
                # print "QUESTION\n" + question
                # print "ANSWERS\n" + answers
                # print "ADDITIONS\n" + additions

        pd.DataFrame(tag_data, columns=['tag', 'header', 'question', 'answers', 'additions'])\
            .to_csv('../data/{0}-{1}extra.csv'.format(i, count_tag), sep='\t', index=False, encoding='utf-8')

    print str(i) + ' ENDED'

if __name__ == '__main__':
    scraper(sys.argv[1])
