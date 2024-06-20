import random
import RPi.GPIO as GPIO # type: ignore
#import GPIOmock as GPIO
import threading
import time
import random
import os
from subprocess import call
import numpy as np

guessBoard = [["0"] * 3 for i in range(3)] #makes board
guessboard2 = [["0"] * 3 for i in range(3)] 


LIGHTS = [2,3,4,17,27,22,11,5,6,13,19,26,8,7,12,16,20,21]
BUZZER = [18]


myDictGreen = dict([("00", 2), ("10", 4), ("20",27), ("01",11), ("11",6), ("21",19), ("02",8), ("12",12), ("22",20)])
myDictRed = dict([("00", 3), ("10", 17), ("20",22), ("01",5), ("11",13), ("21",26), ("02",7), ("12",16), ("22",21)])



def initialize_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(BUZZER,GPIO.OUT)
    GPIO.output(BUZZER,GPIO.LOW)
    for pin in LIGHTS:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
    

def initBoard():
    global s1
    global s2
    global s3
    global s4
    global s5
    global s6
    global s7
    global s8
    global s9
    global s10
    global s11
    global s12

    print("PLAYER 1")

    s1, s2 = int(input("(First Player) What row do you want for your first ship?")), int(input("(First PLayer) What column do you want for your first ship?"))
    s3, s4 = int(input("(First Player) What row do you want for your second ship?")), int(input("(First Player) What column do you want for your second ship?"))
    s5, s6 = int(input("(First Player) What row do you want for the second part of your second ship?")), int(input("(First Player) What column do you want for the second part of your second ship?"))
    
    if s5 == s3+2 or s5 == s3-2 or s6 == s4+2 or s6== s4-2:
        raise Exception("Sorry your second index must be either vertical or horizontal or diagnol of your first index!")
    
    print("You put your ships at locations: ", "(", s1, ",", s2, "), (", s3, ", ", s4, "), (", s5, ", ", s6, ")")
    
    print("---------------------------------------------------------------")
    print("---------------------------------------------------------------")
    print("---------------------------------------------------------------")
    print("---------------------------------------------------------------")
    print("---------------------------------------------------------------")
    print("---------------------------------------------------------------")
    print("---------------------------------------------------------------")
    print("---------------------------------------------------------------")
    print("---------------------------------------------------------------")
    print("---------------------------------------------------------------")
    print("---------------------------------------------------------------")
    print("---------------------------------------------------------------")
    print("---------------------------------------------------------------")
    print("---------------------------------------------------------------")
    print("---------------------------------------------------------------")
    print("---------------------------------------------------------------")

    print("PLAYER 2")


    s7, s8 = int(input("(Second PLayer) What row do you want for your first ship?")), int(input("(Second Player) What column do you want for your first ship?"))
    s9, s10 = int(input("(Second PLayer) What row do you want for your second ship?")), int(input("(Second Player) What column do you want for your second ship?"))
    s11, s12 = int(input("(Second PLayer) What row do you want for the second part of your second ship?")), int(input("(Second Player) What column do you want for the second part of your second ship?"))
    if s11 == s9+2 or s11 == s9-2 or s12 == s10+2 or s12== s10-2:
        raise Exception("Sorry your second index must be either vertical or horizontal or diagnol of your first index!")
    
    print("You put your ships at locations: ", "(", s7, ",", s8, "), (", s9, ", ", s10, "), (", s11, ", ", s12, ")")


    global user1Ship 
    user1Ship = []
    global user1Ship2 
    user1Ship2= []
    global user1Ship3
    user1Ship3 = []
    user1Ship.append(s1)
    user1Ship.append(s2)
    user1Ship2.append(s3)
    user1Ship2.append(s4)
    user1Ship3.append(s5)
    user1Ship3.append(s6)

   


    global user2Ship 
    user2Ship = []
    global user2Ship2 
    user2Ship2 = []
    global user2Ship3
    user2Ship3 = []
    user2Ship.append(s7)
    user2Ship.append(s8)
    user2Ship2.append(s9)
    user2Ship2.append(s10)
    user2Ship3.append(s11)
    user2Ship3.append(s12)

    



def printBoard():
    for row in guessBoard:
        for cell in row:
            if cell == "0" or cell == "-":
                print("0", end=" ")
            else:
                print(cell, end=" ")
        print()

