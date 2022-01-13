import requests
from bs4 import BeautifulSoup
import codecs

base_url = "https://tailwindcss.tw/"

r = requests.get(base_url + "/docs/")
soup = BeautifulSoup(r.text,"html.parser")

pageList = [
  "/docs/installation/using-postcss",
  "/docs/installation/framework-guides",
  "/docs/installation/play-cdn",
  "/docs/guides/nextjs",
  "/docs/guides/laravel",
  "/docs/guides/vite",
  "/docs/guides/nuxtjs",
  "/docs/guides/gatsby",
  "/docs/guides/create-react-app",
]
pageListSelector = soup.select("nav li a")
for p in pageListSelector:
  link = p["href"]

  if link.index("/")==0:
    # print(p["href"])
    pageList.append(p["href"])


# ======================================
wordList = []

for link in pageList:
  r = requests.get(base_url + link)
  soup = BeautifulSoup(r.text,"html.parser")
  sel = soup.select("div#content p")

  print("[PROCCESSING] " + link)

  for s in sel:
    wordList = wordList + str(s.text).split()

clearWordList = []

for w in sorted(list(set(wordList))):
  word = (str(w)
          .replace(":","")
          .replace(",","")
          .replace("<","\\<")
          .replace(">","\\>")
          .replace("`","\\`")
          .replace("|","\\|"))
  
  if "." in word and word.index(".")==len(word)-1:
    word = word[:-1]
      
  clearWordList.append(word)

readMe = "## Word List\n\n"
readMe = readMe + "| 原文 | 中文 |\n"
readMe = readMe + "|------|-----|\n"

for w in sorted(list(set(clearWordList))):
  readMe = readMe + "| " + w + " | |\n"

f = codecs.open("readme.md", "w", "utf-8")
f.write(readMe)
f.close()
