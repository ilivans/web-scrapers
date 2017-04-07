import re
import cPickle

NUM_PARTS = 6

themes_page = open('../../data/pravoved-themes-page.html').read()

tag_links = re.findall(re.compile('/themes/%[^/]*/'), themes_page)
tag_links = map(lambda tail: 'http://pravoved.ru' + tail, tag_links)

tag_names = re.findall(re.compile('(?<=/themes/%)(.+?)(?=</a>)'), themes_page)
tag_names = map(lambda t: t.split('>')[1], tag_names)

assert len(tag_names) == len(tag_links)
tag_zip = zip(tag_names, tag_links)
size = len(tag_zip)
part = size / NUM_PARTS + 1

for i in range(NUM_PARTS):
    cPickle.dump(tag_zip[i*part: (i+1)*part if (i+1)*part < size else size],
                 open('../../data/tag_names_and_links{0}.p'.format(i), 'wb'))
