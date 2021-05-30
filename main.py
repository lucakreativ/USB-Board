import time
import json

import serial
import requests

user= "lucakreativ"
meintoken="Stb8vE3X87q0qznM"

mcount=0
halb_moves=["", ""]
backs_moves=["", ""]
USB_Port="1"

#0 for nicht senden und 1 für senden
senden_ja_nein=1



felder_name=[
"a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1",
"a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2",
"a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3",
"a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4",
"a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5",
"a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6",
"a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7",
"a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8",
"z"
]
felder_name_back=felder_name[::-1]

altser_data=["x","x","x"]
filter_data=["x","x"]


lesestat=0
#time.sleep(3)

def Serial():
    #print(mcount)
    try:
        ser = serial.Serial('/dev/ttyUSB'+USB_Port, 9600)

    except serial.serialutil.SerialException:
        print("Bitte DGT-Brett anschließen")
        #print("1")
        #lesSerial()

    else:
        #print("angeschlossen")
        try:
            ser_data = ser.readline()
        except serial.serialutil.SerialException:
            print("Bitte DGT-Brett anschließen")
            #print("2")
        else:
            ser_data=str(ser_data)
            startd=ser_data.find("s//")+3
            endd=ser_data.find("//s")
            ser_data=ser_data[startd:endd]
            #print(ser_data)


            if len(ser_data)>=65:
                
                #print("Groß Genug")

                altser_data[2]=altser_data[1]
                altser_data[1]=altser_data[0]
                altser_data[0]=ser_data

                if altser_data[2]!= "x":
                    #print("nicht x")
                    #print(ser_data)
                    
                    filter_data[1]=filter_data[0]
                    filter_data[0]=altser_data[0]

                    if filter_data[1]!="x":
                        maxChanges(filter_data[0], filter_data[1], mcount)
                else:
                    print("Keine Referenz")
            else:
                print("Datenübertragung ist zu kurz")


def checkGame():
    userdatajason= requests.get("https://lichess.org/api/user/"+user)
    userdata=userdatajason.text

    posP = userdata.find("playing")

    if posP<=1250:
        #print("Spielt gerade")

        id_game=userdata[posP+30:posP+38]
        #print(id_game)
        return(id_game)
    else:
        #print("Spielt gerade nicht")
        return("0")


def maxChanges(ser_data, altser_datan, mcount):
    changesz=0
    #print(ser_data)
    if ser_data!=altser_datan:
        for i in range(65):
            if ser_data[i]!=altser_datan[i]:
                changesz+=1
    #print("Änderungen: "+str(changesz))
    Felder(ser_data, altser_datan, mcount, changesz)


def Felder(ser_data, altser_datan, mcount, changesz):
    if changesz<=2:

        for i in range(65):
            if ser_data[i]!=altser_datan[i]:
                if ser_data[i]=="0":
                    if halb_moves[0]=="":
                        ms=felder_name[i]

                        if ms!="z":
                            print("Erst: "+ms)

                            #ob es ein Schlagzug ist
                                                      
                        halb_moves[0]=ms


                elif ser_data[i]=="1":
                    if halb_moves[0]!="":
                        me=felder_name[i]

                        print("Zweit :"+me)

                        halb_moves[1]=halb_moves[0]
                        halb_moves[0]=me

                        backs_moves[1]=halb_moves[1]
                        backs_moves[0]=halb_moves[0]

                        #if halb_moves[0]==halb_moves[1]:
                            #mcount=1
                        #else:
                        move=halb_moves[1]+halb_moves[0]
                        move2=halb_moves[0]+halb_moves[1]

                        halb_moves[1]=halb_moves[0]
                        halb_moves[0]=""

                        if halb_moves[1]!="z" and halb_moves[0] != "z":
                            Move(move, move2)
                        else:
                            print("Halbzug Manuell eingegeben")


        i+=1


def Move(move, move2):
    print()
    print("Zug ist: "+move+", oder: "+move2)
    if senden_ja_nein==1:
        sendMove(move, move2)
    

def sendMove(move, move2):
    print()

    game_id=checkGame()
    resoponse=requests.post("https://lichess.org/api/board/game/"+game_id+"/move/"+move, headers={"Authorization":"Bearer "+meintoken})
    print(resoponse.text)

    resoponse=requests.post("https://lichess.org/api/board/game/"+game_id+"/move/"+move2, headers={"Authorization":"Bearer "+meintoken})
    print(resoponse.text)

def Lichess_response(response):
    print(response)
    #print(type(response))
    #json_response=json.loads(response)
    print()



while True:
    #lesestat=Serial(lesestat)
    Serial()
    
    time.sleep(0.1)