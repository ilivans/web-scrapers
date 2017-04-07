import re
import cPickle

NUM_PARTS = 10

rubrics_page = open('../../data/svem-questions-rubric.html').read()

rubric_links = re.findall(re.compile('(?<=<li><a href="/)([\w-]+/)'), rubrics_page)
rubric_links = map(lambda tail: 'http://svem.ru/' + tail, rubric_links)

size = len(rubric_links)
part = size / NUM_PARTS + 1

for i in range(NUM_PARTS):
    cPickle.dump(rubric_links[i*part: (i+1)*part if (i+1)*part < size else size],
                 open('../../data/rubric_links{0}.p'.format(i), 'wb'))
