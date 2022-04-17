import json
import pandas as pd

test = pd.read_json('test.json', orient='index')

with open('train.json', 'r') as f:
    train = json.load(f)

def split_authors_foreach_record(file):
    train_dataset = {}
    train_copy = file.copy()
    count = 0
    while count < len(file):
        for key, value in train_copy.items():
            venue = value['venue']
            keywords = value['keywords']
            year = value['year']
            authors = value['author'].copy()
            if len(value['author']) > 1:
                for author in value['author']:
                    authors.remove(author)
                    new_record = {str(count): {'venue': venue, 'keywords': keywords, 'year': year, 'coauthor': authors,
                                               'target': author}}
                    train_dataset.update(new_record)
                    authors = value['author'].copy()
                    count += 1
            else:
                new_record = {str(count): {'venue': venue, 'keywords': keywords, 'year': year, 'coauthor': authors,
                                           'target': authors.pop()}}
                train_dataset.update(new_record)
                count += 1
    return train_dataset

train = split_authors_foreach_record(train)

print(len(train))
