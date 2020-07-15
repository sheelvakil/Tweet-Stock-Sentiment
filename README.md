# Tweet-Stock-Sentiment

Enter a company's stock ticker to determine whether the stock was or was not volatile to Twitter in the past week. 
Twitter API collects a query of tweets related to the company chosen and uses TextBlob to analyze each tweet's sentiment. 
Yahoo Finance API collects stock data, and then the price changes within the past week are calculated.
At the end of the program, based on the user's request, a bar graph of the stock price change within the past week and a pie chart of positive vs. negative tweets are shown. 
