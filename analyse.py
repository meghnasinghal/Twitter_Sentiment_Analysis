import json, re
import sys
from stanfordcorenlp import StanfordCoreNLP

scn = StanfordCoreNLP('http://localhost',port=9000,timeout=30000)

def analyse(sentence):    
    #Connect to StanfordCoreNLP to get the sentiment analysis for each tweet
    #follows the pipeline tokenize, ssplit, pos, lemma, parse, sentiment
    result = scn.annotate(sentence, properties={
        'annotators': 'sentiment',  #specifying the return -- sentiment
        'outputFormat': 'json',
        'timeout': '50000'
    }).strip()
    if not result:
        return "None"
    else:
        result = json.loads(result)
        if result['sentences']:
            return result['sentences'][0]['sentiment'] #return sentiment for sentence
        else:
            return "None"
