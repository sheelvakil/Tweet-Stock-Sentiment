import tweepy
import re
import yfinance as yf
from textblob import TextBlob
import matplotlib.pyplot as plt
import seaborn
import matplotlib 
matplotlib.axes.Axes.pie 
matplotlib.pyplot.pie

api = tweepy.API(auth)

def cleanTweet(string):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", string).split())

def cleanCompanyName(name):
    index = name.find(" ")
    substring = name[:index] 
    if substring.isalpha():
        return substring
    else:
        regex = re.compile('[^a-zA-Z]')
        substring = regex.sub('', substring)
        return substring

posValues = []
negValues = []
def sentimentAnalysis(string):
    analysis = TextBlob(string)
    sentiment = analysis.sentiment.polarity
    if sentiment > 0:
        posValues.append(sentiment)
    elif sentiment < 0:
        negValues.append(sentiment)

def getSentimentScore(posValues, negValues, totalTweets):   #score developed by percentage of the overall sentiment per total tweet
    overall = 0
    for value in posValues:
        overall = overall + value
    for value in negValues:
        overall = overall + value
    percentSentiment = (overall/totalTweets) * 100
    percentSentiment = round(percentSentiment, 2)
    return percentSentiment

def getPercentChange (opening,closing):
    difference = closing-opening 
    percent = (difference/opening) * 100
    percent = round(percent, 2)
    return percent

def isVolatile(sentimentScore, percentChange):
    if (sentimentScore > 0 and percentChange > 0) or (sentimentScore < 0 and percentChange < 0):
        return "volatile"
    else:
        return "NOT volatile"

def showGraph():
    p = info['Close'].plot(figsize=(16,9))
    p.plot()
    plt.show()

def showChart(pSize, nSize):
    sizes = [pSize, nSize]
    explode = (0, 0.1)  
    labels = ["postitve tweets", "negative tweets"]
    colors = ["green","red"]
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.2f%%', startangle=90)
    ax1.axis('equal') 
    plt.show()

# actual code start 
ticker = input("Enter company ticker: ")
company = yf.Ticker(ticker)
companyName = company.info['longName']
cleanName = cleanCompanyName(companyName)
query = "@" + cleanName 
statusObject = api.search(q=query, lang="en", count=1000)  
totalTweets = len(statusObject)

for tweet in statusObject:     
    clean = cleanTweet(tweet.text)
    sentimentAnalysis(clean)
sentimentScore = getSentimentScore(posValues, negValues, totalTweets)

info = company.history(period="5d")
openingPrice = info['Open'][0]
closingPrice = info['Close'][4]
percent = getPercentChange(openingPrice, closingPrice)

volatility  = isVolatile(sentimentScore, percent)
result = "According to Twitter and Yahoo Finance API data, {}, in the past week, was {} to tweet sentiment."
data = "{}'s stock price in the past week changed by {}%. {}'s twitter sentiment score was {}."
print()
print(result.format(cleanName, volatility))
print()
print(data.format(cleanName, percent, cleanName, sentimentScore))
print()
show = input("Enter 1 to see a line graph of " + companyName + "'s closing prices. Enter anything else to close program.")
if(show == "1"):
    showGraph()
print()
show2 = input("Enter 1 to see a pie chart of the tweet sentiments. Enter anything else to close program.")
if(show2 == "1"):
    showChart(len(posValues), len(negValues))

