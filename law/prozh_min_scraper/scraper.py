# coding=utf-8
from urllib2 import urlopen
import re
import pandas as pd


def scraper():

    link = 'http://yuridicheskaya-konsultaciya.ru/prozhitochnyj-minimum.html'
    all_data = []
    page = urlopen(link).read()

    table1 = re.findall(re.compile('(?<=border="1" width="100%">)(.+?)(?=</table>)', re.DOTALL), page)[0]
    table2 = re.findall(re.compile('(?<= cellspacing="0">)(.+?)(?=</table>)', re.DOTALL), page)[0]

    for tr in re.findall(re.compile('(?<=<tr>)(.*?)(?=</tr>)', re.DOTALL), table1)[2:]:
        cells = tr.split('\n')[1:-1]
        row = []
        for c in cells:
            row.append(filter(lambda s: s != '', re.findall(re.compile('(?<=>)(.*?)(?=<)'), c))[0])

        # Year, quarter, region
        year = int(filter(lambda ch: ch in '1234567890', row[0]))
        quarter = filter(lambda ch: ch in 'IV', row[0])
        quarter = len(quarter) if 'V' not in quarter else 4
        row = [year, quarter, None] + row[1:]

        # Numbers
        row[3:7] = map(lambda s: int(filter(lambda ch: ch in '1234567890', s)), row[3:7])

        # Source link
        row.insert(7, link)

        # Document link
        row.append(None)
        if 'href' in cells[-1]:
            row[-1] = re.findall(re.compile('(?<=href=")(.+?)(?=")'), cells[-1])[0]

        # Actual or not
        row.append(u'да') if 'color' in cells[3] else row.append(u'нет')

        all_data.append(row)

    region = ''

    for tr in re.findall(re.compile('(?<=<tr>)(.*?)(?=</tr>)', re.DOTALL), table2)[2:-1]:
        cells = re.findall(re.compile('(?<=<td)(.+?)(?=td>)', re.DOTALL), tr)
        if len(cells) < 4:
            continue

        row = []
        for c in cells:
            row.append(filter(lambda s: s != '', re.findall(re.compile('(?<=>)(.+?)(?=</)', re.DOTALL), c))[0])
        row = map(lambda s: ' '.join(s.replace('<br>','').replace('&nbsp;', '').replace('\n', '').split()).split('>')[-1], row)

        if len(row) == 8:
            region, row = row[1], row[2:]

        # Year, quarter, region
        year = int(filter(lambda ch: ch in '1234567890', row[0]))
        quarter = filter(lambda ch: ch in 'IV', row[0])
        quarter = len(quarter) if 'V' not in quarter else 4
        row = [year, quarter, region] + row[1:]

        # Numbers
        row[3:7] = map(lambda s: int(filter(lambda ch: ch in '1234567890', s)), row[3:7])

        # Source link
        row.insert(7, link)

        # Document link
        row.append(None)
        if 'href' in cells[-1]:
            row[-1] = re.findall(re.compile('(?<=href=")(.+?)(?=")'), cells[-1])[0]

        # Actual or not
        row.append(u'да') if 'color' in cells[3] else row.append(u'нет')

        all_data.append(row)

    pd.DataFrame(all_data,
                 columns=[u'год', u'квартал', u'регион', u'на душу населения', u'для трудоспособного населения',
                          u'для пенсионеров', u'для детей', u'источник', u'обоснование', u'ссылка на обоснование',
                          u'актуальный']).to_csv('../data/prozh_min.csv', sep='\t', index=False, encoding='utf-8')


if __name__ == '__main__':
    scraper()