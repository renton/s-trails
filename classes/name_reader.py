import random

class NameReader:
    def __init__(self):

        self.files = {
            "m": {
                "file":(open('data/male_first_names.txt','r+b')),
                "names":None
            },
            "f": {
                "file":(open('data/female_first_names.txt','r+b')),
                "names":None
            },
            "l": {
                "file":(open('data/last_names.txt','r+b')),
                "names":None
            },
            "lq": {
                "file":(open('data/lq_names.txt','r+b')),
                "names":None
            },
            "adjective": {
                "file":(open('data/adjectives.txt','r+b')),
                "names":None
            },
            "noun": {
                "file":(open('data/nouns.txt','r+b')),
                "names":None
            },
            "title": {
                "file":(open('data/titles.txt','r+b')),
                "names":None
            },
            "animal": {
                "file":(open('data/animals.txt','r+b')),
                "names":None
            },
            "object": {
                "file":(open('data/objects.txt','r+b')),
                "names":None
            },
            "verb": {
                "file":(open('data/verbs.txt','r+b')),
                "names":None
            }
        }

        for k,v in self.files.items():
            self.files[k]['names'] = v['file'].read().splitlines()

    def get_random_name(self,name_type):
        return random.choice(self.files[name_type]['names'])

    def clean_files(self):
        for k,v in self.files.items():
           fileList= set(v['names'])
           fileList = list(fileList)
           fileList.sort()
           outFile = v['file']
           outFile.seek(0,0)
           for item in fileList:
               outFile.write(item + '\r\n')
           outFile.close()
