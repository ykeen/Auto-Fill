from itertools import islice, tee
import os
import operator
from tkinter import *

root = Tk()
root.title('Auto fill')
root.geometry("500x300")

# Read data from txt files and store them in file_content
unwanted_chars = [';', ':', '!', "*", ".", "»", "-", "،"]
file_content = ""
directory = "Sports/"
printedList = []
inputTxt = ""
for file in os.listdir(directory):
    if file.endswith(".txt"):
        with open(os.path.join(directory, file), encoding="utf8") as fd:
            file_content += fd.read()
file_content = ''.join(i for i in file_content if not i in unwanted_chars)


# Prepare tokens
# We use trigram
N = 3
tokens = list(zip(*(islice(seq, index, None) for index, seq in enumerate(tee(file_content.split(), N)))))



# GUI
# Updating the list box
def update(data):
    # clear the list box
    my_List.delete(0, END)
    # add new words to the listbox
    for item in data:
        my_List.insert(END, item)


# Updating entry box with listbox clicked
def fillout(event):
    my_Entry.delete(0, END)
    my_Entry.insert(END, my_List.get(ANCHOR))


# Creating function to check entry vs listbox
def check(event):
    # grab what was typed
    inputTxt = my_Entry.get()
    count = 0
    twoWords = inputTxt.split()
    nextDic = {}
    nextProb = {}
    sortedNextProb = {}
    txtCounter = 0

    # Get txt count
    if len(twoWords) == 1:
        for i in range(len(tokens) - 1):
            for j in range(len(tokens[i]) - 1):
                if tokens[i][j] == twoWords[0]:
                    txtCounter += 1
    else:
        for i in range(len(tokens) - 1):
            for j in range(len(tokens[i]) - 1):
                if tokens[i][j] == twoWords[0] and tokens[i][j + 1] == twoWords[1]:
                    txtCounter += 1


    # Get predicted word and its count
    for i in range(len(tokens) - 1):
        for j in range(len(tokens[i]) - 1):
            if tokens[i][j] == twoWords[0]:
                if len(twoWords) == 1:
                    nextDic[tokens[i][0] + " " + tokens[i][1] + " " + tokens[i][2]] = 0
                else:
                    if tokens[i][j + 1] == twoWords[1]:
                        nextDic[tokens[i][2]] = 0
                        print("hi")

    for i in range(len(tokens) - 1):
        for j in range(len(tokens[i]) - 1):
            if tokens[i][j] == twoWords[0]:
                if len(twoWords) == 1:
                    tempValue = nextDic.get(tokens[i][0] + " " + tokens[i][1] + " " + tokens[i][2])
                    nextDic[tokens[i][0] + " " + tokens[i][1] + " " + tokens[i][2]] = tempValue + 1

                else:
                    if tokens[i][j + 1] == twoWords[1]:
                        tempValue = nextDic.get(tokens[i][2])
                        nextDic[tokens[i][2]] = tempValue + 1
    # Get Probability
    for word in nextDic:
        nextProb[word] = nextDic.get(word) / txtCounter

    # sort list to print the first 5-elements
    sortedNextProb = sorted(nextProb.items(), key=operator.itemgetter(1), reverse=True)
    for index in range(min(5, len(sortedNextProb))):
        printedList.append(sortedNextProb[index][0])
    update(printedList)


# Creating a label
my_label = Label(root, text="search", font=("Helvetica", 14), fg="grey")
my_label.pack(pady=20)

# Create an entry box
my_Entry = Entry(root)
my_Entry.pack()

# Create a list box
my_List = Listbox(root, width=50)
my_List.pack(pady=40)

# Creating a binding on the entrybox so when typing something a function get called
inputTxt = my_Entry.get()
my_Entry.bind("<Return>", check)

# Create a binding on the listbox onclick
my_List.bind("<<ListboxSelect>>", fillout)

root.mainloop()
