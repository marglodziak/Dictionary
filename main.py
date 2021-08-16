import time
import os
import tkinter as tk
import tkinter.font as font


def change(number):
    if number == '-' or number == '+' or number == ',':
        button3_1["state"] = tk.DISABLED
        button6_1["state"] = tk.DISABLED
        button_comma["state"] = tk.DISABLED
        button1["state"] = tk.NORMAL
        button2["state"] = tk.NORMAL
        button3["state"] = tk.NORMAL
        button4["state"] = tk.NORMAL


# inicjalizacja, fullscreen
root = tk.Tk()
root.title("Słownik")
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.geometry("%dx%d" % (width, height))

# czcionki
entryFont = font.Font(size=30)
welcomeFont = font.Font(size=25)
mainFont = font.Font(size=16)

# ramki
frameMain = tk.Frame(root)
frameAddWord = tk.Frame(root)
frameRandomWord = tk.Frame(root)
frameTestYourself = tk.Frame(root)


# ------------- FUNKCJE -------------

# funkcja chowająca i pokazująca ramki z oknami
def showAndHideFrames(frameToShow, frameToHide=frameMain):
    frameToHide.grid_remove()
    frameToShow.grid()


# funkcja dodająca słowo do słownika
def addWord():

    def sortDict():
        f = open("slownik", "r")
        lines = f.readlines()
        f.close()
        f = open("slownik", "w")
        f.write("")
        f.close()
        g = open("slownik", "a")
        lines.sort()
        for line in lines:
            g.write(line)
        g.close()

    # funkcja zapisująca słowo do pliku słownik i czyszcząca entries
    def save():
        slowo = enterWordInPolish.get()
        tlumaczenie = enterWordInSpanish.get()
        f = open("slownik", "a")
        f.write(slowo + ":" + tlumaczenie + "\n")
        f.close()
        sortDict()

        enterWordInPolish.delete(0, tk.END)
        enterWordInSpanish.delete(0, tk.END)

    # schowanie startowej ramki, pokazanie właściwej
    showAndHideFrames(frameAddWord)

    # wprowadzenie słowa i tłumaczenia
    enterWordInPolish = tk.Entry(frameAddWord, width=14, borderwidth=1, font=entryFont, justify="center")
    enterWordInSpanish = tk.Entry(frameAddWord, width=14, borderwidth=1, font=entryFont, justify="center")
    addWordButton = tk.Button(frameAddWord, text="Dodaj słowo", command=save)
    goBack = tk.Button(frameAddWord, text="Powrót", command=lambda: showAndHideFrames(frameMain, frameAddWord))

    # układ elementów
    enterWordInPolish.grid(row=1, column=0, padx=(60, 0), pady=(0, 30), ipady=20)
    enterWordInSpanish.grid(row=1, column=1, padx=60, pady=(0, 30), ipady=20)
    addWordButton.grid(row=2, column=1, pady=(0, 40), sticky="e", padx=(0, 60))
    goBack.grid(row=2, column=0, pady=(0, 40), sticky="w", padx=(60, 0))


def getRandomWord():
    # schowanie startowej ramki, pokazanie właściwej
    showAndHideFrames(frameRandomWord)

    # wczytanie pliku
    f = open("slownik", "r")
    wholeFile = f.readlines()
    f.close()

    chosenWord = tk.Label(frameRandomWord, text="", font=mainFont)

    def chooseWord():
        # wybranie losowej linii, podział po ':'
        chosenLineNumber = int(time.time()) % len(wholeFile)
        chosenLine = wholeFile[chosenLineNumber].split(":")

        # wypisanie słowa i przycisk 'Powrót'
        chosenWord['text'] = chosenLine[0] + " - " + chosenLine[1]

        # ułożenie elementów

    getAnotherWord = tk.Button(frameRandomWord, text="Wylosuj słowo", font=mainFont, pady=10, command=chooseWord)
    goBack = tk.Button(frameRandomWord, text="Powrót", font=mainFont, pady=10,
                       command=lambda: [showAndHideFrames(frameMain, frameRandomWord), chosenWord.destroy()])
    chosenWord.grid(row=0, column=0, columnspan=2)
    goBack.grid(row=1, column=0, pady=40, padx=20)
    getAnotherWord.grid(row=1, column=1, pady=40, padx=20)
    chooseWord()


