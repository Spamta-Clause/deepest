black = "\033[30m"
red = "\033[31m"
yellow = "\033[33m"
green = "\033[32m"
blue = "\033[34m"
purple = "\033[35m"
white = "\033[37m"
backBlack = "\033[40m"
backRed = "\033[41m"
backYellow = "\033[43m"
backGreen = "\033[42m"
backBlue = "\033[44m"
backPurple = "\033[45m"
backWhite = "\033[47m"
bold = "\033[1m"
italic = "\033[3m"
underlined = "\033[4m"
reset = "\033[0m"
options = [reset,black,red,yellow,green,blue,purple,white]
backOptions = [reset,backBlack,backRed,backYellow,backGreen,backBlue,backPurple,backWhite]
textOptions = [reset,bold,italic,underlined]
def show():
    for textOption in textOptions:
        for backOption in backOptions:
            for option in options:
                order = ""
                back = []
                front = []
                totalOptions = [textOption,backOption,option]
                for totalOption in totalOptions:
                    if(totalOption == reset):
                        back.append(totalOption)
                    else:
                        front.append(totalOption)
                if(len(back) > 0):
                    order += ''.join(back)
                if(len(front) > 0):
                    order += ''.join(front)
                print(f"{order}  hey  {reset}")
    print(f"{bold}{black}{backBlue}These are just some options, you can also combine both italic, bold and underlined{reset}")
def list():
    print(f"Text Colour - {black}black,{red}red,{yellow},yellow,{green}green,{blue}blue,{purple}purple,{white}white{reset}")
    print(f"Background Colour - {backBlack}backBlack,{backRed}backRed,{backYellow},backYellow,{backGreen}backGreen,{backBlue}backBlue,{backPurple}backPurple,{backWhite}backWhite{reset}")
    print(f"Text Options - {bold}bold,{reset}{italic}italic,{reset}{underlined}underlined{reset}")
    print(f"Reset - {bold}{italic}{backRed}{black} Coloured Text, {reset}reset ")