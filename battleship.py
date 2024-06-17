import random
import RPi.GPIO as GPIO # type: ignore
#import GPIOmock as GPIO
import threading
import time
import random
import os
from subprocess import call

guessBoard = [["0"] * 3 for i in range(3)] #makes board

LIGHTS = [2,3,4,17,27,22,11,5,6,13,19,26,8,7,12,16,20,21]


myDictGreen = dict([({1,1}, 2), ({1,2}, 4), ({1,3},27), ({2,1},11), ({2,2},6), ({2,3},19), ({3,1},8), ({3,2},12), ({3,3},20)])
myDictRed = dict([({1,1}, 3), ({1,2}, 17), ({1,3},22), ({2,1},5), ({2,2},13), ({2,3},26), ({3,1},7), ({3,2},16), ({3,3},21)])


ships = 2


def initialize_gpio():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LIGHTS, GPIO.OUT, initial=GPIO.LOW)
    

def initBoard():
    user1, user2 = input("What row do you want for your first ship?"), input("What column do you want for your first ship?")
    user3, user4 = input("What row do you want for your second ship?"), input("What column do you want for your second ship?")
    guessBoard[user1][user2] = "s"
    guessBoard[user3][user4] = "s"

    printBoard()

    
def printBoard():
    for row in guessBoard:
        for cell in row:
            if cell == "0" or cell == "-" or cell == "s":
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
            
        row = row - 1 # Reducing number to desired index.
        column = column - 1 # Reducing number to desired index.
                
                
        #checks to see if you shot a spot already  
        if guessBoard[row][column] == "-" or guessBoard[row][column] == "X":
            print("\nYou have already shot that spot!\n")
        #compares the list of computer ships and checks to see if choice list matches any of them
        elif guessBoard[row][column] == "s":
            print("\nBoom! You hit a ship! \n")
            GPIO.output(myDictRed[{row,column}], GPIO.HIGH)

            guessBoard[row][column] = "X"

        if ships == 0:
                        print("You sunk the all the ships!")
                        print("Congrats, you won! (USER WON)")

        else:
            print("\nYou missed!\n")
            guessBoard[row][column] = "-"
            GPIO.output(myDictRed[{row,column},GPIO.HIGH])
                    
