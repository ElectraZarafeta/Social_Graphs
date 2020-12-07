import pandas as pd
import regex as re
import networkx as nx
import csv
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from fa2 import ForceAtlas2
import jsonlines
import nltk
from nltk.stem import WordNetLemmatizer 
import string
from nltk.tokenize import word_tokenize
import json
import pandas as pd
nltk.download('stopwords')
lemmatizer = WordNetLemmatizer() #assign the lemmatization function to a variable
pun = string.punctuation #assign to a string all sets of punctuation
stops = nltk.corpus.stopwords.words('english') #assign the list of english stop words (commonly used words)
nltk.download('punkt')
nltk.download('wordnet')


def TFPartisanDf(df):
        tokens=[]
        for tweet in df.Tweets:
            words = word_tokenize(tweet) 
            words = [w.lower() for w in words] 
            words = [word for word in words if not word in pun] 
            words = [word for word in words if word.isalpha()] 
            words = [w for w in words if not w in stops] 
            words = [w for w in words if not len(w) == 1]
            for word in words: #loop through the list of words
                word = lemmatizer.lemmatize(word) #return the lemma of each word
                tokens.append(word)
        return tokens


def Initialization(data):
    df=data
  

    Repdf=df[df['Party']=='Republican']
    Demdf=df[df['Party']=='Democrat']
    RepTokens=TFPartisanDf(Repdf)
    DemTokens=TFPartisanDf(Demdf)
    
    A4=nltk.FreqDist(RepTokens)
    B4=nltk.FreqDist(DemTokens)
    A4=dict(A4)
    B4=dict(B4)
    
    WordCount=pd.DataFrame(columns=['Word','Count'])
    WordCount.astype({'Word':'category'})
    WordCount2=pd.DataFrame(columns=['Word','Count'])
    WordCount2.astype({'Word':'category'})
    
    for word,count in A4.items():
        WordCount.loc[len(WordCount)+1]=(word,count)
    for word,count in B4.items():
        WordCount2.loc[len(WordCount2)+1]=(word,count)
    
    
    WordCount2=WordCount2.set_index('Word')
    WordCount=WordCount.set_index('Word')
    WordCountDict=WordCount.to_dict()
    WordCountDict2=WordCount2.to_dict()
    WordCountDict2=WordCountDict2['Count']
    WordCountDict=WordCountDict['Count']
    
    
    #TF-TR computation for democrats
    
    tftr_Dem = {} 
    
    for word in WordCountDict2:
        if word in WordCountDict:
            tr= WordCountDict2[word]/(WordCountDict[word]+25)
            tftr_Dem[word]=tr
    
    
    
    tftr_Rep={}
    for word in WordCountDict2:
        if word in WordCountDict:
            tr= WordCountDict[word]/(WordCountDict2[word]+25)
            tftr_Rep[word]=tr

    return df,RepTokens,DemTokens    

def RepScoreToTwt(tweet):
    score=0
    i=0
    Twt=''
    words = word_tokenize(tweet) 
    words = [w.lower() for w in words] 
    words = [word for word in words if not word in pun] 
    words = [word for word in words if word.isalpha()] 
    words = [w for w in words if not w in stops] 
    words = [w for w in words if not len(w) == 1]
    for word in words: #loop through the list of words
        word = lemmatizer.lemmatize(word) #return the lemma of each word
        if word in tftr_Rep:
            score+=tftr_Rep[word]
            i+=1
    return score/i
            
def DemScoreToTwt(tweet):
    score=0
    i=0
    Twt=''
    words = word_tokenize(tweet) 
    words = [w.lower() for w in words] 
    words = [word for word in words if not word in pun] 
    words = [word for word in words if word.isalpha()] 
    words = [w for w in words if not w in stops] 
    words = [w for w in words if not len(w) == 1]
    for word in words: #loop through the list of words
        word = lemmatizer.lemmatize(word) #return the lemma of each word
        if word in tftr_Dem:
            score+=tftr_Dem[word]
            i+=1
    return score/i


StateList=['Minnesota',
 'Montana',
 'North Dakota',
 'Idaho',
 'Washington',
 'Arizona',
 'California',
 'Colorado',
 'Nevada',
 'New Mexico',
 'Oregon',
 'Utah',
 'Wyoming',
 'Arkansas',
 'Iowa',
 'Kansas',
 'Missouri',
 'Nebraska',
 'Oklahoma',
 'South Dakota',
 'Louisiana',
 'Texas',
 'Connecticut',
 'Massachusetts',
 'New Hampshire',
 'Rhode Island',
 'Vermont',
 'Alabama',
 'Florida',
 'Georgia',
 'Mississippi',
 'South Carolina',
 'Illinois',
 'Indiana',
 'Kentucky',
 'North Carolina',
 'Ohio',
 'Tennessee',
 'Virginia',
 'Wisconsin',
 'West Virginia',
 'Delaware',
 'District of Columbia',
 'Maryland',
 'New Jersey',
 'New York',
 'Pennsylvania',
 'Maine',
 'Michigan']
