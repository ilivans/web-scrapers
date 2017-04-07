#!/usr/bin/python
import re
import urllib2
from time import sleep

from fake_useragent import UserAgent

from html_helpers import remove_tags

_START_PAGE = 102
_LAST_PAGE = 1737  # found manually (using binary search) as website has smart protection


def scrape_generatefacts():
    user_agent = UserAgent()
    facts_all = []
    for page_number in range(_START_PAGE, _LAST_PAGE + 1):
        print "Page #{}".format(page_number)

        url = "http://www.generatefacts.com/fact/{}/index.html".format(page_number)
        request = urllib2.Request(url, headers={'User-Agent': user_agent.random})
        try:
            page = urllib2.urlopen(request)
        except urllib2.HTTPError as e:
            print e
            if e.code == 500:
                continue
            break
        except Exception as e:
            print type(e), e
            break
        html = page.read()

        # Find and process facts on the page
        match = re.search(re.compile('(?<=<div class="fact-text">)(.+?)(?=</div>)', re.DOTALL), html)
        if match is None:
            print "Fact is not found"
            continue
        fact = match.group(0)
        fact = remove_tags(fact)  # remove such tags as <span> or <br>
        fact = " ".join(fact.split())  # remove extra whitespaces

        facts_all.append(fact)
        sleep(1)

    return facts_all


if __name__ == '__main__':
    facts = scrape_generatefacts()
    num_facts = len(facts)
    print "{} facts total".format(num_facts)
    with open("../data/generate{}from{}page.txt".format(num_facts, _START_PAGE), "w") as f:
        f.write("\n".join(facts) + "\n")
