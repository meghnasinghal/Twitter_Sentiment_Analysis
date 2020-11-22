# Twitter_Sentiment_Analysis

Implemented the following framework using Apache Spark
Streaming, Kafka (optional), Elastic, and Kibana. The framework performs SENTIMENT analysis of particular hash tags in twitter data in real-time. For example, we want to do the sentiment analysis for all the tweets for #trump, #coronavirus. 

The framework has the following components:

1. Scrapper (for python, but Scala needs to produce same result)
The scrapper will collect all tweets and sends them to Kafka for analytics. The scraper will be a standalone program written in PYTHON and should perform the followings:
a. Collecting tweets in real-time with particular hash tags. For example, we will collect all tweets with #trump, #coronavirus.
b. After filtering, we will send them to Kafka (as Python is used)
c. Used Kafka API (producer) in the program (https://kafka.apache.org/090/documentation.html#producerapi)
d. The scrapper program will run infinitely and takes hash tag as input parameter while running.

2. Kafka (for Python)
Installed Kafka and run Kafka Server with Zookeeper. Created a dedicated channel/topic for data transport

3. Spark Streaming
In Spark Streaming, Created a Kafka consumer (for python, shown in the class for streaming) and periodically collect filtered tweets (required for both Scala and python) from scrapper. For each hash tag, performed sentiment analysis using Sentiment Analyzing tool (discussed below). 

3. Sentiment Analyzer
Sentiment Analysis is the process of determining whether a piece of writing is positive, negative or neutral. It's also known as opinion mining, deriving the opinion or attitude of a speaker.

For example,

“President Donald Trump approaches his first big test this week from a
position of unusual weakness.” - has positive sentiment.

“Trump has the lowest standing in public opinion of any new president in
modern history.” - has neutral sentiment.

“Trump has displayed little interest in the policy itself, casting it as a
thankless chore to be done before getting to tax-cut legislation he values
more.” - has negative sentiment.

The above examples are taken from CNBC news:
http://www.cnbc.com/2017/03/22/trumps-first-big-test-comes-as-hes-in-an-
unusual-position-of-weakness.html

We have used StandardCoreNLP for sentiment analysis.

Note: You can use any third-party sentiment analyzer like Stanford CoreNLP
(Scala), NLTK(python) for sentiment analyzing. For example, you can
add Stanford CoreNLP as an external library using SBT/Maven in your
Scala project. In python you can import NLTK by installing it using pip.

4. Elasticsearch
Installed the Elasticsearch and run it to store the tweets and their sentiment information for further visualization purpose.
You can point http://localhost:9200 to check if it’s running.
For further information, you can refer:
https://www.elastic.co/guide/en/elasticsearch/reference/current/getting-started.html

5. Kibana
Kibana is a visualization tool that can explore the data stored in Elasticsearch. Instead of directly output the result, we used the visualization tool to show the tweets sentiment classification result in a real-time manner. 
Please see the documentation for more information: 
https://www.elastic.co/guide/en/kibana/current/getting-started.html



CONFIGURATION USED:
kafka_2.13-2.5.0
stanford-corenlp-4.1.0
elasticsearch-7.6.2
kibana-7.6.2-darwin-x86_64


