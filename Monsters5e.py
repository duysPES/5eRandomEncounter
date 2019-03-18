#!/usr/bin/env python
import numpy as np
import configparser, csv, sys, argparse

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
        
    
    def CRtoXP(self, cr_decimal):
        cr = float(cr_decimal)
        if cr == 0:
            return 10.0
        elif cr == 0.25:
            return 50
        elif cr == 0.50:
            return 100
        else:
            return self.Cr2XP[int(cr)]
        
        

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



if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description="Build Random Encounters for DND 5e", prog=sys.argv[0])
    parser.add_argument('--mfile', help="File containing monsters")
    parser.add_argument('--pfile', help=".ini file contain player info")
    parser.add_argument('-D', choices=[0,1,2,3], type=int, help="Difficulty of the encounter")
    parser.add_argument('-N', help='Number of monsters wanted in encounter', type=int)
    args = vars(parser.parse_args())
    monsters = MonsterStorage(args['mfile'])
    players = PlayerStorage(args['pfile'])
    
    print(players.PartyXpThreshold(0))
    monster = monsters.Storage[34]
    print(monster[0], monsters.CRtoXP(monster[11]))
    print(monsters.Monsters[0].Info)
    print(monsters.Monsters[0].Info['CR (Decimal)'],
            monsters.CRtoXP(monsters.Monsters[0].Info['CR (Decimal)']))
  