def printBoard2():
    for row in guessboard2:
        for cell in row:
            if cell == "0" or cell == "-":
                print("0", end=" ")
            else:
                print(cell, end=" ")
        print()

def hitOrMiss():
        global user1Ships

        print("--------------------------------")
        print("User 2's turn!")
        GPIO.output(18, GPIO.HIGH)
        time.sleep(.4)
        GPIO.output(18, GPIO.LOW)
        time.sleep(.2)
        GPIO.output(18, GPIO.HIGH)
        time.sleep(.4)
        GPIO.output(18, GPIO.LOW)
        time.sleep(.5)
        row = int(input("You must enter a row number between 1-{} >: ".format(3)))
        column = int(input("You must enter a column number between 1-{} >: ".format(3)))

        print("You guessed row: {} col: {}".format(row, column))
                
        #ensures the user cannot type outisde of the bounds of the grid
        if row not in range(1,3+1) or column not in range(1, 3+1):
            print("\nThe numbers must be between 1-{}!".format(3))

        choice = [row,column]

        row = row-1
        column = column-1

        #checks to see if you shot a spot already  
        if guessBoard[row][column] == "-" or guessBoard[row][column] == "X":
            print("\nYou have already shot that spot!\n")
           
            
        #compares the list of computer ships and checks to see if choice list matches any of them
        elif choice == user1Ship or choice == user1Ship2 or choice == user1Ship3:
            print("\nBoom! You hit a ship! \n")
            guessBoard[row][column] = "X"
            if choice == user1Ship:
                user1Ship.clear()
            elif choice == user1Ship2:
                 user1Ship2.clear()
            elif choice == user1Ship3:
                 user1Ship3.clear()

        

            str1 = str(row)+str(column)
            GPIO.output(myDictRed[str1], GPIO.HIGH)
            time.sleep(3)
            GPIO.output(myDictRed[str1], GPIO.LOW)

        else:
            print("\nYou missed!\n")
            guessBoard[row][column] = "-"
            
            str2 = str(row)+str(column)

            GPIO.output(myDictGreen[str2], GPIO.HIGH)
            time.sleep(1)
            GPIO.output(myDictGreen[str2], GPIO.LOW)

        if user1Ship == []:
            print("You sunk the small ship!")
            user1Ship.append(s1-1)
            user1Ship.append(s2-1)
            str2 = str(s1-1)+str(s2-1)
            GPIO.output(myDictGreen[str2], GPIO.HIGH)
            GPIO.output(myDictRed[str2], GPIO.HIGH)
            GPIO.output(18, GPIO.HIGH)
            time.sleep(3)
            GPIO.output(myDictGreen[str2], GPIO.LOW)
            GPIO.output(myDictRed[str2], GPIO.LOW)
            GPIO.output(18, GPIO.LOW)
            time.sleep(.3)
            user1Ships = user1Ships-1


        
        if user1Ship2 == [] and user1Ship3 == []:
            print("You sunk the large ship!")
            user1Ship2.append(s3-1)
            user1Ship2.append(s4-1)
            user1Ship3.append(s5-1)
            user1Ship3.append(s6-1)
            str3 = str(s3-1)+str(s4-1)
            str4 = str(s5-1)+str(s6-1)
            GPIO.output(myDictGreen[str3], GPIO.HIGH)
            GPIO.output(myDictRed[str3], GPIO.HIGH)
            GPIO.output(myDictGreen[str4], GPIO.HIGH)
            GPIO.output(myDictRed[str4], GPIO.HIGH)
            GPIO.output(18, GPIO.HIGH)
            time.sleep(3)
            GPIO.output(myDictGreen[str3], GPIO.LOW)
            GPIO.output(myDictRed[str3], GPIO.LOW)
            GPIO.output(myDictGreen[str4], GPIO.LOW)
            GPIO.output(myDictRed[str4], GPIO.LOW)
            GPIO.output(18, GPIO.LOW)
            time.sleep(.3)
            user1Ships = user1Ships-1

        if user1Ships == 0:
            print("----------------------------")
            print("You sunk the all the ships!")
            print("Congrats, User 2 Won!")

       

