
from PIL import *
from PIL import Image
import pytesseract
import pytesseract
import pyscreenshot as ImageGrab
import cv2
import time
import string

from DirectKeys import PressKey , ReleaseKey

#*******************************User Settings ****************************************************
XRes = 1600 # This is The resolution of the Monitor This Program using Screen Recogniton
YRes = 900 # Common Resolutions Would be 1600 = X 900 = Y ; 1920 = X 1080 = Y ; 2,560 = X  1,440 = Y
#******************ALL Of These Keys are Using Direct X Scan Codes
# Codes Found Here: http://www.gamespp.com/directx/directInputKeyboardScanCodes.html******
DealerKey = 0xC9 # Page Up The |Key that is Bound to Look At he Dealers Cards
YourKey = 0xD1 # page Down | The key that is bound to look at your cards
StandKey = 0x39 # Space | The Key that you would press to hit Stand
HitKey = 0x1C  # Enter | Default The Key that you would Press to Get Another Card or Hit
DoubleKey = 0x0F # Tab | Default The Key that you would Press to Double Down and Get Another Card
#*******************************End Of User Settings **********************************************

X1 = (15/1600) * XRes
Y1 = (10/900) * YRes
X2 = (300/1600) * XRes
X22 = (180/1600) * XRes
Y2 = (55/900) * YRes
def FlipColor(ImagePath):
    image = cv2.imread(ImagePath)
    image = ~image
    cv2.imwrite(ImagePath,image)
def KeyPress(hexKeyCode):
    PressKey(hexKeyCode)
    time.sleep(.5)
    ReleaseKey(hexKeyCode)

def GetDealerHand():
    print("Getting Dealers Hand")
    # part of the screen
    PressKey(DealerKey)
    im = ImageGrab.grab(bbox=(X1, Y1, X2, Y2))  # X1,Y1,X2,Y2
    im.save("Dealer.jpg")
    time.sleep(2)
    ReleaseKey(DealerKey)
    FlipColor("Dealer.jpg")
    Hand = pytesseract.image_to_string(Image.open('Dealer.jpg'),config = '--psm 7 ')
    print("Extracted: " + Hand)
    s = Hand
    Handvalue = ''.join(i for i in s if i.isdigit())
    return(Handvalue)

def GetPlayerHand():
    print("Getting Players Hand")
    PressKey(YourKey)
    im = ImageGrab.grab(bbox=(X1, Y1, X22, Y2))  # X1,Y1,X2,Y2

    im.save("Player.jpg")
    time.sleep(2)
    ReleaseKey(YourKey)
    FlipColor("Player.jpg")
    Hand = pytesseract.image_to_string(Image.open('Player.jpg'),config = '--psm 7 ')
    print("Extracted: " + Hand)
    s = Hand
    Handvalue = ''.join(i for i in s if i.isdigit())
    return(Handvalue)


def Bet():
    print("Betting Value")
    KeyPress(HitKey)

def Hit():
    print("Hitting on Hand")
    KeyPress(HitKey)

def Stand():
    print("Standing On Hand")
    KeyPress(StandKey)

def Double():
    print("Doubling On Hand")
    KeyPress(DoubleKey)

def CalulateMove(PlayerHand, DealerHand):  # 1 = Hit 0 = Stand 2 = Double
    Playerhand = int(float(PlayerHand))
    Dealerhand = int(float(DealerHand))
    if Playerhand >= 17:
            return(0)
    elif Playerhand <= 8 and Dealerhand == 5 and DealerHand == 6:
        return(2)
    elif Playerhand == 9 and Dealerhand < 7:
        return(2)
    elif Playerhand == 10 and Dealerhand < 10:
        return(2)
    elif Playerhand == 11:
        return(2)
    elif Playerhand < 12:
        return(1)
    elif Playerhand == 12 and 4 =< Dealerhand  =< 6:
        return(0)
    elif 12 =< Playerhand < 17 and 6 < Dealerhand:
        return(1)
    else:
        return(0)

def TypeTest():
    print('down')
    KeyPress(0x11)
def PreformMove():
    time.sleep(4)
    DealerHand = GetDealerHand()
    print(DealerHand)
    time.sleep(2)
    PlayerHand = GetPlayerHand()
    print(PlayerHand)
    if not PlayerHand or not DealerHand:
        print("Dealer Had Black Jack Or Error has Occured Restarting Code")
        time.sleep(30)
        MainCode()
    Move = CalulateMove(PlayerHand,DealerHand)
    if Move ==  1:
        Hit()
    elif Move == 2:
        Double()
    else:
        Stand()
    time.sleep(12)
    PlayerHand = GetPlayerHand()
    if not PlayerHand:
        print("Turn Over")
    else:
        PreformMove()
def MainCode():
    Bet()
    time.sleep(14)
    PreformMove()
    time.sleep(15)
    print("Hand Complete")


if __name__ == '__main__':
    time.sleep(1)
    print('5')
    time.sleep(1)
    print('4')
    time.sleep(1)
    print('3')
    time.sleep(1)
    print('2')
    time.sleep(1)
    print('1')
#    TypeTest()
    for _ in range(50):
        MainCode()