StateList.append('Alaska')
StateList.append('Hawaii')

def getState(stt):
    for x in StateList:
        if x in stt:
            return x
        

def StateSentiment(df):
    df['Republican Sentiment']=df.apply(lambda row:RepScoreToTwt(row['Tweets']),axis=1)
    df['Democrat Sentiment']=df.apply(lambda row:DemScoreToTwt(row['Tweets']),axis=1)
    dfRep=df[df['Party']=='Republican']
    dfDem=df[df['Party']=='Democrat']
    
    dfDem['State']=dfDem['State'].apply(lambda stt: getState(stt))
    dfRep['State']=dfRep['State'].apply(lambda stt: getState(stt))
    dfRep=dfRep.groupby(['State']).mean()
    dfDem=dfDem.groupby(['State']).mean()
    dfRep['State']=dfRep.index.to_series()
    dfDem['State']=dfDem.index.to_series()
    us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}


    dfRep['code']=dfRep['State'].apply(lambda state: us_state_abbrev[state])
    dfDem['code']=dfDem['State'].apply(lambda state: us_state_abbrev[state])


    return dfRep,dfDem

def DrawRepMap(dfRep):
    import chart_studio.plotly as py
    from plotly.offline import iplot
    
    scl = [[0, 'rgb(255,200,200)'],[1,'rgb(255,0,0)']]
    
    
    for col in dfRep.columns:
        dfRep[col] = dfRep[col].astype(str)
    
    
    
    
    dfRep['text'] = dfRep.index + '<br>' +\
        'Republican Sentiment '+dfRep['Republican Sentiment']
    
    data = [ dict(
            type='choropleth',
            colorscale = scl,
            autocolorscale = False,
            locations = dfRep['code'],
            z = dfRep['Republican Sentiment'].astype(float),
            locationmode = 'USA-states',
            text = dfRep['text'],
            marker = dict(
                line = dict (
                    color = 'rgb(255,255,255)',
                    width = 2
                )
            ),
            colorbar = dict(
                title = "Sentiment"
            )
        ) ]
    
    layout = dict(
            title = 'Republican Sentiment for Republican Congressmember',
            geo = dict(
                scope='usa',
                projection=dict( type='albers usa' ),
                showlakes = True,
                lakecolor = 'rgb(255, 255, 255)',
            ),
        )
    
    fig = dict( data=data, layout=layout )
    
    url = iplot( fig, filename='d3-cloropleth-map' )
    
    
def drawDemMap(dfDem):


    scl2 = [[0,'rgb(99,151,255)'], [1,'rgb(0,0,255)']]
    
    
    
    for col in dfDem.columns:
        dfDem[col] = dfDem[col].astype(str)
    
    
    
    
    dfDem['text'] = dfDem.index + '<br>' +\
        'Democrat Sentiment '+dfDem['Democrat Sentiment']
    
    data = [ dict(
            type='choropleth',
            colorscale = scl2,
            autocolorscale = False,
            locations = dfDem['code'],
            z = dfDem['Democrat Sentiment'].astype(float),
            locationmode = 'USA-states',
            text = dfDem['text'],
            marker = dict(
                line = dict (
                    color = 'rgb(255,255,255)',
                    width = 2
                )
            ),
            colorbar = dict(
                title = "Sentiment"
            )
        ) ]
    
    layout = dict(
            title = 'Democrat Sentiment for Dem Congressmember',
            geo = dict(
                scope='usa',
                projection=dict( type='albers usa' ),
                showlakes = True,
                lakecolor = 'rgb(255, 255, 255)',
            ),
        )
    
    fig2 = dict( data=data, layout=layout )
    
    url = iplot( fig2, filename='d4-cloropleth-map' )
        
LabMT  = pd.read_excel("ClasseurTest.xlsx") #the xls is just the .txt with every column removed but word and happiness_average
LabMT=LabMT.set_index('word') 
Scores= LabMT['happiness_average'] 

def SentimentTokens(tokFreq):  #Associate a sentiment score to the the output of FreqDist ie a list of tokens and their counts
    Sentiment=0
    count=0
    for tok,freq in tokFreq.items():
        if tok in Scores.keys():                    #only scoring words that are in the LabMT list
            Sentiment+=Scores[tok]*freq
            count+=freq
            
    if count !=0:                             #to avoid error when used on empty text or text without any graded words.
        return Sentiment/count
    else:
        return 5.5 #average of 1 to 10





def GetRepSent(datafr):
    See=[]
    for index,row in datafr.iterrows():
        tweet=row['Tweets']
        tokens=[]
        words = word_tokenize(tweet) 
        words = [w.lower() for w in words] 
        words = [word for word in words if not word in pun] 
        words = [word for word in words if word.isalpha()] 
        words = [w for w in words if not w in stops] 
        words = [w for w in words if not len(w) == 1]
        for word in words: #loop through the list of words
            word = lemmatizer.lemmatize(word) #return the lemma of each word
            tokens.append(word)
        See.append(SentimentTokens(nltk.FreqDist(tokens)) )
    return See