def sprawdz():
    def checking(tlu):
        slow = entryCheck.get()
        checkWord['text'] = "Losuj ponownie"
        checkWord['command'] = chooseWord
        if slow == tlu:
            getLabel2['text'] += "poprawnie"

        else:
            getLabel2['text'] += "błąd"

    showAndHideFrames(frameTestYourself)
    getLabel = tk.Label(frameTestYourself, text="", font=mainFont)
    getLabel2 = tk.Label(frameTestYourself, text="Ocena: ", font=mainFont)
    entryCheck = tk.Entry(frameTestYourself, width=14, borderwidth=1, font=entryFont, justify="center")
    checkWord = tk.Button(frameTestYourself, text="", font=mainFont, command="")

    f = open("slownik", "r")
    wholeFile = f.readlines()

    def chooseWord():
        entryCheck.delete(0, tk.END)
        getLabel2['text'] = "Ocena: "
        checkWord['text'] = "Sprawdź!"
        y = int(time.time()) % len(wholeFile)
        chosenLine = wholeFile[y].split(':')
        slowo = chosenLine[0]
        tlumaczenie = chosenLine[1][:-1]
        getLabel['text'] = slowo
        checkWord['command'] = lambda: checking(tlumaczenie)

    getLabel.grid(row=0, column=0, columnspan=2, pady=40)
    getLabel2.grid(row=2, column=0, columnspan=2, pady=40)
    entryCheck.grid(row=1, column=0, columnspan=2)
    checkWord.grid(row=3, column=1, sticky="e")

    goBackShow = tk.Button(frameTestYourself, text="Powrót", font=mainFont,
                           command=lambda: [showAndHideFrames(frameMain, frameTestYourself), getLabel.destroy(), getLabel2.destroy()])
    goBackShow.grid(row=3, column=0, sticky="w")
    chooseWord()
    f.close()


def show():
    # utwórz nową ramkę, na wypadek zmiany liczby słów (przykrywanie starego tekstu), pokaż ją; przycisk 'Powrót'
    frameShowDictionary = tk.Frame(root)
    showAndHideFrames(frameShowDictionary)

    # otwarcie pliku 'slownik', wypisanie po linii
    if not os.path.isfile("slownik"):
        tk.Label(frameShowDictionary, text="Brak wpisów w słowniku.").grid(row=0)
        goBackDict = tk.Button(frameShowDictionary, text="Powrót",
                               command=lambda: [showAndHideFrames(frameMain), frameShowDictionary.destroy()])
        goBackDict.grid(row=1)
        return
    f = open("slownik", "r")

    _row, page = 0, 0
    frames = []
    flag = 1
    while flag:
        frames.append(tk.Frame(frameShowDictionary))
        frames[-1].grid_remove()
        while _row < 10:
            line = f.readline()
            wyrazy = line.split(":")
            if line:
                tk.Label(frames[-1], text=wyrazy[0] + " - " + wyrazy[1], font=mainFont).grid(row=_row, column=0, padx=20)
                _row += 1
            else:
                flag = 0
                break

        _row = 0
        page += 1

    frames[0].grid()

    buttonFrame = tk.Frame(frameShowDictionary)
    goBackDict = tk.Button(buttonFrame, text="Powrót",
                           command=lambda: [showAndHideFrames(frameMain), frameShowDictionary.destroy()])

    buttonFrame.grid()
    buttons = []

    def changeFrame(index):

        for frame in frames:
            frame.grid_remove()

        buttonFrame.grid_remove()
        frames[index].grid()
        buttonFrame.grid()

    goBackDict.grid(row=12, column=0, columnspan=5)
    for i in range(len(frames)):
        buttons.append(tk.Button(buttonFrame, text=i+1))
        buttons[-1].grid(row=11, column=i)
    for i in range(len(buttons)):
        buttons[i]['command'] = lambda i=i:changeFrame(i)


# TODO przycisk sprawdź się wewnątrz sprawdź się
# TODO kolory

# ------------- EKRAN GŁÓWNY -------------


# ekran główny, elementy
frameMain.grid(row=0, column=0, columnspan=3, sticky='')
welcomeText = tk.Label(frameMain, text="Witaj w słowniku.\n\n"
                                       "Wybierz z poniższych opcji, co chcesz zrobić:", font=welcomeFont)
addWords = tk.Button(frameMain, text="Dodaj słowo", font=welcomeFont, pady=10, command=addWord)
getWord = tk.Button(frameMain, text="Wylosuj słowo", font=welcomeFont, pady=10, command=getRandomWord)
showDict = tk.Button(frameMain, text="Wyświetl słownik", font=welcomeFont, pady=10, command=show)
check = tk.Button(frameMain, text="Sprawdź się!", font=welcomeFont, pady=10, command=sprawdz)
close = tk.Button(frameMain, text="Wyjdź", font=welcomeFont, pady=10, command=root.destroy)

# ekran główny, ułożenie elementów
welcomeText.grid(row=0, column=0, columnspan=4, sticky="")
addWords.grid(row=1, column=0, padx=40)
getWord.grid(row=1, column=1, padx=(0, 40), pady=80)
showDict.grid(row=1, column=2, padx=(0, 40))
check.grid(row=2, column=0)
close.grid(row=2, column=2)


