# -*- coding: utf-8 -*-
"""
Created on Sun Apr  9 14:57:49 2017

@author: doopleganger
"""
import csv
import pickle

class CsvReader:
    
    def __init__(self):
        self.description = "module de parsing d'un fichier CSV"
    
    def convertBase(self, file):
        with open(file, newline='') as csvfile:
            
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            
            
            
            base = {}        
            idplayer = 0
            
            tag = "player"
            
            for r in reader:

                player = {}
                
                idplayer += 1
                
                lname = r[2]
                fname = r[3]
                
                name = str(lname.lower()) + ", " + str(fname.lower())
                
                gender = r[4]
                elo = r[9]
                country = r[7]
                

                cNat = ConvertNat()
                country = cNat.convert(country)
                
                player.update({"name":name, "sexe":gender, "nat":country, "elo":elo})
                base.update({tag+str(idplayer):player})
            
            
            output = open("../data/output/baseplayer.txt", 'ab+')
            pickle.dump(base, output)
            
          
            
if __name__ == "__main__":
    #csvReader = CsvReader()
    #csvReader.convertBase("../data/csv/JOUEURS.csv")
    
        
    test = open("../data/output/baseplayer.txt", 'rb')
    playerdic = pickle.load(test)
        
    for p in playerdic:
       if(playerdic[p]['name'] in "jacobsen, bo"):
           print(playerdic[p]['name'], playerdic[p]['nat'])
       
    

