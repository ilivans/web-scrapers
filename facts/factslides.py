#!/usr/bin/python
import re
import urllib2
from time import sleep

from fake_useragent import UserAgent

from html_helpers import remove_tags

_START_PAGE = 1


def scrape_factslides():
    user_agent = UserAgent()
    facts_all = []
    page_number = _START_PAGE
    while True:
        print "Page #{}".format(page_number)

        url = "http://www.factslides.com/p-{}".format(page_number)
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
        match = re.search(re.compile("(?<=itemsHTML  	= new Array\('',')(.+?)(?='\);)"), html)
        if match is None:
            print "END"
            break
        facts = match.group(0)
        facts = remove_tags(facts)  # remove such tags as <span> or <br>
        facts = facts.split("','")
        facts = [" ".join(fact.split()) for fact in facts]  # remove extra whitespaces

        if len(facts) != 10:
            print "Only {} facts found".format(len(facts))

        facts_all.extend(facts)
        page_number += 1
        sleep(2)  # do not hurry

    return facts_all


if __name__ == '__main__':
    facts = scrape_factslides()
    num_facts = len(facts)
    print "{} facts total".format(num_facts)
    with open("../data/factslides{}from{}page.txt".format(num_facts, _START_PAGE), "w") as f:
        f.write("\n".join(facts) + "\n")
