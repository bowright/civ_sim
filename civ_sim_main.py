# -*- coding: utf-8 -*-
"""
Created on Wed Oct 29 21:23:44 2014

@author: ZN

Objective: Simulate civilization evolvement in the universe

Axiom 1. Survival is the primal demand of a civilization
Axiom 2. The total matter of the universe is constant

Rule 1. Civ occur spontaneously at random interval
Rule 2. Civ die spontaneously when reach random logevity
Rule 3. Civ evolve in different pace, exponential or linear
Rule 4. Civ grow aggressive proportional to its resouce
Rule 5. Civ starts war proportional to its aggressiveness
Rule 6. Probability civ win wars proportional to its resouce differential
Rule 7. Civ invade nearest neighbor first
Rule 8. Civ advance to next technology level randomly, proportional to its resources
Rule 9. War starts inversly porportional to the free matter of the universe
Rule 10. Civ growth rate is lowered by free matter
Rule 11. Civ gets all resouces of others if wins the war
Rule 12. Civ advance to next level randomly
Rule 13. Resource holding determine very little tech advancement
Rule 14. Civ only invades other civs less than or equal to its level

"""

import sys
import pdb
import time
import numpy as np
import random
import matplotlib.pyplot as plt

# Settings

war_on = 1
civ_grow_rate = 0.01
civ_grow_model = 2  # growth model see def grow

        
class Civ(object):
    """ generic civilization class"""
    
    # Universe parameters
    uni_r = 50      # Radius of the universe
    uni_yr = 1000   # universe evolution years
    uni_age = 0     # Current age of universe
    uni_matter = 10**8     # free resources of the universe
    
    # Total civilizations parameters
    civs_live = {}  # set of live civs
    civs_serial = 0 # serial of civ
    civs_born = 0   # number of civ born
    civs_died = 0   # number of civ died
    civs_wars = 0
    
    def __init__(self):
        self.pos = [np.random.rand() * x for x in [Civ.uni_r, 2*np.pi, 2*np.pi]]
        self.rsc = np.random.random_integers(1, 1000)  # initial resource
        self.rsc_grow_rate = random.randint(1, 10) * civ_grow_rate
        self.p_agg = 0.0   # aggressiveness probability
        self.aggres = random.randint(1, 1000)
        self.logevity = 0.0
        self.age = 0
        self.dob = 0    # date of birth
        self.tech = 0   # level of technology
        
        self.serial = Civ.civs_serial   # serial of civ object
        Civ.civs_serial += 1            # increment serial after assign to object
        Civ.civs_born += 1
        Civ.uni_matter -= self.rsc
        self.name = "civ #" + str(Civ.civs_serial)
        
    def grow(self):
        # grow by using free matter in the universe
        # growth coefficient is randomly diminishing with resource
        if civ_grow_model == 1:
            # model 1, single civ can use all matters
            g_coeff = random.random() * (Civ.uni_matter/(self.rsc+Civ.uni_matter))
        if civ_grow_model == 2:
            # model 2, single civ can use upto 1/100 universe matter
            g_coeff = random.random() * (1 - self.rsc*100/Civ.uni_matter)
        rsc_used = self.rsc * self.rsc_grow_rate * g_coeff
        self.rsc += rsc_used
        Civ.uni_matter -= rsc_used
        
        # civ probability of aggression grows
        self.p_agg = self.rsc / Civ.uni_matter * self.aggres
        
    def die(self, civ):
        # killed by civ, other or self, matter becomes free
        Civ.civs_died += 1
        
        if self.name!=civ.name:
            print(self.name + " killed by " + civ.name)
            civ.rsc += self.rsc
        else:
            Civ.uni_matter += self.rsc
        
        # remove from live civs
        # Civ.civs_live.pop(Civ.civs_live.keys()[Civ.civs_live.values().index(self)])
        Civ.civs_live.pop(self.serial)
        del self
    

def random_born():
    # civs randomly born with free matter
    n_born = random.randint(0, round(Civ.uni_matter/10**7))
    for k in range(Civ.civs_serial, Civ.civs_serial+n_born-1):
        Civ.civs_live[k] = Civ()
        Civ.civs_live[k].dob = Civ.uni_age
        Civ.civs_live[k].logevity = 100 * Civ.uni_yr * np.random.rand()
        print(Civ.civs_live[k].name + " is born in year " + str(Civ.uni_age) + ".")
        
