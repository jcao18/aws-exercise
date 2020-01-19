# Exercise #1

EC2, S3 and Athena are used for this exercise. An EC2 instance is used to run the python script to download the dataset, convert the dataset into csv format and upload the converted dataset to a S3 bucket. A database and table are created in Athena to allow for query and data aggregation. The EC2 instance is optional. The python script can be run on an on-premise PC. 

[census_resources.yaml](census_resources.yaml) is the CloudFormation template used for the deployment. It creates the following resources,

  * EC2 instance
  * IAM user and IAM access key (for the python script to upload the dataset with AWS API)
  * IAM policy (to allow the user access to the S3 bucket)
  * S3 bucket
  * Glue database and table
    
[census_processor.py](census_processor.py) is a simple python script that does the download, convertion and upload. It is run after the resources are deployed via the CloudFormation template. 

Query can be run from the Athena console or through AWS CLI from the EC2 instance.

As for cost, the dataset is less than 80MB, it costs $0.03 per month to host it in a S3 bucket. The cost of the Athena is based on number of queries and calculated as follows,
    (number of queries per month) x (dataset size in TB) x $5 USD
For a 80MB dataset, it costs $0.38 per month for 1000 queries. Since the EC2 instance is optional, its cost is not calculated.

# Exercise #2

I would propose deploying Neo4j on EC2 to build a graph of data. Neo4j is open-source and has a larger support network than Neptune. It supports a wider range of programming languages and has build-in graph visualization which Nepture does not have. It is very easy to deploy Neo4j on EC2 using officially published AMIs, and probably costs less.

For the census migration data, I would design the graph model as follows, 

  * Node: State
    * Property: name, code
  * Node: County
    * Property: name, code, migration population
  * Relationship: Is part of
    * between State and County
  * Relationship: Move
    * between County and County
    * Property: direction, number of mover
    
The cypher query language (LOAD CSV command) is used to load data into Neo4j. 'State' nodes are created by extracting state name and code from the dataset. 'County' nodes are created by extracting county name and code and all the migration population data from the dataset. Relationships 'Is part of' are created by extracting rows from the dataset and matching them against the newly created 'State' nodes and 'County' nodes. Similarly, 'Move' relationships are created by extracting rows from the dataset and matching them against the newly created 'County' nodes.
