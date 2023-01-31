import requests
from bs4 import BeautifulSoup, SoupStrainer
import html5lib
import matplotlib.pyplot as plt

def parseSite(link):
    html_text = requests.get(link, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}).text
    result = requests.get(link, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}).text
    doc = BeautifulSoup(result, "html.parser")
    return doc


def search(user, region):
    try:
        link = f"https://www.op.gg/summoners/{region}/{user}"
        doc = parseSite(link)
        
        rank = (doc.find(class_="tier").text).title()
        lp = doc.find(class_="lp").text
        winrate = doc.find(class_="ratio").text
        winloss = doc.find(class_="win-lose").text

        return [rank, lp, winrate, winloss]
    
    except:
        return "this user aint ranked yet."

def stats(user, region):
    try:
        link = f"https://championmastery.gg/summoner?summoner={user}&region={region}"
        doc = parseSite(link)
        topFiveMastery = (doc.select("tr > td")[:3], doc.select("tr > td")[7:10], doc.select("tr > td")[14:17], doc.select("tr > td")[21:24], doc.select("tr > td")[28:31])
        labels = [topFiveMastery[0][0].text, topFiveMastery[1][0].text, topFiveMastery[2][0].text, topFiveMastery[3][0].text, topFiveMastery[4][0].text]
        sizes = list(map(int, [topFiveMastery[0][2].text, topFiveMastery[1][2].text, topFiveMastery[2][2].text, topFiveMastery[3][2].text, topFiveMastery[4][2].text]))
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')
        ax1.set_title("Chamption Mastery for top 5 champs")
        plt.show()
    except:
        return "this user aint found."
