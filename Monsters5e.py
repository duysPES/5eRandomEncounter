#!/usr/bin/env python
import numpy as np
import configparser, csv, sys, argparse, random

class Monster(object):
    def __init__(self, minfo, header):
        '''self.Name = minfo[0]
        self.Type = minfo[1]
        self.Alignment = minfo[2]
        self.Size = minfo[3]
        self.AC   = minfo[5]
        self.HP = minfo[6]
        self.Spellcaster = minfo[7]
        self.A1D = minfo[8]
        self.A2D = minfo[9]
        self.Page = minfo[10]
        self.CR = minfo[11]
        self.inArtic = minfo[12]
        self.inCoast = minfo[13]
        self.inDesert = minfo[14]
        self.inForest = minfo[15]
        self.inGrassland = minfo[16]
        self.inHill = minfo[17]
        self.inMountain = minfo[18]
        self.inSwamp = minfo[19]
        self.inUnderdark = minfo[20]
        self.inUnderwater = minfo[21]
        '''
        
        self.Info = {}
        counter = 0
        for item in minfo:
            self.Info[header[counter]] = item
            counter += 1
        

class MonsterStorage(object):
    def __init__(self, fpath):
        monsters = []
        self.Monsters = []
        with open(fpath) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            for row in csv_reader:
                monsters.append(row)
                
                
        self.Storage = np.array(monsters)
        self.Header = self.Storage[0]
        
        cnt = 0
        for row in self.Storage:
            if cnt == 0:
                cnt += 1
                continue
            
            self.Monsters.append(Monster(row, self.Header))
                
        
        self.Cr2XP =[
          0,    # buffer so index matches CR
        200,    # CR 1
        450,
        700,
        1100,
        1800,
        2300,
        2900,
        3900,
        5000,
        5900,
        7200,
        8400,
        10000,
        11500,
        13000,
        15000,
        18000,
        20000,
        22000,
        25000,
        33000,
        41000,
        50000,
        62000,
        75000   # CR 25
        
        ]
        
    def monstersBelowXP(self, pthreshold):
        ms = []
        for m in self.Monsters:
            if self.CRtoXP(m) <= pthreshold:
                ms.append(m)
        
        return ms
        
        
    def CRtoXP(self, cr_decimal):
        try:
            cr = float(cr_decimal)
        except:
            cr = 0
        if cr == 0:
            return 10.0
        elif cr == 0.25:
            return 50
        elif cr == 0.50:
            return 100
        else:
            return self.Cr2XP[int(cr)]
            
    def CRtoXP(self, monster):
        try:
            cr = float(monster.Info['CR (Decimal)'])
        except:
            cr = float(eval(monster.Info['CR']))
            
        if cr == 0:
            return 10.0
        elif cr == 0.25:
            return 50
        elif cr == 0.50:
            return 100
        else:
            try:
                return self.Cr2XP[int(cr)]
            except:
                return self.Cr2XP[-1]
        

class PlayerStorage(object):
    def __init__(self, fpath):
        self.players = configparser.ConfigParser()
        self.players.read(fpath)
        self.XpThresholdsByLvl = [
            # ex: level 5 hard threshold =
            # self.XpThresholdsByLvl[5][2]
            [0,0,0],     
            [25, 50, 75, 100],     # lvl 1
            [50, 100, 150, 200],
            [75, 150, 225, 400],
            [125, 250, 375, 500],
            [250, 500, 750, 1100],
            [300, 600, 900, 1400],
            [350, 750, 1100, 1700],
            [450, 900, 1400, 2100],
            [550, 1100, 1600, 2400],
            [600, 1200, 1900, 2800],   # lvl 10
            [800, 1600, 2400, 3600],
            [1000, 2000, 3000, 4500],
            [1100, 2200, 3400, 5100],
            [1250, 2500, 3800, 5700],
            [1400, 2800, 4300, 6400],
            [1600, 3200, 4800, 7200],
            [2000, 3900, 5900, 8800],
            [2100, 4200, 6300, 9500],
            [2400, 4900, 7300, 10900],
            [2800, 5700, 8500, 12700]    # lvl 20
        ]
        
        # add total player levels
        self.XpThreshold = 0

                    
        
    def PartyXpThreshold(self, difficulty):
        counter = 0
        
        for player in self.Players():
            for item in self.players[player]:
                if item == 'level':
                    level = int(self.players[player][item])
                    threshold = self.XpThresholdsByLvl[level][difficulty]
                    counter += threshold
                    #print player, counter, level, threshold
                    break
                    
        return counter
                    
                        
    def Players(self):
        return self.players.sections()


def EncounterMulti(nmonsters):
    m = nmonsters
    if m ==1:
        return 1.0
    if m == 2:
        return 1.5
    if m >= 3 or m <=6:
        return 2.0
    if m >=7 or m <= 10:
        return 2.5
    if m >= 11 or m <= 14:
        return 3.0
    
    return 4.0


def isclose(a, b, rel_tol=0.1, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)
    
    
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description="Build Random Encounters for DND 5e", prog=sys.argv[0])
    parser.add_argument('--mfile', help="File containing monsters")
    parser.add_argument('--pfile', help=".ini file contain player info")
    parser.add_argument('-D', choices=[0,1,2,3], type=int, help="Difficulty of the encounter")
    parser.add_argument('-N', help='Number of monsters wanted in encounter', type=int)
    args = vars(parser.parse_args())
    
    monsters = MonsterStorage(args['mfile'])
    players = PlayerStorage(args['pfile'])
    num_of_monsters = args['N']
    difficulty = args['D']
    
    players_threshold = players.PartyXpThreshold(difficulty)
    appropriate_monsters = monsters.monstersBelowXP(players_threshold)
    
    found_match = False
    rmonsters = []
    monsters_threshold = 0
    
    while(not found_match):
        
        for i in range(0,num_of_monsters):
            rmon = random.choice(appropriate_monsters)
            monsters_threshold += monsters.CRtoXP(rmon)
            rmonsters.append(rmon)
            
        monsters_threshold *= EncounterMulti(num_of_monsters)
        thres = abs(monsters_threshold - players_threshold)
        #print thres
        if not isclose(monsters_threshold, players_threshold):
            rmonsters = []
            monsters_threshold = 0
            continue
        
        found_match = True
        
        print("\nPlayers threshold: %s\t Monsters Threshold: %s\t Abs: %s\n" % (players_threshold, monsters_threshold, thres))
    
    for m in rmonsters:
        print("Monster: [%30s]\tCR: [%3s]\t XP: [%10s]\tBook: [%30s/%3s]" % (m.Info['Name'], m.Info["CR"], monsters.CRtoXP(m), m.Info['Book'], m.Info['Page']))   
            
        
        
        
        
        
        
    
    
    
  
