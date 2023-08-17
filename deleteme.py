import time, random
import colour
def slowPrint(text, delay=0.03):
    isCode = False
    for letter in text:
        print(letter.replace("~",""), end="", flush=True)
        if(letter != "~" and not isCode):
            time.sleep(random.uniform(1.8/len(text),2/len(text)))
        elif(letter == "~"):
            isCode = not isCode
    print()

def slowInput(text, delay=0.03):
    global isCode
    isCode = False  # Initialize isCode to False
    lettersTyped = ""
    
    for letter in text:
        print(letter.replace("~",""), end="", flush=True)
        if(letter != "~" and not isCode):
            time.sleep(random.uniform(1.8/len(text),2/len(text)))
        elif(letter == "~"):
            isCode = not isCode
        
    return input()

slowPrint(f"{colour.backBlack}{colour.backBlack}{colour.backBlack}{colour.backBlack}What class would you like to play? Paladin / Bonus damage with claymores, Spearsman / Attacks multiple times with spears, Swordsman / Bonus damage and two attacks with shortsword    -    ")