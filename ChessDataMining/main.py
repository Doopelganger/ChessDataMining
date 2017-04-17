# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 13:24:02 2017

@author: 21003607
"""
import time

import chess
import chess.uci
import chess.pgn

import pickle

import parser.readPGN
import parser.convertECO
import parser.convertP
import parser.predictOracle

import classifier
import parser

#####################################
### Fonction de creation dico pgn ###
#####################################
def build():
    # init du lecteur PGN
    reader = ReadPGN()
    '''
    Ecriture Dico
    '''
    # lecture du fichier PGN - creation du dictionnaire - a faire une seule fois
    dico = reader.build("data/pgn/train.pgn")
    output = open("data/output/codex.txt", 'ab+')
    # ecriture du dictionnaire
    pickle.dump(dico, output)
    output.close
    

#=============================================================#
    
#####################################
### Fonction de calcul des traits ###
#####################################
def main():
    
    start = time.clock()
    """
    Init du moteur
    """
    engine = chess.uci.popen_engine("stockfish/Linux/stockfish_8_x64")
    engine.uci()
    info_handler = chess.uci.InfoHandler()
    engine.info_handlers.append(info_handler)
    
    """
    Init des outils
    """
    conv_ECO = ConvertECO()
    conv_NAT = ConvertNat()
    conv_P = ConvertP()
    oracle = PredictOracle()

    
    #########################
    
    '''
    Lecture Dico
    '''
    # recuperation du dictionnaire
    intels = open('data/output/codex.txt', 'rb')
    gamedic = pickle.load(intels)

    """
    Traitement des parties
    parsing pour 10 / 15 / 20 / 30 traits
    """
    
    result5 = open("data/vectors/vectors_5f.txt", 'w')
    elos5 = open("data/vectors/elos_5f.txt", 'w')
    
    result10 = open("data/vectors/vectors_10f.txt", 'w')
    elos10 = open("data/vectors/elos_10f.txt", 'w')
    
    result15 = open("data/vectors/vectors_15f.txt", 'w')
    elos15 = open("data/vectors/elos_15f.txt", 'w')
    
    result20 = open("data/vectors/vectors_20f.txt", 'w')
    elos20 = open("data/vectors/elos_20f.txt", 'w')
    
    result30 = open("data/vectors/vectors_30f.txt", 'w')
    elos30 = open("data/vectors/elos_30f.txt", 'w')
    
    #########################
    
    cp = 0
    
    for g in gamedic:
        
        cp += 1
        
        # joueurs
        # print(gamedic[g]['white'])
        # white = gamedic[g]['white']
        # black = gamedic[g]['black']
        print("game")
        # ouverture             
        eco = gamedic[g]['eco']
        # rankings elo
        white_elo = gamedic[g]['whiteElo']
        black_elo = gamedic[g]['blackElo']        
        code_elo_W = 0        
        code_elo_B = 0
        
        if(int(white_elo) > 2400):
            code_elo_W = "master"
        else:
            code_elo_W = "not_master"
            
        if(int(black_elo) > 2400):
            code_elo_B = "master"
        else:
            code_elo_B = "not_master"
        
        # nationalite
        white_nat = gamedic[g]['whiteNat']
        black_nat = gamedic[g]['blackNat']

        # sexe
        white_gen = gamedic[g]['whiteGen']
        black_gen = gamedic[g]['blackGen']
        
        # tag pour marquer le joueur actif
        colors = ['W', 'B']
        i = 0
        
        # liste des coups
        moves = gamedic[g]['moves']
        
        #########################
        #### init des traits ####
        #########################
        
        # nombre de coups
        nb_moves = 0
        nb_W = 0
        nb_B = 0
        
        ### score Oracle ###
        # moyenne score Oracle sur 10 / 25 coups / total
        moy10_oracle_W = 0
        moy25_oracle_W = 0
        
        moy10_oracle_B = 0
        moy25_oracle_B = 0
        
        moy_oracle_W = 0
        moy_oracle_B = 0
        
        # plus grande serie de meilleurs coups consecutifs
        serie_W = 0
        serie_B = 0
        
        # nombre de meilleurs coups
        best_W = 0
        best_B = 0
        
        maxW = 0
        maxB = 0     

    
        ### distance cp ###
        # moyenne distance cp sur 10 /25 coups / total
        
        dist10_W = 0
        dist25_W = 0
        
        dist10_B = 0
        dist25_B = 0
        
        dist_W = 0
        dist_B = 0

        dist_max_W = 0
        dist_max_B = 0        
        
        dist_min_W = 0
        dist_min_B = 0
        
        min_cp_W = 0
        min_cp_B = 0
        
        max_cp_W = 0
        max_cp_B = 0
        
        var_W = []
        var_B = []
        
        
        # nombre de mises en echec par W / B
        check_W = 0
        check_B = 0

        ### roque ###
        # type de Roque : 1 pour petit, 2 pour grand, 0 sinon
        castling_W = 0
        castling_B = 0
        
        # timer indiquant apres combien de coups le Roque a ete effectue, si 0, non effectue
        timer_castling_W = 0
        timer_castling_B = 0
        
        # premiere piece jouee
        first_W = ""
        first_B = ""
        
        # premiere piece jouee deux fois
        first_double_W = ""
        first_double_B = ""
        
        # piece la plus jouee
        most_played_W = 0
        most_played_B = 0
        
        # ratio coups P sur les 10 | 20 premiers coups
        ratio10P_W = 0
        ratio10P_B = 0
        
        ratio20P_W = 0
        ratio20P_B = 0
        
        # ratio coups N sur les 10 | 20 premiers coups        
        ratio10N_W = 0
        ratio10N_B = 0        
            
        ratio20N_W = 0
        ratio20N_B = 0
        
        
        # decompte des mouvements pour chaque type de piece K / Q / B / N / R / P
        # pour white
        k_W = 0
        q_W = 0
        b_W = 0
        n_W = 0
        r_W = 0
        p_W = 0
        
        # pour black
        k_B = 0
        q_B = 0
        b_B = 0
        n_B = 0
        r_B = 0
        p_B = 0
        
        
        #########################
        #########################
        #########################
        
        """
        Traitements des coups
        """
        n = len(moves)

        board = chess.Board()        
        
        for m in range (1, n):
            
            # un coup est un tuple (node, move)
            # le node est un SAN : ex : e4
            # le move est le movement complet : e2e4
            node = moves[str(m)]['node']
            move = moves[str(m)]['move']           
            
            # tag pour identifier le joueur courant
            player = colors[i]
            
            # decompte des coups
            nb_moves += 1
            i = (i+1)%2
            
            # decompte du nombre de coups pour chaque joueur
            if(player == 'W'):
                nb_W += 1
            else:
                nb_B += 1
                
            ### Recup Petit ou Grand Roque ###
            if("O-O" in node):
                if(player == 'W'):
                    castling_W = 1
                    timer_castling_W = nb_moves
                    k_W += 1
                    r_W += 1
                else :
                    castling_B = 1
                    timer_castling_B = nb_moves
                    k_B += 1
                    r_B += 1
                
            elif("O-O-O" in node):
                if(player == 'W'):
                    castling_W = 2
                    timer_castling_W = nb_moves
                    k_W += 1
                    r_W += 1
                    
                else :
                    castling_B = 2
                    timer_castling_B = nb_moves
                    k_B += 1
                    r_B += 1
            
            ### Recup decompte attaques ###
            if("+" in node):
                if(player == 'W'):
                    check_W += 1
                else:
                    check_B += 1
            
            ### Recup premiere piece jouee et decompte des moves pour chaque piece ###
            pieces = 'KQBNR'
            p = node[0]
            if(p in pieces):
                if(player == "W" and first_W ==""):
                    first_W = conv_P.symbolP(p)
                elif(first_B == ""):
                    first_B = conv_P.symbolP(p)
                
                if(p == 'K'):
                    if(player == 'W'):
                        k_W += 1
                    else:
                        k_B += 1
                        
                elif(p == 'Q'):
                    if(player == 'W'):
                        q_W += 1
                    else:
                        q_B += 1
                        
                elif(p == 'B'):
                    if(player == 'W'):
                        b_W += 1
                    else:
                        b_B += 1
                        
                elif(p == 'N'):
                    if(player == 'W'):
                        n_W += 1
                    else:
                        n_B += 1
                        
                elif(p == 'R'):
                    if(player == 'W'):
                        r_W += 1
                    else:
                        r_B += 1
            
            else:
                if(player == 'W'):
                    p_W += 1
                else:
                    p_B += 1
                        
            ### Recup premiere piece jouee deux fois ###
            if(k_W == 2 and first_double_W == ""):
                first_double_W = conv_P.symbolP('K')
                
            elif(q_W == 2 and first_double_W == ""):
                first_double_W = conv_P.symbolP('Q')
                
            elif(b_W == 2 and first_double_W == ""):
                first_double_W = conv_P.symbolP('B')
                
            elif(n_W == 2 and first_double_W == ""):
                first_double_W = conv_P.symbolP('N')
                
            elif(r_W == 2 and first_double_W == ""):
                first_double_W = conv_P.symbolP('R')
                
                
            if(k_B == 2 and first_double_B == ""):
                first_double_B = conv_P.symbolP('K')
                
            elif(q_B == 2 and first_double_B == ""):
                first_double_B = conv_P.symbolP('Q')
                
            elif(b_B == 2 and first_double_W == ""):
                first_double_B = conv_P.symbolP('B')
                
            elif(n_B == 2 and first_double_B == ""):
                first_double_B = conv_P.symbolP('N')
                
            elif(r_B == 2 and first_double_B == ""):
                first_double_B = conv_P.symbolP('R')
            
            ### Decompte Ratios P / K / B sur 10 / 20 premiers coups ###
            
            if(nb_W == 10):
                ratio10P_W = p_W / 10
                ratio10N_W = n_W / 10
                ratio10B_W = b_W / 10
            
            if(nb_B == 10):
                ratio10P_B = p_B / 10
                ratio10N_B = n_B / 10
                ratio10B_B = b_B / 10
                
            if(nb_W == 20):
                ratio20P_W = p_W / 20
                ratio20N_W = n_W / 20
                ratio20B_W = b_W /20
                
            if(nb_B == 20):
                ratio20P_B = p_B / 20
                ratio20N_B = n_B / 20
                ratio20B_B = b_B /20
                
            #########################
            #### calculs Moteur  ####
            #########################
            
            # positionnement de stockFish sur le board courant
            engine.position(board)
            
            ### calculs meilleur coup et moyenne oracle sur 10 / 25 coups ###
            # fonction custom pour determiner le meilleur coup et les score cp
            prediction = oracle.predict(board, move, engine, info_handler)
            bestmove = prediction[0]
            score_oracle = prediction[1]
            score_player = prediction[2]
            

            # si le coup joue correspond au coup oracle
            if str(move) == str(bestmove):
                # on augmente de 1 le score Oracle du joueur
                # on augmente de 1 la serie de coup en accord avec l'Oracle
                if(player == "W"):
                    best_W += 1
                    serie_W += 1
                else:
                    best_B += 1
                    serie_B += 1
                # print("w" + str(white_serie))
                # print("b" + str(black_serie))
            else:
                # si le coup joue ne correspond pas
                # on fixe un max temporaire et on reset la serie
                if(player == "W"):
                    if(maxW < serie_W):
                        maxW = serie_W
                    serie_W = 0
                else:
                    if(maxB < serie_B):
                        maxB = serie_B
                    serie_B = 0           
                
            # moy score Oracle sur 10 coups
            if(nb_W == 10 and player == 'W'):
                moy10_oracle_W = best_W/10
            if(nb_B == 10 and player == 'B'):
               moy10_oracle_B = best_B/10
                
            # moy score Oracle sur 25 coups
            if(nb_W == 25 and player == 'W'):
                moy25_oracle_W = best_W/25
            if(nb_B == 25 and player == 'B'):
                moy25_oracle_B = best_B/25
                    
            
            board.push_san(node)
            
            ### calculs score cp et distance player-oracle sur 10 / 25 coups ###
            # garde fou : le score cp peut etre None, par defaut on fixe le score en question a 0, la distance sera le max entre 0 et l'autre valeur
            if(score_oracle is None):
                score_oracle = int(0)
                
            if(score_player is None):
                score_player = int(0)
                
            if(player == 'W'):
                if(score_player == 0 or score_oracle == 0):
                    dist_W = max(int(score_oracle), int(score_player))
                else:    
                    dist_W = int(score_oracle) - int(score_player)
                if nb_moves == 1:
                    min_cp_W = max_cp_W = score_player
                    dist_min_W = dist_max_W = dist_W
                else:
                    min_cp_W = min(min_cp_W, score_player)
                    max_cp_W = max(max_cp_W, score_player)
                    
                    dist_min_W = min(dist_min_W, dist_W)
                    dist_max_W = max(dist_max_W, dist_W)
                    
                var_W.append(dist_W)
            else:
                 if(score_player == 0 or score_oracle == 0):
                    dist_B = max(int(score_oracle), int(score_player))
                 else:
                    dist_B = int(score_oracle) - int(score_player)
                 if nb_moves == 1:
                    min_cp_B = max_cp_B = score_player
                    dist_min_B = dist_max_B = dist_B
                 else:
                    min_cp_B = min(min_cp_B, score_player)
                    max_cp_B = max(max_cp_B, score_player)
                    
                    dist_min_B = min(dist_min_B, dist_B)
                    dist_max_B = max(dist_max_B, dist_B)
                    
                 var_B.append(dist_B)
            
            # moy distance sur 10 coups
            if(nb_W == 10 and player == 'W'):
                dist10_W = dist_W/10
            if(nb_B == 10 and player == 'B'):
                dist10_B = dist_B/10
                
            # moy distance sur 25 coups
            if(nb_W == 25 and player == 'W'):
                dist25_W = dist_W/25
            if(nb_B == 25 and player == 'B'):
                dist25_B = dist_B/25

          
        # moyenne du score Oracle pour chaque joueur
        moy_oracle_W = float("{0:.2f}".format(best_W / nb_W))
        moy_oracle_B = float("{0:.2f}".format(best_B / nb_B))
        
        serie_W = max(maxW, serie_W)        
        serie_B = max(maxB, serie_B)     
        
        # moyenne de la distance entre les scores des joueurs et l'oracle 
        dist_W = float("{0:.2f}".format(dist_W / nb_W))
        dist_B = float("{0:.2f}".format(dist_B / nb_B))
    
        e_dist_W = 0 
        e_dist_B = 0
        
        for x in var_W:
            e_dist_W = ((x-dist_W)**2 / nb_W)
        for y in var_B:
            e_dist_B = ((y-dist_B)**2 / nb_B)
            
        e_dist_W = float("{0:.2f}".format(e_dist_W**0.5))
        e_dist_B = float("{0:.2f}".format(e_dist_B**0.5))
        
        # piece la plus jouee
        # pour W
        max_p_W = max(q_W, k_W, b_W, n_W, r_W)
        if max_p_W == k_W:            
            most_played_W = 0
        elif  max_p_W == q_W:      
            most_played_W = 1
        elif  max_p_W == b_W:      
            most_played_W = 2
        elif  max_p_W == n_W:      
            most_played_W = 3
        elif  max_p_W == r_W:      
            most_played_W = 4
            
        # pour B
        max_p_B = max(q_B, k_B, b_B, n_B, r_B)
        if max_p_B == k_B:            
            most_played_B = 0
        elif  max_p_B == q_B:      
            most_played_B = 1
        elif  max_p_B == b_B:      
            most_played_B = 2
        elif  max_p_B == n_B:      
            most_played_B = 3
        elif  max_p_B == r_B:      
            most_played_B = 4
        
        # code ECO
        eco = conv_ECO.convert(eco)
        
        # sexe joueur
        if(white_gen == 'M'):
            white_gen = 0
        else:
            white_gen = 1
            
        if(black_gen == 'M'):
            black_gen = 0
        else:
            black_gen = 1
        

        """
        Ecriture des resultats pour 5 traits
        format : classe | eco | moy_oracle | serie | nb moves | first
        """        
        line5W = str(code_elo_W) +"\t"+ str(eco) +" "+ str(moy_oracle_W) +" "+ str(serie_W) +" "+ str(nb_W) +" "+ str(first_W) +'\n'
        line5B = str(code_elo_B) +"\t"+ str(eco) +" "+ str(moy_oracle_B) +" "+ str(serie_B) +" "+ str(nb_B) +" "+ str(first_B) +'\n'
        
        result5.write(line5W)
        result5.write(line5B)
    
        elos5.write(str(white_elo) +'\n')
        elos5.write(str(black_elo) +'\n')
        
        """
        Ecriture des resultats pour 10 traits
        format : classe | eco | dist_moy | moy_oracle | serie | best_moves | nb moves | first | attaques | moves Q | castling
        """     
        line10W = str(code_elo_W) +"\t"+ str(eco) +" "+ str(dist_W) +" "+ str(moy_oracle_W) +" "+ str(serie_W) +" "+ str(best_W) +" "+ str(nb_W) +" "+ str(eco) +" "+ str(first_W) +" "+ str(check_W) +" "+ str(castling_W) +'\n'
        line10B = str(code_elo_B) +"\t"+ str(eco) +" "+ str(dist_B) +" "+ str(moy_oracle_B) +" "+ str(serie_B) +" "+ str(best_B) +" "+ str(nb_B) +" "+ str(eco) +" "+ str(first_B) +" "+ str(check_B) +" "+ str(castling_B) +'\n'
        
        result10.write(line10W)
        result10.write(line10B)
        
        elos10.write(str(white_elo) +'\n')
        elos10.write(str(black_elo) +'\n')
        
        """
        Ecriture des resultats pour 15 traits
        format : classe | eco | dist_moy | dist_min | dist_max | moy_oracle | serie | best_moves | cp_min | cp_max | nb moves | first | first_double | attaques | moves Q | castling 
        """  
        line15W = str(code_elo_W) +"\t"+ str(eco) +" "+ str(dist_W) +" "+ str(dist_min_W) +" "+ str(dist_max_W) +" "+ str(moy_oracle_W) +" "+ str(serie_W) +" "+ str(best_W) +" "+ str(min_cp_W) +" "+ str(max_cp_W) +" "+ str(nb_W) +" "+ str(first_W) +" "+ str(first_double_W) +" "+ str(check_W) +" "+ str(q_W) +" "+ str(castling_W) +'\n'
        line15B = str(code_elo_B) +"\t"+ str(eco) +" "+ str(dist_B) +" "+ str(dist_min_B) +" "+ str(dist_max_B) +" "+ str(moy_oracle_B) +" "+ str(serie_B) +" "+ str(best_B) +" "+ str(min_cp_B) +" "+ str(max_cp_B) +" "+ str(nb_B) +" "+ str(first_B) +" "+ str(first_double_B) +" "+ str(check_B) +" "+ str(q_B) +" "+ str(castling_B) +'\n'

        result15.write(line15W)
        result15.write(line15B)
        
        elos15.write(str(white_elo) +'\n')
        elos15.write(str(black_elo) +'\n')
        
        """
        Ecriture des resultats pour 20 traits
        format : classe | eco | dist_moy | dist_min | dist_max | dist10 | dist25 | moy oracle 10 | moy oracle 25 | moy_oracle | serie | best_moves | cp_min | cp_max | nb moves | first | first_double | attaques | moves Q | castling | timer_castling
        """  
        line20W = str(code_elo_W) +"\t"+ str(eco) +""+ str(dist_W) +" "+ str(dist_min_W) +" "+ str(dist_max_W) +" "+ str(dist10_W) +" "+ str(dist25_W) +" "+ str(moy10_oracle_W) + " "+ str(moy25_oracle_W) +" "+ str(moy_oracle_W) +" "+ str(serie_W) +" "+ str(best_W) +" "+ str(min_cp_W) +" "+ str(max_cp_W) +" "+ str(nb_W) +" "+ str(first_W) +" "+ str(first_double_W) +" "+ str(check_W) +" "+ str(q_W) +" "+ str(castling_W) +" "+ str(timer_castling_W) +'\n'
        line20B = str(code_elo_B) +"\t"+ str(eco) +" "+ str(dist_B) +" "+ str(dist_min_B) +" "+ str(dist_max_B) +" "+ str(dist10_B) +" "+ str(dist25_B) +" "+ str(moy10_oracle_B) +" "+ str(moy25_oracle_B) +" "+ str(moy_oracle_B) +" "+ str(serie_B) +" "+ str(best_B) +" "+ str(min_cp_B) +" "+ str(max_cp_B) +" "+ str(nb_B) +" "+ str(first_B) +" "+ str(first_double_B) +" "+ str(check_B) +" "+ str(q_B) +" "+ str(castling_B) +" "+ str(timer_castling_B) +'\n'
        
        result20.write(line20W)
        result20.write(line20B)
        
        elos20.write(str(white_elo) +'\n')
        elos20.write(str(black_elo) +'\n')
        
        """
        Ecriture des resultats  pour 30 traits
        format : classe | Nat | Sexe | eco | dist_min | dist_max | ecart-type | dist_moy | dist10 | dist25 | cp_min | cp_max | nb best moves | meilleure serie | moy oracle 10 | moy oracle 25 | moy oracle | nb moves player | most played | first | first double | ratio10P | ratio20P | ratio10N | ratio20N | ratio10B | ratio20B | moves Q | attaques | castling | timer castling     
        """
        line30W = str(code_elo_W) +"\t"+ str(white_nat) +" "+ str(white_gen) +" "+ str(eco) +" "+ str(dist_min_W) +" "+ str(dist_max_W) +" "+ str(e_dist_W) +" "+ str(dist_W) +" "+ str(dist10_W) +" "+ str(dist25_W) +" "+ str(min_cp_W) +" "+  str(max_cp_W) +" "+ str(best_W) +" "+ str(serie_W) +" "+ str(moy_oracle_W) +" "+ str(moy10_oracle_W) +" "+ str(moy25_oracle_W) +" "+ str(nb_W) +" "+ str(most_played_W) +" "+ str(first_W) +" "+ str(first_double_W) +" "+ str(ratio10P_W) +" "+ str(ratio20P_W) +" "+ str(ratio10N_W) +" "+ str(ratio20N_W) +" "+ str(ratio10B_W) +" "+ str(ratio20B_W) +" "+ str(q_W) +" "+ str(check_W) +" "+ str(castling_W) +" "+ str(timer_castling_W) +'\n'
        line30B = str(code_elo_B) +"\t"+ str(black_nat) +" "+ str(black_gen) +" "+ str(eco) +" "+ str(dist_min_B) +" "+ str(dist_max_B) +" "+ str(e_dist_B) +" "+ str(dist_B) +" "+ str(dist10_B) +" "+ str(dist25_B) +" "+ str(min_cp_B) +" "+  str(max_cp_B) +" "+ str(best_B) +" "+ str(serie_B) +" "+ str(moy_oracle_B) +" "+ str(moy10_oracle_B) +" "+ str(moy25_oracle_B) +" "+ str(nb_B) +" "+ str(most_played_B) +" "+ str(first_B) +" "+ str(first_double_B) +" "+ str(ratio10P_B) +" "+ str(ratio20P_B) +" "+ str(ratio10N_B) +" "+ str(ratio20N_B) +" "+ str(ratio10B_B) +" "+ str(ratio20B_B) +" "+  str(q_B) +" "+ str(check_B) +" "+ str(castling_B) +" "+ str(timer_castling_B) +'\n'

        result30.write(line30W)
        result30.write(line30B)
        
        elos30.write(str(white_elo) +'\n')        
        elos30.write(str(black_elo) +'\n')
                
        print(' ')
    
    result5.close()
    elos5.close()

    result10.close()
    elos10.close()

    result15.close()
    elos15.close()

    result20.close()
    elos20.close()
        
    result30.close()
    elos30.close()
    
    end = time.clock()
    monitor =  float("{0:.2f}".format(end - start ))
    print(' ')
    print("games traitees :", cp)
    print("timer :", monitor)


#=============================================================#
   

def classify():
    """
    Init donnees
    """
    # basiquement, une liste de string a passer au classifieur pour pouvoir nommer chaque trait
    # necessaire uniquement pour la representation graphique de l'arbre de decision
    list5f = ["eco", "moy_oracle", "serie", "nb moves", "first"]
    
    list10f = ["eco", "dist_moy", "moy_oracle", "serie", "best_moves", "nb moves", "first", "attaques", "moves Q", "castling"]
    
    list15f = ["eco", "dist_moy", "dist_min", "dist_max", "moy_oracle", "serie", "best_moves", "cp_min",
               "cp_max", "nb moves","first", "first_double", "attaques", "moves Q", "castling"]
    
    list20f = ["eco", "dist_moy", "dist_min", "dist_max", "dist10", "dist25", 
    "moy oracle10", "moy oracle 25", "moy_oracle", "serie", " best_moves", "cp_min", "cp_max",
    "nb moves", "first", "first_double", "attaques", "moves Q", "castling", "timer_castling"]
    
    list30f = ["nat", "sexe", "eco", "dist_min", "dist_max", "ecart_d", "dist_moy",
               "dist10", "dist25", "cp_min", "cp_max", "nb_best_moves", "serie", 
               "moy_oracle10", "moy_oracle25", "moy_oracle", "nb_moves", "most_played", 
               "first", "first double", "ratio10P", "ratio20P", "ratio10N", "ratio20N",
               "ratio10B", "ratio20B", "moves_Q", "attacks", "castling", "timer_castling"]
    
    
    classes = ['Master', 'nonMaster']
    
    vectors5f = "data/vectors/vectors_5f.txt"
    vectors10f = "data/vectors/vectors_10f.txt"
    vectors15f = "data/vectors/vectors_15f.txt"
    vectors20f = "data/vectors/vectors_20f.txt"
    vectors30f = "data/vectors/vectors_30f.txt"
    
    """
    Init des classifieurs
    """        
    arbre = ArbreDecision()
    svm = SupportVecteurMachine()
    kppv = KPPV()
    naif = NaifBayes()
    tree_graph = ArbreGraph()
    """
    Classifications
    """
    ########################
    ## arbres de decision ##
    ########################
    
    arbre.classify(vectors5f, classes, list5f)    
    
    ########################
    ##  classifieurs SVM  ##
    ########################     
    
    svm.classify(vectors5f, classes, list5f)
    
    ########################
    ## classifieurs kppv  ##
    ########################   
    
    kppv.classify(vectors5f, classes, list5f)
    
    ########################
    ##  classifieurs NB   ##
    ######################## 

    naif.classify(vectors5f, classes, list5f)
    
    ########################
    ##  arbre avec graph  ##
    ######################## 
    
    tree_graph.classify(vectors5f, classes, list5f)


if __name__ == "__main__":
    # pour changer l'action de main, utiliser les mots cles : build(), main(), classify()
    #main()
    classify()