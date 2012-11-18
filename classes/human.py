import uuid

class Human:
    def __init__(self,father=None,mother=None,day=None):
        self.id = uuid.uuid1()
        self.lq = None
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
        self.birthday = 0
        self.stat_int = 50 #intelligence
        self.stat_str = 50 #strength
        self.stat_agi = 50 #agility+health
        self.stat_cha = 50 #charisma
        self.stat_emp = 50 #empathy
        self.stat_cry = 50 #creativity
        self.stat_eth = 50 #work ethic

        self.stat_loy = 50 #loyalty
        self.stat_imm = 50 #genetic immunity

        self.age = 50
    
    def _init_birth_stats(self,father,mother,day):
        self.birthday = 0
        self.stat_int = 50 #intelligence
        self.stat_str = 50 #strength
        self.stat_agi = 50 #agility+health
        self.stat_cha = 50 #charisma
        self.stat_emp = 50 #empathy
        self.stat_cry = 50 #creativity
        self.stat_eth = 50 #work ethic

        self.stat_loy = 50 #loyalty
        self.stat_imm = 50 #genetic immunity

        self.age = 50

    def daily_step(self):
        # % random event
        pass

    def change_lq(self,new_lq):
        self.lq = new_lq
