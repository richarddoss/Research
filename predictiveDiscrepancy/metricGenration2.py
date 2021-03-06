from collections import defaultdict
import collections
import time
import re
import csv
import matplotlib.pyplot as plt
import numpy as np
import function as f

#season 2016-2017
csv_file1 = open('TeamMatchups.csv', 'r')
reader1 = csv.reader(csv_file1)
i = 0
j = 0
noOfPredictions = 0
minutesPlayed = defaultdict(dict)
minutesPlayedEstimate = defaultdict(dict)
NumberMinutes=defaultdict(dict)
playerRating = defaultdict(dict)
plusminus = defaultdict(dict)
duplicate = defaultdict(dict)
tempTeam = defaultdict(dict)
check = defaultdict(dict)
TeamRating = defaultdict(dict)
HomeAdv = defaultdict(dict)
checklist = []
flog = 1
match = 0
avg=[]
number=0
flag=0
Dray=[]
James=[]
Bruno=[]
Curry=[]
Jordan=[]
CLE=[]
for row1 in reader1:
    plusminus1 = defaultdict(dict)
    plusminus2 = defaultdict(dict)
    if i > 0:
        s = re.split('\W+', row1[2])
        # print(s)
        if len(s) == 2:
            Team1 = s[0]
            Team2 = s[1]
            flag=1
            c = Team1 + Team2
            HomeAdv[Team1]=0
            HomeAdv[Team2]=100
        if (flag==1):
            flag=0
            for fixedPlayer in minutesPlayed[Team1]:
                minutesPlayed[Team1][fixedPlayer] = 0
                plusminus1[fixedPlayer]=0
            for fixedPlayer in minutesPlayed[Team2]:
                minutesPlayed[Team2][fixedPlayer] = 0
                plusminus2[fixedPlayer]=0
            csv_file2 = open('PlayerDetails.csv', 'r')
            reader2 = csv.reader(csv_file2)
            for row2 in reader2:
                if j > 0:

                    if (Team1 == row2[1] or Team2 == row2[1]) and row1[1] == row2[2]:
                        # print(row2[0],"playername",row2[1],"team",row2[2],"date")
                        # time.sleep(2)
                        if int(row2[5])!=0:
                            avg.append(int(row2[6])/int(row2[5]))
                            number+=1
                        if Team1 == row2[1]:
                            minutesPlayed[Team1][row2[0]+Team1] = int(row2[5]) / (int(row1[4]))
                            plusminus1[row2[0]+Team1] = int(row2[7])
                            if check[row2[0]+Team1] == {}:
                                playerRating[row2[0]+Team1] = 1000
                                #print(row2[0])
                                check[row2[0]+Team1] = 'Filled'
                        elif Team2==row2[1]:
                            minutesPlayed[Team2][row2[0]+Team2] = int(row2[5]) / (int(row1[4]))
                            plusminus2[row2[0]+Team2] = int(row2[7])
                            if check[row2[0]+Team2] == {}:
                                playerRating[row2[0]+Team2] = 1000
                                #print(row2[0])
                                check[row2[0]+Team2] = 'Filled'
                        else:
                            print("HHHHHHHHHEEEEEEEEEEELLLLLLLLLLOOOOOOOOOOOOOOOOOOOOOOOOOOO")
                j = j + 1
            j = 0
            csv_file2.close()
            checklist.append(c)
            for fixedPlayer in minutesPlayed[Team1]:
                if minutesPlayedEstimate[fixedPlayer] == {}:
                    #print(fixedPlayer)
                    minutesPlayedEstimate[fixedPlayer] = minutesPlayed[Team1][fixedPlayer]
                    NumberMinutes[fixedPlayer] = 1
                else:
                    minutesPlayedEstimate[fixedPlayer] = (NumberMinutes[fixedPlayer] * minutesPlayedEstimate[fixedPlayer] +
                                                      minutesPlayed[Team1][fixedPlayer]) / (NumberMinutes[fixedPlayer] + 1)
                    NumberMinutes[fixedPlayer] = NumberMinutes[fixedPlayer] + 1
            for fixedPlayer in minutesPlayed[Team2]:
                if minutesPlayedEstimate[fixedPlayer] == {}:
                    minutesPlayedEstimate[fixedPlayer] = minutesPlayed[Team2][fixedPlayer]
                    NumberMinutes[fixedPlayer] = 1
                else:
                    minutesPlayedEstimate[fixedPlayer] = (NumberMinutes[fixedPlayer] * minutesPlayedEstimate[fixedPlayer] +
                                                      minutesPlayed[Team2][fixedPlayer]) / (NumberMinutes[fixedPlayer] + 1)
                    NumberMinutes[fixedPlayer] = NumberMinutes[fixedPlayer] + 1

            # rating update for the 2 teams
            m1 = 0
            m2 = 0
            p1=0
            p2=0
            for players in minutesPlayed[Team1]:
                m1 += playerRating[players] * minutesPlayedEstimate[players]
                p1+=playerRating[players]
            for players in minutesPlayed[Team2]:
                m2 += playerRating[players] * minutesPlayedEstimate[players]
                p2+=playerRating[players]
            #print("%%%%%%%%%%%%%%%%%  Before Update %%%%%%%%%%%%%%%%")
            #print("Updated rating for {}".format(Team1), round(p1))
            #print("updated rating for {}".format(Team2), round(p2))
            #print("p2",p2)
            #print("total1",p1+p2)
            sumTeam = 0
            for Teeam in minutesPlayed:
                for player in minutesPlayed[Teeam]:
                    sumTeam = sumTeam + playerRating[player]
                    # print(Teeam,TeamRating[Teeam])
            #print(Team1,p1)
            #print(Team2,p2)
            #print("total1",p1+p2)
            #print("Sum of team rating1", sumTeam)
            #time.sleep(2)
            m1+=HomeAdv[Team1]
            m2 += HomeAdv[Team2]
            if m1 > m2:
                outcome = 'W'
            else:
                outcome = 'L'
            if outcome == row1[3]:
                noOfPredictions = noOfPredictions + 1
                W = 1
            else:
                W = 0
            match = match + 1
            print(Team1, m1, row1[3], Team2, m2, noOfPredictions, match,"Prediction Rate",noOfPredictions/match)
            playerRating= f.elo(playerRating, minutesPlayed, Team1, Team2, int(row1[4]), plusminus1, plusminus2, 500, 10000)
            if Team1=="UTA" or Team2=="UTA":
                #print(playerRating["Draymond GreenGSW"])
                #Dray.append(playerRating["Draymond GreenGSW"])
                if playerRating["Gordon HaywardUTA"]!={}:
                    print("Gordon Hayward", playerRating["Gordon HaywardUTA"])
                    Curry.append(playerRating["Gordon HaywardUTA"])
                else:
                    Curry.append(0)
            if Team1=="CLE" or Team2=="CLE":
                James.append(playerRating["LeBron JamesCLE"])
            if Team1=="TOR" or Team2=="TOR":
                if playerRating["Bruno CabocloTOR"]!={}:
                    Bruno.append(playerRating["Bruno CabocloTOR"])
            if Team1=="LAC" or Team2=="LAC":
                if playerRating["DeAndre JordanLAC"]!={}:
                    Jordan.append(playerRating["DeAndre JordanLAC"])
            m1 = 0
            m2 = 0
            p1=0
            p2=0
            for players in minutesPlayed[Team1]:
                m1 += playerRating[players] * minutesPlayedEstimate[players]
                p1+=playerRating[players]
            for players in minutesPlayed[Team2]:
                m2 += playerRating[players] * minutesPlayedEstimate[players]
                p2+=playerRating[players]
            if Team1=="UTA":
                CLE.append(m1)
                print("UTA",m1)
            elif Team2=="UTA":
                CLE.append(m2)
                print("UTA",m2)
            TeamRating[Team1] = m1
            TeamRating[Team2] = m2
    i = i + 1

SUM=sum(avg)    # computing the constant value
#print("average",SUM/number)
csv_file1.close()
#print(Dray)
#print(Bruno)
Dray=np.array(Dray)
James=np.array(James)
Bruno=np.array(Bruno)
Curry=np.array(Curry)
Jordan=np.array(Jordan)
CLE=np.array(CLE)
#plt.plot(Dray,label="Draymond Green")
#plt.plot(James,label="LeBron James")
#plt.plot(Bruno,label="Bruno Caboclo")
plt.plot(Curry,label="Steph Curry")
#plt.plot(Jordan,label="DeAndre Jordan")
plt.plot(CLE,label="CLE")
plt.xlabel("Game number")
plt.ylabel("Player Rating")
plt.title("Rating comparison of LeBron James and Draymond Green")
plt.legend()
plt.show()


