import uuid
from random import randint,choice
from log_types import *

class Human:

    OLD_AGE = 75
    MAX_STAT_VALUE = 100
    MIN_STAT_VALUE = 0
    DEPRESSION_THRESHOLD = 30
    HIGH_STANDARD_HAPPINESS = 80
    HEALTHY_HP = 50

    def __init__(self,ship=None,father=None,mother=None,day=None):
        self.id = uuid.uuid1()
        self.lq = None
        self.job = None
        self.ship = ship
        self.hp = 100
        self.alive = True
        self.days_on_ship = 0
        self.days_at_job = 0
        self.days_at_home = 0
        self.criminal_day_sentence = 0

        self.old_age_immobile = False
        self.old_age_hospitalized = False
		
	self.should_be_prisoner = False
		
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
            "int":randint(10,100), #intelligence
            "str":randint(10,100), #strength
            "agi":randint(10,100), #agility
            "cha":randint(10,100), #charisma
            "emp":randint(10,100), #empathy
            "cry":randint(10,100), #creativity
            "eth":randint(10,100), #work ethic

            "hap":randint(80,100), #happiness

            "loy":randint(10,100), #loyalty
            "imm":randint(10,100), #immune system
        }
        if randint(0,100) == 0:
            self.should_be_prisoner = True

    
        self.sex = choice(['m','f'])

        self.first_name = self.ship.name_reader.get_random_name(self.sex)
        self.last_name = self.ship.name_reader.get_random_name('l')
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

            "hap":50,

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

    def daily_step(self,day):
            
        if self.alive:

            # if you should be in a hospital, but arent - take major health hit
            if self.should_be_hospitalized():
                if not self.lq or self.lq.type != "hospital":
                    self.hp -= randint(1,3)

            # reduce happiness if homeless (TODO- % to change loyalty)
            if self.lq is None:
                # more empathetic people become depressed easier
                empathy_factor = self.stats['emp']/10
                self.dec_stat("hap",randint(0,empathy_factor))

            # reduce happiness if jobless (TODO- % to change loyalty)
            if self.job is None:
                # more empathetic people become depressed easier
                empathy_factor = self.stats['emp']/10
                self.dec_stat("hap",randint(0,empathy_factor))

            # celebrate birthday. increase happiness if you are social!
            if day == self.birthday:
                self.age += 1
                self.ship._add_log(LOG_TYPE_HUMANS,LOG_LEVEL_LOW,str(self.first_name)+" "+str(self.last_name)+" turned "+str(self.age)+" years old.")
                self.inc_stat("hap",randint(0,((self.stats['cha'])/5)))

            # if everything is good in life, increase happiness based on empathy
            if self.job and self.lq and self.hp >= Human.HEALTHY_HP:
                empathy_factor = self.stats['emp']/5
                if randint(0,empathy_factor) == 0:
                    self.inc_stat("hap",1)

            if self.stats["hap"] >= Human.HIGH_STANDARD_HAPPINESS:
                self.inc_stat("loy",1)

            # if you are depressed, it can lower your stats!
            if self.stats["hap"] <= Human.DEPRESSION_THRESHOLD:
                if randint(0,self.stats["hap"]*3) == 0:
                    #self.ship._add_log(3,str(self.first_name)+" "+str(self.last_name)+" is severely depressed.")
                    self.dec_stat(choice(['agi','cha','cry','emp','eth','loy']),1)

            # if you are elderly
            if self.age > Human.OLD_AGE:

                # chance to decline in stats based on agility
                health_factor = self.stats['agi']/2
                if randint(0,health_factor) == 0:
                    dec_factor = self.age/10
                    self.dec_stat(choice(['int','str','agi','eth','imm']),randint(0,dec_factor))

                # chance to lose hp in declining health
                if randint(0,100) >= (((self.stats['agi']+self.stats['imm'])/2)+10):
                    self.hp -= randint(1,5)

                    if not self.old_age_immobile:
                        # chance to become bedridden and unable to work
                        if randint(0,self.stats['agi']) == 0:
                            self.set_old_age_immobile()
                    else:
                        if not self.old_age_hospitalized:
                            if randint(0,100) >= self.stats['imm'] and self.hp < Human.HEALTHY_HP:
                                self.ship._add_log(LOG_TYPE_HUMANS,LOG_LEVEL_MED,str(self.first_name)+" "+str(self.last_name)+" requires hospitalization due to old age.")
                                self.old_age_hospitalized = True

            # no longer alive
            if self.hp <= 0:
                self.ship._add_log(LOG_TYPE_HUMANS,LOG_LEVEL_HIGH,str(self.first_name)+" "+str(self.last_name)+" ("+str(self.age)+") has passed away.")
                self.alive = False

        self.days_on_ship +=1
        self.days_at_job +=1
        self.days_at_home +=1

        return self.alive

    def should_be_hospitalized(self):
        # TODO handle disease/injury hospitalization
        return self.old_age_hospitalized
		
    def should_be_imprisoned(self):
        # TODO criminal system
        return self.should_be_prisoner
	
    def inc_stat(self,stat,amount):
        if self.stats[stat] < Human.MAX_STAT_VALUE:
            self.stats[stat]+=amount
        if self.stats[stat] > Human.MAX_STAT_VALUE:
            self.stats[stat] = Human.MAX_STAT_VALUE

    def dec_stat(self,stat,amount):
        if self.stats[stat] > Human.MIN_STAT_VALUE:
            self.stats[stat]-=amount
        if self.stats[stat] < Human.MIN_STAT_VALUE:
            self.stats[stat] = Human.MIN_STAT_VALUE

    def set_old_age_immobile(self):
        if self.old_age_immobile == False:
            self.old_age_immobile = True
            if self.job:
                self.job['room'].fire_human(self,self.job['job'])
            self.ship._add_log(LOG_TYPE_ROOMS,LOG_LEVEL_MED,str(self.first_name)+" "+str(self.last_name)+" ("+str(self.age)+") is bedridden and can no longer work.")

    def change_lq(self,new_lq):
        self.days_at_home = 0
        self.lq = new_lq

    def change_job(self,new_job):
        self.days_at_job = 0
        self.job = new_job

    def print_stats(self):
        print str(self.first_name)+" "+str(self.last_name)+": "+str(self.stats)

    def meets_requirements(self,requirements):
        for k,v in requirements.items():
            if self.stats[k] < v:
                return False
        return True

    #TODO - suffering affects old and young more

    def suffer_thirst(self):
        self.hp -= randint(10,30)

    def suffer_hunger(self):
        self.ship._add_log(LOG_TYPE_HUMANS,LOG_LEVEL_MED,str(self.first_name)+" "+str(self.last_name)+" hunger")
        self.hp -= randint(0,5)

    def suffer_protein_loss(self):
        if randint(0,25) == 0:
            self.dec_stat('agi',1)

    def suffer_vitamin_loss(self):
        if randint(0,30) == 0:
            self.dec_stat('imm',1)

    def eat_balanced_diet(self):
        pass

    def suffocate(self):
        self.hp -= randint(0,100)
