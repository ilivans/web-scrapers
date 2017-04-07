# coding=utf-8
from urllib2 import urlopen
import cPickle
import re
import pandas as pd
import time

import sys

from data_parser import DataParser


def scraper(i):
    rubric_links = cPickle.load(open('../data/rubric_links{0}.p'.format(i), 'rb'))
    start_time = time.time()

    count_rubric = 0
    for init_rubric_link in rubric_links:
        count_rubric += 1
        rubric_data = []
        count_page = 0
        rubric_name = init_rubric_link.split('/')[-2]

        print str(i) + ' started rubric {0}/{1} : {2}'.format(count_rubric, len(rubric_links), rubric_name)

        while True:
            count_page += 1
            rubric_link = init_rubric_link + 'page' + str(count_page) + '/'
            rubric_page = urlopen(rubric_link).read()
            question_links = filter(lambda s: s.startswith(init_rubric_link),
                                    map(lambda tail: 'http://svem.ru' + tail,
                                        re.findall(re.compile('(?<=")(.+?)(?=" target="_blank">)'), rubric_page)))
            if not question_links:
                break
            for question_link in question_links:
                rubric_data.append(DataParser().get_data(question_link))

                # tag, header, question, answers, additions = DataParser().get_data(question_link)
                # print "TAG\n" + tag
                # print "HEADER\n" + header
                # print "QUESTION\n" + question
                # print "ANSWERS\n" + answers
                # print "ADDITIONS\n" + additions

        pd.DataFrame(rubric_data, columns=['tag', 'header', 'question', 'answers', 'additions'])\
            .to_csv('../data/{0}.csv'.format(rubric_name), sep='\t', index=False, encoding='utf-8')

    print str(i) + ' ENDED'

if __name__ == '__main__':
    scraper(sys.argv[1])
