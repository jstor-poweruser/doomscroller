# "Doomscroller"
## The inspiration
Since I spend so much time lately on Twitter thinking about the country's degredation of democracy, I thought it might be helpful to my misery to create an application that weeds out any Tweets in my feed that have any amount of optimism in them. To do this, I want to harness AWS serverless architecture, the Twitter Developer API, and infrastructure-as-code deployments through AWS SAM. 

## How does it work?
Here's the rough plan:
![alt text](https://github.com/delaneykranz/doomscroller/blob/main/docs/tentative-plan.png?raw=true)

When a user makes a new request, it will open up a websocket in API Gateway. 

DynamoDB is going to be the main hub of Tweets that have been vetted for negativity. When a user issues their first request, the logic will go one of two ways:

1. If the user has made a request before, then there should be some already-processed Tweets for them stored in DynamoDB already. We query Dynamo for some Tweets to have on the feed while waiting for the next ones to be processed.
2. If te user has not made a request before, they have to just wait for some Tweets to be processed.

Any time a user makes a request, a message is sent to an SQS queue signalling "hey, get me some Tweets". A Lambda function will kick off polling for Tweets from the Twitter Developer API, which it then sends to Amazon Comprehend, a NLP processor that will root out any Tweets that have a positive sentiment. We then write Tweets with a negative sentiment to DynamoDB.

Finally, another Lambda function is fired by a write to Dynamo, and issues the newly-processed tweet to the user's feed.

I am planning on making a shitty, disgusting front-end for this in React.js. Lambdas will be written in Python because I think I'm illiterate in any other language at this point, and the AWS infrastructure will be deployed through AWS SAM yaml files. We'll see if I actually do this or if it's just some fever dream