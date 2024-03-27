## Using Entity Resolution to construct a Knowledge Graph

## Introduction
(**Report**)

This article provides a hands-on tutorial to get started running both [Senzing](https://senzing.com/) for _entity resolution_ and [Neo4j](https://neo4j.com/) for _knowledge graphs_.
We'll begin with three datasets, clean up entities in the data, and finally build a knowledge graph from the results.
The code shown here is intended to be simple to download, easy to follow, and presented so you can also try it with your own data.

Although knowledge graphs (KGs) have been around for many years, there's been lots of recent interest due to uses with AI. For example, it turns out that KGs are super helpful to "ground" the prompts and results of chatbots, to reduce "hallucination" errors in AI models.

First, we need to discuss about _entity resolution_ (ER), which becomes especially important when you're working with knowledge graphs.
Knowledge graphs help us understand about _relations_ between _entities_.
You can think of these in terms of language grammar, where entities are "nouns" and relations are the "verbs" connecting them. In the sentence `"Jack catches the ball"` there are two entities `"Jack"` and `"the ball"` which are both nouns, and these are connected by a relation `"catches"` which is a verb.
This approach of using graphs allows for very flexible ways of representing knowledge in general.
Also, there are many powerful algorithms which can be applied for graph data, plus queries, graph machine learning, and so on.

But there are caveats.
If the quality of our input datasets is anything like _most_ data in the world, there will be errors.
Imagine that someone named `"Robert Smith"` lives on `"First Street"` in a large city, and there's also `"Robert A. Smith"` and `"Robert Smith, Jr."` or some typo introduced in official records, confusing either their names or addresses.
Either case makes record matching confusing and within public records "confusing" might get numbered in the tens, or hundreds, or thousands.
On the one hand, `"Robert X."` might not be amused to receive an electricity bill for `"Robert A."` when the post office mixes up records.
On the other hand, if `"Robert X."` recently fled from an arrest, `"Robert A."` is going to hope the police department doesn't make the same mistake.

When we build knowledge graphs we want to make sure that unique entities don't get fragmented into a bunch of other poorly connected entities.
Nor do we want differing entities to get collapsed into one giant blob.
The process of ER involves highly sophisticated decisions about input data records, being careful to consolidate multiple references to the same entity together, while splitting references which are different.
In other words, when we scan a thousand records from different sources describing a community, then based on names and addresses we want to determine which records are shared by the same entity, and which records represent unique entities.

By the way, if you're already familiar with _natural language processing_ (NLP) tools used in data science, such as the popular [`spaCy` library](https://spacy.io/) in Python, you may have used [_named entity recognition_](https://nlpprogress.com/english/named_entity_recognition.html) (NER) previously.
Understand that NER is quite different from ER: NER simply identifies spans of text which are likely to be proper nouns (i.e., entities) then tags them with labels.
So is `"Jack"` a person, place, or thing?
Jack is a person.
The ball is a thing.
NER provides `"person"` and `"thing"` as labels.
That's helpful for _parsing_ text, but not especially useful for constructing KGs.
Your input data might contain references to different but overlapping entities, in which case after running NER you'll need to clean up the KG by _disambiguating_ entities **after** they've been linked.
That's generally quite a mess, and can be costly.
Use ER on the data records first, then build your graph.
This is a much better way to produce useful graph data and make the most of KGs, AI applications, and so on.


## Senzing and Neo4j background
(**Report**)

	1. Senzing
		- <https://www.linkedin.com/events/7165310793893281793/comments/>
		- currently the 6th generation industrial strength engine for _entity resolution_, since 2009 (shipping since 2012)
		- people on this team have 20+ years avg experience
		- scales from the largest use cases all the way down to running on a laptop
		- "We see transmissions, not cars."
		- "Connect the right data to the right person, in real time."
		- Speed, accuracy, throughput
	
	2. Neo4j
		1. Graph Database
		2. <https://www.youtube.com/watch?v=YDWkPFijKQ4&t=572s>
		3. names, verbs, adjectives => nodes, relations, properties
		4. graphs help us understand relationships, while tables emphasize facts


## The input datasets
(**Jupyter**)

pulled from `1.datasets.ipynb`

	1. Link to sources: SafeGraph POI, DoL WHISARD, SBA PPP
	2. Set up env for Jupyter, etc.
	2. Load each in a Pandas dataframe
	3. Explore the ranges of fields available
	4. Which details could be useful for constructing a KG?


## Using Senzing
(**Cloud**)

  	1. Point to docs, API, etc.
  	2. Set up and configure on a Linux server
	3. Load the datasets
	4. Run entity resolution, explore within Senzing
	5. Export JSON, linking entities and component records

Launch a Linux server running Ubuntu 20.04 LTS server with 4 vCPU, 16 GB memory.

See: <https://senzing.zendesk.com/hc/en-us/articles/115002408867-Quickstart-Guide>

```bash
wget https://senzing-production-apt.s3.amazonaws.com/senzingrepo_1.0.1-1_amd64.deb
sudo apt install ./senzingrepo_1.0.1-1_amd64.deb
sudo apt update
sudo apt upgrade
```

Depending on the Linux distribution, this may require installing `libssl1.1` as well, which is described in
<https://stackoverflow.com/questions/73251468/e-package-libssl1-1-has-no-installation-candidate>:

```bash
wget http://archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2_amd64.deb
sudo dpkg -i libssl1.1_1.1.1f-1ubuntu2_amd64.deb
```

Then install Senzing, which will be located in the `/opt/senzing/data/current` directory:

```bash
sudo apt install senzingapi
```

Now create a project `~/senzing` in the current user's home directory and set up its configuration:

```bash
python3 /opt/senzing/g2/python/G2CreateProject.py ~/senzing
cd ~/senzing
source setupEnv
./python/G2SetupConfig.py
```

Prepare to load our three datasets into Senzing as data sources:

```bash
./python/G2ConfigTool.py
	+ addDataSource SAFEGRAPH
	+ addDataSource DOL_WHISARD
	+ addDataSource PPP_LOANS
	+ save
	+ y
	+ quit
```

We'll specify using up to 16 threads, to parallelize the input process:

```bash
./python/G2Loader.py -f lv_data/poi.json -nt 16
./python/G2Loader.py -f lv_data/dol.csv -nt 16
./python/G2Loader.py -f lv_data/ppp.csv -nt 16
```

Finally, export the resolved entities as the `export.json` local file:

```bash
./python/G2Export.py -F JSON -o export.json
```


## Working in Neo4j
(**Desktop**)

    1. Set up Neo4j desktop
		- Browser, Bloom vs. cloud, etc. 
    2. Create a database
    3. Run local service endpoint for accessing the graph DB
    4. Describe the intended KG schema


## Examine the results
(**Jupyter**)

pull from `2.results.ipynb`

    1. Use the Neo4j driver in Python
		- GDS
		- Point to docs for Cypher, Python API, etc.
    2. Load entities into Pandas, run light summary analysis
    3. Build a KG
		1. Load entities into Neo4j `:Entity` nodes/props
		2. Load datasets into Neo4j `:Record`​ nodes/props
		3. Connect entities with resolve records, add props
		4. Connect entities with related entities, add props
		5. Simple initial schema on Desktop Browser: `CALL db.schema.visualization()`
    4. Analyze impact of ER
		1. Cypher + Pandas to analyze ER connectivity
		2. Visualize to illustrate the convergence of the dataset records through entity resolution


## What's difficult to obtain without a graph database?
(**Jupyter**)

    1. SafeGraph POI has business categories and NAICS codes – natural links and taxonomy for adding more relations to the KG, to build structure
    2. Use geo coordinates to visualize map as a quick example use case


## Summary
(**Report**)

    1. Mention popular needs for this kind of work, e.g., GraphRAG
		- <https://neo4j.com/developer-blog/knowledge-graph-rag-application/>
	2. Next steps...
		- <https://graphacademy.neo4j.com/> 
		- Senzing follow-up
