import random

class NameReader:
    def __init__(self):

        self.files = {
            "m": {
                "file":(open('data/male_first_names.txt','r')),
                "names":None
            },
            "f": {
                "file":(open('data/female_first_names.txt','r')),
                "names":None
            },
            "l": {
                "file":(open('data/last_names.txt','r')),
                "names":None
            },
            "lq": {
                "file":(open('data/lq_names.txt','r')),
                "names":None
            },
            "adjective": {
                "file":(open('data/adjectives.txt','r')),
                "names":None
            },
            "noun": {
                "file":(open('data/nouns.txt','r')),
                "names":None
            },
            "title": {
                "file":(open('data/titles.txt','r')),
                "names":None
            },
        }

        for k,v in self.files.items():
            self.files[k]['names'] = v['file'].read().splitlines()

    def get_random_name(self,name_type):
        return random.choice(self.files[name_type]['names'])
