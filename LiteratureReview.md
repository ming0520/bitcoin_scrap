# Data Scraping on Bitcoin and Media Post

# Todo:

Initialize Git

Scrap Data

Django with mysql

Visualization

# Data Collection Method

## A Complete VADER-Based Sentiment Analysis of Bitcoin (BTC) Tweets during the Era of COVID-19

### Tweepy

custom tweet scraper using Twitter API

collect data for three main reasons manually, online free datasets did not include the COVID-19 pandemic period

All web scrapers were avoided because they might bypass the restrictions of the Twitter API, restrictions were meant to protect Twitter users

### Filtering tweets

filtering tweets by a manually chosen set of keywords:

keywords related to bitcoin (“bitcoin”, “bitcoins”, “Bitcoin”, “Bitcoins”, “BTC”, “XBT”, and “satoshi”) or any hashtags of Bitcoin’s ticker symbols (“#XBT”, “$XBT”, “#BTC”, and “$BTC”) 

### Column

Raw tweet text and their timestamps

### Data Source

**Tweet**

As Twitter truncates tweets over 140 characters, the full-length version of those tweets was also collected by using link at below

[https://developer.twitter.com/en/docs/counting-characters](https://developer.twitter.com/en/docs/counting-characters)

[https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/overview](https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/overview)

**Bitcoin Price**

CryptoCompare API

provide open historical data of opening, high, low, and closing prices and volume (OHLCV) information at a temporal resolution of every minute

Minutely, Bitcoin data were obtained over hourly data to provide enough data points to analyze

71,472 minute of data points was collected from 

hourly prices would have provided nearly 1191 data points

recorded OHLCV data from ([Cryptocompare.com](http://cryptocompare.com/)) seemed to fluctuate when prices were still recent

A bi-daily collection routine was used to replace any recent prices (near the start of the collection period) that matched timestamps with any older prices from the next collection period

### Data Processing

1. each tweet converted into an average polarity score, and tweet polarity volume per minute
2. removal of tweet-specific syntax, splitting text into sentences, and removing stopwords
3. main text cleaning functions labeled “cleaned,” “split,”, and “no sw”
    1. cleaned
        1. removed unwanted characters and words used specifically on
        Twitter’s platform, such as hyperlinks, numbers, and tweet specific syntax, using regular expressions
        2. applied to preserve emojis and possible emoticon characters for use in the VADER sentiment analyzer
        3. ellipsis mark “ . . . ” was removed
        4. truncated to fit within 140 characters
        5. HTML entities such as “&” were converted to UTF-8 equivalent characters, such as “&”
        6. hyperlinks starting with the characters “http” or “www.” were removed
        7. Numbers, along with any symbols, punctuation, or units next to them, were removed
        8. tweet-specific syntax was removed
            1. “@username,” “#hashtag”, start of retweets of the form “RT @username.”
        9. VADER
    2. split
        1. “NLTK split”, “regex split”
    3. no sw
        1. tokenizes text into words and removes any stopwords
        2. whitespace mark our word boundaries, split by Python’s split () function
        3. VADER allows exclamation marks ”!” and question marks ”?”, which affect
        the sentiment score
4. Discussion
    1. strongest correlation comes from processing a day’s worth of data
    2. longer-term trends in correlation were observed when using ten days or 35+ data days
    3. full-length tweet text match closely with the patterns in processing truncated tweet text, reduced preprocessing cost, helps process large datasets or real-time prediction systems such as KryptoOracle
5. Result: 
    1. features from cleaning text of tweet syntax and splitting text into sentences, in combination or separately
    2. VADER score from text preprocessing shows a significant short-term correlation with Bitcoin prices

## Using sentiment analysis to predict interday Bitcoin price movements

Data Source: 

Price data was obtained from the Bitstamp

all dates and times were converted to GMT+0

In practice one would use 252, the average number of trading days on the NASDAQ and NYSE. However, Bitcoin can be traded every day of the year so 365 is used

Raw data obtained from [http://us.spindices.com](http://us.spindices.com/), last accessed: May 6, 2016.

Sharpie Ratio

[What Is a Sharpe Ratio? Understanding Its Use in Investing (investopedia.com)](https://www.investopedia.com/ask/answers/010815/what-good-sharpe-ratio.asp)

Reddit

### Future Enhance

expert media one can predict semi-short term Bitcoin price movements, the market initially overreacts resulting in multiple corrections

not all Bitcoin traders are reading English media

flash crashes or other black swan events that can wipe out all profits

correlate profits to market volatility, the number of transactions, the number of articles published

expert and mainstream media where the former publishes the news first, causing a price movement, and the latter follows, causing a second price movement.

Bitstamp fees vary with your monthly, exchange volume, assume to fall in the tierwith the lowest and the highest fee: 0.10% and 0.25%.

### Filtering:

All incomplete, for example a missing date or headline, articles were removed

Articles that turned out to be irrelevant after all, e.g. the article contains the words virtual and currency but not consecutively, were removed as well

Expert media shows to be a good short-term predictor

duplicate articles were filtered

very similar, e.g. a corrected typo in the body, one of both would be deleted from the set

### Feature

search volumes, social media shares or mentions of Bitcoi

strong correlations between Mt. Gox price data and the daily Wikipedia and weekly Google search volumes

Facebook reshares

Bitcoin client downloads and the number of unique users, proxied using heuristics on the blockchain

Bitcoin exchanges take at least a day to be credit to the trader’s account

Bitstamp closing price, In case no price data is available or Bitstamp
service is suspended, we skip trading those day

### Data Processing

lexicon-based sentiment analysis, combined with Harvard Psychosocial, and finance industry specific dictionary, domain-specific dictionary, point to the Fin-Pos and Fin-Neg word lists

sum of the sentiment scores

Loughran-McDonald dictionary, context-specific lexicon on a sample of 10-Ks

finance-focused lexicon created by Loughran and McDonald

Need to Account: commissions, bid-ask spreads, taxes

Neutral texts tend to fool many sentiment

fifty word minimum and at least five sentiment words, at least three unique sentiment words

Due to our variable term weight, the threshold is more precisely defined as the sum of the absolute values

# Journal Article Review on Sentiment Analysis

## A Complete VADER-Based Sentiment Analysis of Bitcoin (BTC) Tweets during the Era of COVID-19

Author: Toni Pano and Rasha Kashef

**Goal/Purpose:** 

1. develops different text preprocessing strategies for correlating the sentiment scores of Twitter text with Bitcoin prices during the COVID-19 pandemic
2. Valence Aware Dictionary and Sentiment Reasoner (VADER)-based sentiment analysis of BTC tweets during the era of COVID-19 to identify the role of different preprocessing strategies in predicting Bitcoin prices.

**Best Practices:**

1. splitting sentences, removing Twitter-specific tags, or their combination generally improve the correlation of sentiment scores and volume polarity scores with Bitcoin prices
2. recommended using lemmatization, replacing repeated punctuation, replacing contractions, or removing numbers.

**Precaution:** 

1. prices only correlate well with sentiment scores over shorter timespans

**Analysis:** 

1. stock market volatility and policy responses
2. dynamic correlation analysis, Bitcoin could not hedge the US stocks’ extraordinary tail risk

**Prediction:**

1. tested 16 different preprocessing, Multiple Linear Regression (MLR) model to predict a bihourly average price from the number of positive, neutral, and negative tweets accumulated every two hours
2. five most impactful techniques for use in a second, replacing URLs and user mentions, replacing
contractions, replacing repeated punctuation, and lemmatization for a neural network classification model
3. Multi-Layer Perceptron (MLP) efficiency in forecasting the Bitcoin price

**Step:**

1. converting tweet text into a sentiment score that is representative of its emotion