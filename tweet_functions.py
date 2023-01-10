import pandas as pd
from datetime import datetime, timedelta
from data_pipeline import DataPipeline
import twint
import re

# to install twint, use: 
# pip3 install --user --upgrade git+https://github.com/twintproject/twint.git@origin/master#egg=twint

def cleaner(tweet):
    tweet = re.sub(r'https?://\S+|www\.\S+','', tweet) # remove url
    tweet = re.sub(r'[^A-Za-z0-9 ]+', '', tweet) # remove special chars
    return tweet

def getTweets(search_term, until, since, limit=20):
    """
    Configures Twint and returns a dataframe of tweets for a specific day.
    """
    # Configuring Twint for search
    c = twint.Config()
    # The limit of tweets to retrieve
    c.Limit = limit
    # Search term
    c.Search = search_term
    # Removing retweets
    c.Filter_retweets = True
    # Popular tweets
    c.Popular_tweets = True
    # Verified users only
    c.Verified = True
    # Lowercasing tweets
    c.Lowercase = False
    # English only
    c.Lang = 'en'
    # Tweets until a specified date
    c.Until = until + " 00:00:00"
    # Tweets since a specified date
    c.Since = since + " 00:00:00"
    # Making the results pandas friendly
    c.Pandas = True
    # Stopping print in terminal
    c.Hide_output = True
    # Searching
    twint.run.Search(c)
    # Assigning the DF
    df = twint.storage.panda.Tweets_df
    # Returning an empty DF if no tweets were found
    if len(df)<=0:
        return pd.DataFrame()
    # Formatting the date
    df['date'] = df['date'].apply(lambda x: x.split(" ")[0])
    # Returning with english filter to account for an issue with the twint language filter
    return df[df['language']=='en']
  
  
def tweetByDay(start, end, df, search, limit=20):
    """
    Runs the twint query everyday between the given dates and returns
    the total dataframe. 
    
    Start is the first date in the past.
    
    End is the last date (usually would be current date)
    """
    # Finishing the recursive loop
    if start==end:
        # Removing any potential duplicates
        df = df.drop_duplicates(subset="id")
        print(len(df))
        return df    
    # Appending the new set of tweets for specified window of time
    tweet_df = getTweets(
        search, 
        until=(datetime.strptime(start, "%Y-%m-%d") + timedelta(days=2)).strftime("%Y-%m-%d"), 
        since=start, 
        limit=limit
    )
    # Running the query a few more times in case twint missed some tweets
    run = 0 
    while len(tweet_df)==0 and run<=2:
        # Running query again
        tweet_df = getTweets(
            search, 
            until=(datetime.strptime(start, "%Y-%m-%d") + timedelta(days=2)).strftime("%Y-%m-%d"), 
            since=start, 
            limit=limit
        )
        # Counting how many times it ran
        run += 1
    # Adding the new tweets
    df = df.append(tweet_df, ignore_index=True)
    # Updating the new start date
    new_start = (datetime.strptime(start, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
    # Printing scraping status
    print(f"\t{len(df)} Total Tweets collected as of {new_start}\t")
    # Running the function again
    return tweetByDay(
        start=new_start, 
        end=end, 
        df=df, 
        search=search
    )

if __name__ == '__main__':
    # end date need to be set a day later or else it 
    # doesn't fetch current end date
    dp = DataPipeline()
    # Getting tweets daily
    data = {'headline': [], 'date': []}
    df = tweetByDay(
        start="2023-01-08", 
        end="2023-01-10", 
        df=pd.DataFrame(), 
        search="economy", 
        limit=20
    )
    df.reset_index()
    df['tweet'] = df['tweet'].map(lambda x: cleaner(x))
    for index, tweet in df.iterrows():
        data['headline'].append(tweet['tweet'])
        data['date'].append(tweet['date'])
    df = dp.transform(pd.DataFrame(data))
    print(df)