def zamiana():
    button1 = tk.Button(root, text="a", fg="#875c00", bg="#ffff9c", activeforeground="#875c00",
                        activebackground="#ffffcf", padx="51", pady="20", font=myFont,
                        command=lambda: change('a')).grid(row=5, column=0)
    button2 = tk.Button(root, text="b", fg="#875c00", bg="#ffff9c", activeforeground="#875c00",
                        activebackground="#ffffcf", padx="50", pady="20", font=myFont,
                        command=lambda: change('b')).grid(row=5, column=1)
    button3 = tk.Button(root, text="c", fg="#875c00", bg="#ffff9c", activeforeground="#875c00",
                        activebackground="#ffffcf", padx="50", pady="20", font=myFont,
                        command=lambda: change('c')).grid(row=5, column=2)
    button3_1 = tk.Button(root, text="-", fg="#875c00", bg="#e6d047", activeforeground="#431800",
                          activebackground="#f7e158", padx="52", pady="20", font=myFont,
                          command=lambda: change('-')).grid(row=5, column=3)
    button4 = tk.Button(root, text="d", fg="#875c00", bg="#ffff9c", activeforeground="#875c00",
                        activebackground="#ffffcf", padx="50", pady="20", font=myFont,
                        command=lambda: change('d')).grid(row=6, column=0)
    button5 = tk.Button(root, text="e", fg="#875c00", bg="#ffff9c", activeforeground="#875c00",
                        activebackground="#ffffcf", padx="50", pady="20", font=myFont,
                        command=lambda: change('e')).grid(row=6, column=1)
    button6 = tk.Button(root, text="f", fg="#875c00", bg="#ffff9c", activeforeground="#875c00",
                        activebackground="#ffffcf", padx="52", pady="20", font=myFont,
                        command=lambda: change('f')).grid(row=6, column=2)
    button6_1 = tk.Button(root, text="+", fg="#875c00", bg="#e6d047", activeforeground="#431800",
                          activebackground="#f7e158", padx="47", pady="20", font=myFont,
                          command=lambda: change('+')).grid(row=6, column=3)
    button7 = tk.Button(root, text="g", fg="#875c00", bg="#ffff9c", activeforeground="#875c00",
                        activebackground="#ffffcf", padx="50", pady="20", font=myFont,
                        command=lambda: change('g')).grid(row=7, column=0)
    button8 = tk.Button(root, text="h", fg="#875c00", bg="#ffff9c", activeforeground="#875c00",
                        activebackground="#ffffcf", padx="50", pady="20", font=myFont,
                        command=lambda: change('h')).grid(row=7, column=1)
    button9 = tk.Button(root, text="i", fg="#875c00", bg="#ffff9c", activeforeground="#875c00",
                        activebackground="#ffffcf", padx="53", pady="20", font=myFont,
                        command=lambda: change('i')).grid(row=7, column=2)
    button9_1 = tk.Button(root, text="=", fg="#875c00", bg="#e6d047", activeforeground="#431800",
                          activebackground="#f7e158", padx="47", pady="58", font=myFont,
                          command=lambda: change('=')).grid(row=7, rowspan=2, column=3)
    button0 = tk.Button(root, text="0", fg="#875c00", bg="#ffff9c", activeforeground="#875c00",
                        activebackground="#ffffcf", padx="110", pady="20", font=myFont, command=lambda: change(0)).grid(
        row=8, columnspan=2)
    button_var = tk.Button(root, text="cyfry", fg="#ffed7a", bg="#a16d00", activeforeground="#431800",
                           activebackground="#e49f33", padx="32", pady="10", font=myFont, command=main).grid(row=3,
                                                                                                             column=2,
                                                                                                             columnspan=2)


# button0=tk.Button(root, state=tk.NORMAL, text="0", fg="#875c00", bg="#ffff9c", activeforeground="#875c00", activebackground="#ffffcf", padx="110", pady="20", font=myFont, command=lambda: change(0))
# button_comma=tk.Button(root, state=tk.DISABLED, text=",", fg="#875c00", bg="#ffff9c", activeforeground="#875c00", activebackground="#ffffcf", padx="53", pady="20", font=myFont, command=lambda: change(','))
# button_clear=tk.Button(root, text="Kasuj", fg="#875c00", bg="#e6d047", activeforeground="#ffed7a", activebackground="#bf1717", padx="27", pady="10", font=myFont, command=clear)


# button0.grid(row=8,columnspan=2)
# button_comma.grid(row=8,column=2)
# button_clear.grid(row=4,column=0)
# root.geometry("600x200")


root.mainloop()
