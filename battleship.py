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


LIGHTS = [2,3,4,17,27,22,11,5,6,13,19,26,8,7,12,16,20,21]

set1 = {0,0}
set2 = {0,1}
set3 = {0,2}
set4 = {1,0}
set5 = {1,1}
set6 = {1,2}
set7 = {2,0}
set8 = {2,1}
set9 = {2,2}



f1 = frozenset(set1)
f2 = frozenset(set2)
f3 = frozenset(set3)
f4 = frozenset(set4)
f5 = frozenset(set5)
f6 = frozenset(set6)
f7 = frozenset(set7)
f8 = frozenset(set8)
f9 = frozenset(set9)


myDictGreen = dict([(f1, 2), (f2, 4), (f3,27), (f4,11), (f5,6), (f6,19), (f7,8), (f8,12), (f9,20)])
myDictRed = dict([(f1, 3), (f2, 17), (f3,22), (f4,5), (f5,13), (f6,26), (f7,7), (f8,16), (f9,21)])







ships = 2


def initialize_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    for pin in LIGHTS:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
    

def initBoard():
    user1, user2 = int(input("What row do you want for your first ship?")), int(input("What column do you want for your first ship?"))
    user3, user4 = int(input("What row do you want for your second ship?")), int(input("What column do you want for your second ship?"))
    guessBoard[user1-1][user2-1] = "s"
    guessBoard[user3-1][user4-1] = "s"

    
    
def printBoard():
    for row in guessBoard:
        for cell in row:
            if cell == "0" or cell == "-":
                print("0", end=" ")
            else:
                print(cell, end=" ")
        print()

def hitOrMiss():
    while ships != 0:
        row = int(input("You must enter a row number between 1-{} >: ".format(3)))
        column = int(input("You must enter a column number between 1-{} >: ".format(3)))

        print("You guessed row: {} col: {}".format(row, column))
                
        #ensures the user cannot type outisde of the bounds of the grid
        if row not in range(1,3+1) or column not in range(1, 3+1):
            print("\nThe numbers must be between 1-{}!".format(3))

        row = row-1
        column = column-1
                
                
        #checks to see if you shot a spot already  
        if guessBoard[row][column] == "-" or guessBoard[row][column] == "X":
            print("\nYou have already shot that spot!\n")
        #compares the list of computer ships and checks to see if choice list matches any of them
        elif guessBoard[row][column] == "s":
            print("\nBoom! You hit a ship! \n")
            tempSet1 = {row, column}
            tempF1 = frozenset(tempSet1)
            print(myDictRed[tempF1])
            GPIO.output(myDictRed[tempF1], GPIO.HIGH)
            time.sleep(1)
            GPIO.output(myDictRed[tempF1], GPIO.LOW)

            

        elif ships == 0:
                        print("You sunk the all the ships!")
                        print("Congrats, you won! (USER WON)")

        else:
            print("\nYou missed!\n")
            guessBoard[row][column] = "-"
            tempSet = {row,column}
            tempF = frozenset(tempSet)
            print(myDictGreen[tempF])
            GPIO.output(myDictGreen[tempF], GPIO.HIGH)
            time.sleep(1)
            GPIO.output(myDictGreen[tempF], GPIO.LOW)

                    
def main():
     initialize_gpio()
     print("Welcome to Battleship!")
     initBoard()
     printBoard()
     hitOrMiss()


main()