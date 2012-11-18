import uuid
from random import randint

class Human:
    def __init__(self,father=None,mother=None,day=None):
        self.id = uuid.uuid1()
        self.lq = None
        self.job = None
        self.hp = 100
        self.criminal_day_sentence = 0

        self.is_pregnant = False
        self.day_pregnant = 0

        self.status_effects = [] #injuries+diseases

        if father and mother and day:
            self._init_birth_stats(father,mother)
        else:
            self._roll_stats()
        #print "Human created with id: "+str(self.id)

    def _roll_stats(self):
        self.birthday = randint(1,365)
        self.stats = {
            "int":randint(0,100),
            "str":randint(0,100),
            "agi":randint(0,100),
            "cha":randint(0,100),
            "emp":randint(0,100),
            "cry":randint(0,100),
            "eth":randint(0,100),

            "loy":randint(0,100),
            "imm":randint(0,100),
        }

        self.first_name = "John"
        self.last_name = "Smith"
        self.age = randint(0,80)
    
    def _init_birth_stats(self,father,mother,day):
        self.birthday = 0
        self.stats = {
            "int":50,
            "str":50,
            "agi":50,
            "cha":50,
            "emp":50,
            "cry":50,
            "eth":50,

            "loy":50,
            "imm":50
        }
        #intelligence
        #strength
        #agility+health
        #charisma
        #empathy
        #creativity
        #work ethic

        self.stat_loy = 50 #loyalty
        self.stat_imm = 50 #genetic immunity

        self.age = 50

    def daily_step(self):
        # % random event
        pass

    def change_lq(self,new_lq):
        self.lq = new_lq

    def print_stats(self):
        print str(self.first_name)+" "+str(self.last_name)+": "+str(self.stats)

    def meets_requirements(self,requirements):
        for k,v in requirements.items():
            if self.stats[k] < v:
                print str(self.id)+" "+str(k)+" has "+str(self.stats[k])+" needs "+str(v)
                return False
        return True
