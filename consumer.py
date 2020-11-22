import os
#mapping object that represents the user’s environmental variables
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.4.5 --jars spark-streaming-kafka-0-8_2.11-2.4.5.jar --jars elasticsearch-hadoop-7.6.2.jar pyspark-shell' 

import json
import re
import hashlib
from analyse import analyse
from kafka import KafkaConsumer
from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from elasticsearch import Elasticsearch


es = Elasticsearch()

#to get sentiment of the tweet
def analysis(sentence):
    return analyse(sentence)
    
#filter tweets with hastag corona
def corona_filter(tweet):
    for i in ["#corona","#coronavirus","#covid19","#covid-19"]:
        if i in tweet:
            return True
    return False

#filter tweets with hashtag donald
def donald_filter(tweet):
    for i in ["#donald","#donaldtrump","#trump"]:
        if i in tweet:
            return True
    return False

#parse data and adding to dictionary with keys as tweet and  values as sentiment for the tweet
def parse(rdd):
    d={}
    d['tweet']=rdd[0]
    d['senti']=rdd[1]
    return d

#filter text before sending for sentiment analysis
def filter(text):
    text = re.sub(r'http\S+', "", text) #remove urls
    text = ' '.join(re.sub(r'[^\w.\s#@/:%,_-]|', "", text).split()) #filter special keywords/symbols using regular expressions
    return text

# def uploadtoelatic(data):
#     es.index(index="tweet",doc_type="test-type",body={"author":"hi", "message":data})
#     return

#take a sentence and creating a id for it
def addId(data):
    j=json.dumps(data).encode('ascii','ignore') #getting the data as string with encoding as ascii and errors = ignore
    data['doc_id']=hashlib.sha224(j).hexdigest() #get a hash object and store it as doc_id of data
    return (data['doc_id'],json.dumps(data)) #return the data doc id and json data

if __name__ == "__main__":

#configuration for corona hashtags

    # corona_write_conf = {
    #     "es.nodes" : "localhost",
    #     "es.port" : "9200",
    #     "es.resource" : 'corona/corona-doc',
    #     "es.input.json": "yes",
    #     "es.mapping.id": "doc_id"
    # }

#configuration for trump hashtags

    donald_write_conf = {
        "es.nodes" : "localhost",
        "es.port" : "9200",
        "es.resource" : 'donaldtest/donald-doc',
        "es.input.json": "yes",
        "es.mapping.id": "doc_id"
    }
    
    #create spark configuration and run Spark locally with as many worker threads as logical cores on the machine.
    conf = SparkConf().setMaster("local[*]").setAppName("Twitter_Sentiment_Analysis") 
    #create spark context
    sc = SparkContext(conf = conf)
    sc.setLogLevel("WARN") #reducing the amount of trace info spark context produces
    sparkstream = StreamingContext(sc, 10) #spark streaming for every 10 units of data (messages)
    sparkstream.checkpoint(r'./checkpoint') #set checkpoints after that instance

    #kafka stream created using spark streaming on topic "twitter"
    kafkaStream = KafkaUtils.createStream(sparkstream, 'localhost:2181', 'tweets-consumer', {"twitter":1})  
    data_all = kafkaStream.map(lambda x: json.loads(x[1])) #get all data using kafka as a json
    sentiment_analysis = data_all.map(lambda tweet: (str(filter(tweet['text'])),analysis(filter(tweet['text'])))) 
    #perform sentiment analysis by calling the analyse function and filtering the text before sending


#filter the tags and parse them as key value pairs and add unique id and save them as new hadoopfile using the configurations

    # coronaHashTags=sentiment_analysis.filter(lambda x:corona_filter(x[0].lower())).map(lambda value:value).map(parse).map(addId)
    # coronaHashTags.foreachRDD(lambda rdd: rdd.saveAsNewAPIHadoopFile(
    #     path='-',
    #     outputFormatClass="org.elasticsearch.hadoop.mr.EsOutputFormat",       
    #     keyClass="org.apache.hadoop.io.NullWritable",
    #     valueClass="org.elasticsearch.hadoop.mr.LinkedMapWritable",
    #     conf=corona_write_conf))

    donaldHashtags=sentiment_analysis.filter(lambda x:donald_filter(x[0].lower())).map(lambda value:value).map(parse).map(addId)
    donaldHashtags.foreachRDD(lambda rdd: rdd.saveAsNewAPIHadoopFile(
        path='-',
        outputFormatClass="org.elasticsearch.hadoop.mr.EsOutputFormat",       
        keyClass="org.apache.hadoop.io.NullWritable",
        valueClass="org.elasticsearch.hadoop.mr.LinkedMapWritable",
        conf=donald_write_conf))
    

    sparkstream.start();
    sparkstream.awaitTermination()



