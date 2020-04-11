##1 How and what 
This is microservice for 'judge client' and 'web client'.

###1.1 The 'Judge Client'
The 'judge client' is program can compile source code and run with test data ,then it will post judge result to this microservice.

The judge client is writen in c++ and store in 'OJClient' repository. 

###1.2 The 'Web Client'
The 'web client' is you program which user the api to judge source code.

##2 For Development
More detail on this software

###2.1 The json fields in web api and store in redis
The problem and judege result was save in redis. More details in 'db.models.py' file.





