# coding: utf-8
import pandas as pd

list_of_csv = map(lambda s: s[:-1], open('../../data/list_of_csv.txt').readlines())
all_data = pd.read_csv(list_of_csv[0], delimiter='\t', encoding='utf8', dtype=unicode)
all_data.drop(['answers', 'additions'], axis=1, inplace=True)
for file_name in list_of_csv[1:]:
    another_table = pd.read_csv(file_name, delimiter='\t', encoding='utf8', dtype=unicode)
    another_table.drop(['answers', 'additions'], axis=1, inplace=True)
    all_data = all_data.append(another_table)

all_data.index = range(all_data.shape[0])
all_data.dropna(inplace=True)

all_data.to_csv('../../../tags_classifier/data/pravoved.csv', sep='\t', index=False, encoding='utf-8')


