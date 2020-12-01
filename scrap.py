import twitter
import csv
import pandas as pd

if __name__ == "__main__":
    #Secret keys to use the twitter API

    consumer_key='JwBGzHlJImbq65zdSbD2t77SC'
    consumer_secret='HSStuFy7OpXg35GW4N7iobVDkSvevVmMYkAeC9BJQ0Kl4SNVW2'
    access_token_key='1326184476611842050-y74nowqvPo314THVipXtQ5A95DMcHY'
    access_token_secret='L6vUq7co4Pstpfzc45wuCyxy4c34DKqQ3xxahH10lgWAl'

    #First, let's use the twitter API in order to scrap data

    api = twitter.Api(consumer_key=consumer_key,
                      consumer_secret=consumer_secret,
                      access_token_key=access_token_key,
                      access_token_secret=access_token_secret)

    #From the list of US representatives for 2020 we obtain the `Party`, `TwitterUsernames`, `Name`, etc..

    with open('./data/2020 representatives list.csv', newline='', encoding="utf8") as f:
        reader = csv.reader(f)
        data = list(reader)

        Party = []
        TwitterUsernames = []
        Names = []
        State = []
        Chamber = []

        for line in data:
            if line[4] != "":
                TwitterUsernames.append(line[4].replace("@",""))
                Names.append(line[2])
                Chamber.append(line[1])
                State.append(line[0])

                if line[3] == "R":
                    Party.append("Republican")
                else:
                    Party.append("Democrat")

        # Print an example of a Twitter 0Username
        #print(TwitterUsernames[17])

    # checking the size of each our attributes

    #print(len(TwitterUsernames))
    #print(len(Party))
    #print(len(Names))
    #print(len(Chamber))
    #print(len(State))

    # Let's create the DataFrame
    Data = pd.DataFrame()


    # the 1st row is the names of the list
    Party.pop(0), State.pop(0), Chamber.pop(0), Names.pop(0), TwitterUsernames.pop(0)  # drop the index

    Data['Party'] = Party
    Data['Name'] = Names
    Data['State'] = State
    Data['Chamber'] = Chamber
    Data['TwitterUsernames'] = TwitterUsernames

    #print(Datahead())

    Timelines1 = []
    for name in TwitterUsernames[0:100]:
        Timelines1.append(api.GetUserTimeline(screen_name=name, count=200))  # 200 tweets

    Timelines2 = []
    for name in TwitterUsernames[100:200]:
        Timelines2.append(api.GetUserTimeline(screen_name=name, count=200))

    Timelines3 = []
    for name in TwitterUsernames[200:300]:
        Timelines3.append(api.GetUserTimeline(screen_name=name, count=200))

    Timelines4 = []
    for name in TwitterUsernames[300:400]:
        Timelines4.append(api.GetUserTimeline(screen_name=name, count=200))

    Timelines5 = []
    for name in TwitterUsernames[400:]:
        Timelines5.append(api.GetUserTimeline(screen_name=name, count=200))

    # combining all the timelines together, form on dataset w tweets
    Timelines = []
    Timelines = Timelines1 + Timelines2 + Timelines3 + Timelines4 + Timelines5

    # NO OLD tweets so make a time limit or use the time attribute in the tweet

    # Let's grab all the content of the tweets into the `ListOftxt` list.

    ListOftxt = []

    for timeline in Timelines:
        fullTxt = ''

        for tweet in timeline:
            fullTxt += tweet.text

        ListOftxt.append(fullTxt)

    Data['Tweets'] = ListOftxt

    #print(Data.head(10))

    Data.to_csv(r'./data/Data.csv', index=False)