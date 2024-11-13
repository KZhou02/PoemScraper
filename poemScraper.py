# IMPORTS
from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib
import os

# FUNCTION DEFs
# scrapes poems' html from urls under https://mypoeticside.com (specifically urls of the poem itself)
def getPoem(url):
    req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"}) 
    con = urllib.request.urlopen( req )
    html = con.read()
    soup = BeautifulSoup(html, features="html.parser")
    
    element = soup.find("div", {"class": "poem-entry"}).find("p", recursive=False)

    text = element.text


    with open("Poems.txt", "a", encoding="utf-8") as my_file:
        my_file.write(text)
        my_file.write("\n\n")

# creates an identical Poems.txt with '<br>' for markdown
def addLineBreaks():
    with open('Poems.txt', 'r') as istr:
        with open('PoemsWithBr.txt', 'w') as ostr:
            for line in istr:
                line = line.rstrip('\n') + '<br>'
                print(line, file=ostr)


# THE MAIN SAUCE

# it's easier to delete and create a new Poems.txt since getPoem() appends to the file
#   else you get multiple copies of all poems under the same Poems.txt file
if os.path.exists("Poems.txt"):
  os.remove("Poems.txt")
else:
  print("The file does not exist")

f = open("Poems.txt", "x")
f.close()

# gets html from poet's page
# REPLACE URL FOR OTHER POETS
url = "https://mypoeticside.com/poets/algernon-charles-swinburne-poems"
req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"}) 
con = urllib.request.urlopen( req )
html = con.read()
soup = BeautifulSoup(html, features="html.parser")

# feeds link to every poem under target artist to getPoem()
element = soup.find("ul", {"id": "sortable"})
for poem in element.children:
    for link in poem:
        a = link.get("href")
        with open("Poems.txt", "a", encoding="utf-8") as my_file:
            my_file.write('**'+link.text+'**\n')
        getPoem("https:" +a)

# create linkbreak version for markdown
addLineBreaks()

# EXECUTION TAKES A WHILE
# MAKE SURE TO RUN THIS SCRIPT UNDER THE FOLDER YOU WANT THE TXT FILES STORED