def uni_grow():
    # university grows
    if len(Civ.civs_live)>0:
        key_dead = []
        ls_civs_live = list(Civ.civs_live.keys())
        for i in ls_civs_live:
            # skip if civ killed
            # print('key_dead:', key_dead)
            if i in key_dead:
                continue
            
            civ = Civ.civs_live[i]
            civ.age += 1
            civ.grow()
            
#            if civ.age > civ.logevity:
#                # civ dies when reach its logevity
#                print(civ.name + " died in year " + `Civ.uni_age` + ". Age " + `civ.age` + ". Rsc " + format(civ.rsc, ".2e"))
#                civ.die(civ)
                
            # if civ has more rsc more likely to invade
            if war_on==1:
                if civ.p_agg > random.random():
                    key_loser = war(invader=civ)
                    key_dead.append(key_loser)
                
    Civ.uni_age += 1


def war(invader):
    # invader choose civs with less but comparable civs to invade
    key_def = random.choice(list(Civ.civs_live.keys()))
    defender = Civ.civs_live[key_def]
    all_keys = Civ.civs_live.keys()
    
    while ((defender.rsc > invader.rsc*100) & (defender.rsc < invader.rsc/100) & (len(all_keys)>1) & (defender.name!=invader.name)):
        key_def = random.choice(all_keys)
        all_keys.remove(key_def)
        defender = Civ.civs_live[key_def]
        
    if (len(all_keys)<1) | (invader.name == defender.name):
        return None
    
    # war happens
    Civ.civs_wars += 1
    
    # outcome of the war is random but proportional to parties' resource
    print(invader.name + " invades " + defender.name)
    if random.random() > invader.rsc/(invader.rsc+defender.rsc):
        # print('invader:\n', invader)
        # print('invader serial:', str(invader.serial))
        # key_inv = Civ.civs_live.keys()[Civ.civs_live.values().index(invader)]
        key_inv = invader.serial
        invader.die(defender)
        return key_inv
    else:
        defender.die(invader)
        return key_def  # return the key of dead
        
        
def main():
    """ main module for time evolution """
    
    civ_hist = {}
    rsc_hist = {}
    # time lapse
    for t in range(Civ.uni_yr):  
        print("\nUniverse year: " + str(t))
        
        # civ born on random interval
        random_born()
        
        # universe grow with time
        uni_grow()
        
        # append number of living civs
        civ_hist[t] = len(Civ.civs_live)
        rsc_hist[t] = sum(Civ.civs_live[i].rsc for i in Civ.civs_live.keys()) / (sum(Civ.civs_live[i].rsc for i in Civ.civs_live.keys()) + Civ.uni_matter)

        # time.sleep(0.1)
        
    print("\n\nThis Universe Simulation Ends.\n")
    print(str(len(Civ.civs_live)) + " civ survived in the universe. " + str(Civ.civs_born) + " born. " + str(Civ.civs_died) + " perished.")
    print("Free matter in the universe: " + format(Civ.uni_matter, ",.0f"))
    print("Matters utlitzed by civs: " + format(sum(Civ.civs_live[i].rsc for i in Civ.civs_live.keys()), ",.0f"))
    print("Wars happened: " + format(Civ.civs_wars, ",.0f"))
    
    # plot civ survived distribution
    n_bins = 10
    plt.figure()
    plt.hist([Civ.civs_live[x].rsc for x in Civ.civs_live.keys()], n_bins)
    plt.xlabel("Resource under control")
    plt.ylabel("Number of civs")
    plt.title("Resource distribution")
    
    # plot civ number history
    plt.figure()
    # plt.fill_between(civ_hist.keys(), 0, civ_hist.values(), facecolor="r")
    plt.plot(civ_hist.keys(), civ_hist.values())
    plt.title("Historical number of civilizations")
    
    # plot resources used by civilizations    
    plt.figure()
    # plt.fill_between(rsc_hist.keys(), 0, rsc_hist.values(), facecolor="g")
    plt.plot(rsc_hist.keys(), rsc_hist.values())
    plt.title("Resources utilization by civilizations")
    
    plt.show()
    
    
if __name__ == "__main__":
    main()