def hitOrMiss2():
        global user2Ships
        print("--------------------------------")
        print("User 1's Turn!")
        GPIO.output(18, GPIO.HIGH)
        time.sleep(.3)
        GPIO.output(18, GPIO.LOW)
        time.sleep(.5)
        row2 = int(input("You must enter a row number between 1-{} >: ".format(3)))
        column2 = int(input("You must enter a column number between 1-{} >: ".format(3)))

        print("You guessed row: {} col: {}".format(row2, column2))
                
        #ensures the user cannot type outisde of the bounds of the grid
        if row2 not in range(1,3+1) or column2 not in range(1, 3+1):
            print("\nThe numbers must be between 1-{}!".format(3))

        choice = [row2,column2]

        row2 = row2-1
        column2 = column2-1
                
        #checks to see if you shot a spot already  
        if guessboard2[row2][column2] == "-" or guessboard2[row2][column2] == "X":
            print("\nYou have already shot that spot!\n")
           
            
        #compares the list of computer ships and checks to see if choice list matches any of them
        elif choice == user2Ship or choice == user2Ship2 or choice == user2Ship3:
            print("\nBoom! You hit a ship! \n")
            guessboard2[row2][column2] = "X"
            if choice == user2Ship:
                user2Ship.clear()
            elif choice == user2Ship2:
                 user2Ship2.clear()
            elif choice == user2Ship3:
                 user2Ship3.clear()

        

            str5 = str(row2)+str(column2)
            GPIO.output(myDictRed[str5], GPIO.HIGH)
            time.sleep(3)
            GPIO.output(myDictRed[str5], GPIO.LOW)

        

        else:
            print("\nYou missed!\n")
            guessboard2[row2][column2] = "-"
            
            str6 = str(row2)+str(column2)

            GPIO.output(myDictGreen[str6], GPIO.HIGH)
            time.sleep(1)
            GPIO.output(myDictGreen[str6], GPIO.LOW)

            
        if user2Ship == []:
            print("You sunk the small ship!")
            user2Ship.append(s7-1)
            user2Ship.append(s8-1)
            str7 = str(s7-1)+str(s8-1)
            GPIO.output(myDictGreen[str7], GPIO.HIGH)
            GPIO.output(myDictRed[str7], GPIO.HIGH)
            GPIO.output(18, GPIO.HIGH)
            time.sleep(3)
            GPIO.output(myDictGreen[str7], GPIO.LOW)
            GPIO.output(myDictRed[str7], GPIO.LOW)
            GPIO.output(18, GPIO.LOW)
            time.sleep(.3)
            user2Ships = user2Ships - 1
            


        
        if user2Ship2 == [] and user2Ship3 == []:
            print("You sunk the large ship!")
            user2Ship2.append(s9-1)
            user2Ship2.append(s10-1)
            user2Ship3.append(s11-1)
            user2Ship3.append(s12-1)
            str8 = str(s9-1)+str(s10-1)
            str9 = str(s11-1)+str(s12-1)
            GPIO.output(myDictGreen[str8], GPIO.HIGH)
            GPIO.output(myDictRed[str8], GPIO.HIGH)
            GPIO.output(myDictGreen[str9], GPIO.HIGH)
            GPIO.output(myDictRed[str9], GPIO.HIGH)
            GPIO.output(18, GPIO.HIGH)
            time.sleep(3)
            GPIO.output(myDictGreen[str8], GPIO.LOW)
            GPIO.output(myDictRed[str8], GPIO.LOW)
            GPIO.output(myDictGreen[str9], GPIO.LOW)
            GPIO.output(myDictRed[str9], GPIO.LOW)
            GPIO.output(18, GPIO.LOW)
            time.sleep(.3)
            user2Ships = user2Ships - 1
            

       
        if user2Ships == 0:
            print("----------------------------")
            print("You sunk the all the ships!")
            print("Congrats, User 2 Won!")

            



                    
def main():
    global user1Ships
    user1Ships = 2
    global user2Ships
    user2Ships = 2
    initialize_gpio()
    print("Welcome to Battleship!")
    initBoard()
    printBoard()
    while user1Ships != 0 and user2Ships != 0:
         hitOrMiss2()
         if user2Ships ==0:
             break
         hitOrMiss()
         if user1Ships ==0:
             break
    
    print("------------------")
    print("Goodbye!")
    exit()


main()