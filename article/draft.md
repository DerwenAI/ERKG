## Leverage entity resolution to construct knowledge graphs

## Introduction

This article provides a hands-on tutorial to get started running both [Senzing](https://senzing.com/) for _entity resolution_ and [Neo4j](https://neo4j.com/) for _knowledge graphs_, working in Python code.
We'll begin with three datasets, clean up entities in the data, and finally build a knowledge graph from the results.
The code shown here is intended to be simple to download, easy to follow, and presented so you can also try it with your own data.

In this tutorial we'll be working in two environments which require some hands-on configuration and coding.
The examples show code at level which should be fine for most anyone working in data science.
You need to have some familiarity with each of the following:

  - simple Python programming
  - using a Linux command line
  - cloning a public repo from GitHub

Although _knowledge graphs_ (KGs) have been around for many years, there's been lots of recent interest due to uses with AI. For example, it turns out that KGs are super helpful to "ground" the prompts and results of chatbots, to reduce "hallucination" errors in AI models.

We need to discuss about _entity resolution_ (ER), which becomes especially important when you're working with knowledge graphs.
Recognize that knowledge graphs help us understand about _relations_ between _entities_.
You can think in terms of language grammar, where entities are the "nouns" and relations are the "verbs" connecting them.
In the sentence `"Jack catches the ball"` there are two entities `"Jack"` and `"the ball"` which are both nouns, and these are connected by a relation `"catches"` which is a verb.
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

Use ER on your data records first, then build your graph.
This is a much better way to produce useful graph data and make the most of KGs, AI applications, and so on.


## Senzing and Neo4j background

Before we jump into code, let's cover some background about the two technologies we're showing in this tutorial: Senzing and Neo4j.

[Senzing](https://senzing.com/) provides a 6th generation industrial strength engine for _entity resolution_.
The product has been shipping since 2012 and is used around the world by law enforcement, tax authorities, defense/ intelligence agencies, and enterprise applications in general.
The company's expertise in this field is stellar: people on this team have on average more than 20 years experience in entity resolution production, often in extreme cases.

Note that the code for Senzing is open source.
Check out <https://github.com/Senzing> on GitHub where you can find more than 30 public repos.
You can download and get running right away, with a free license for up to 100,000 records.
This scales from the largest use cases all the way down to running on a laptop.
You can run from Docker containers available as source on GitHub or images on [Docker Hub](https://hub.docker.com/u/senzing), or develop code using [API bindings](https://docs.senzing.com/) for Java and Python.

A motto at the company is "We see transmissions, not cars."
To be clear, everything about this technology is laser-focused on providing speed, accuracy, and throughput for the best quality entity resolution available -- connecting the right data to the right person, in real time.
For details about the company, see the ["Senzing AI: A New Era"](https://senzing.com/senzing-ai-video/).
For deep-dives into how Senzing _entity resolution_ works, see these two techincal overview articles:

  - ["Principle-Based Entity Resolution Explained"](https://senzing.com/principle-based-ER)
  - ["Entity Resolution Capabilities to Consider"](https://senzing.com/er-capabilities)

[Neo4j](https://neo4j.com/) is the world's most popular solution for graph databases.
It provides native graph storage, graph data science, graph machine learning, analytics, and visualization -- with enterprise-grade security controls to scale transactional and analytic workloads.

First released in 2010, Neo4j pioneered using [Cypher](https://en.wikipedia.org/wiki/Cypher_(query_language)), a declarative graph query language for _labeled property graphs_.
As mentioned, graphs help us understand **relationships**.
In contrast, relational databases, data warehouses, data lakes, data lakehouses, etc., tend to emphasize **facts**.
That's important because AI -- and for that matter, _business decisions_ in general -- depend on relationships within the data.

Extending from the "nouns" and "verbs" analogy we'd described above, Cypher also provides for _properties_.
You can think of these as the "adjectives" in human language.
The expressiveness of Cypher queries results in data analytics applications with 10x less code than comparable applications written in SQL.

Neo4j has an incredible developer community, with so many resources available online.
Check out  <https://github.com/neo4j> on GitHub for more than 70 public repos supporting a wide range of graph technologies.
For an excellent introduction overall, see the recent ["Intro to Neo4j"](https://www.youtube.com/watch?v=YDWkPFijKQ4&t=572s) video.
Also check the many courses, certifications programs, and other resources at [GraphAcademy](https://graphacademy.neo4j.com/).


## Getting started with Neo4j

To get started coding, first let's set up a _Neo4j Desktop_ application, beginning with the download instructions at <https://neo4j.com/download/> for your desktop or laptop.
This is available on Mac, Linux, and Windows.
While there are multiple ways to get started with Neo4j, Desktop provides a quick way to begin working with the general set of features that we'll need.

Once the download completes, follow the [instructions to install the Desktop application](https://neo4j.com/docs/desktop-manual/current/installation/download-installation/) and register to obtain an activation key for it.
Then open the application and copy/paste your activation key.

Next, [create a new project and a database](https://neo4j.com/docs/desktop-manual/current/operations/create-dbms/) -- named `Senzing` in our example, located within the `Entity Resolution` project.
By default `neo4j` is the user name for accessing this database, then Neo4j Desktop requires setting a password -- `Z1ngs3n!` in our example.
You'll also need to select a version -- we'll use 5.17.0 which is recent at the time of this writing.

![Neo4j Desktop application window](img/neo4j_desktop.png)

Click on the newly created database, then a right side panel will show settings and administrative links -- as shown in the "Neo4j Desktop" figure.
Click on the `Plugin` link, open the `Graph Data Science Library` drop-down, then install this plugin.
We'll use the GDS library to access the Neo4j graph database through Python.

Click on the reset button, next to `Stop` -- or simply stop the database, then start it again.
Your GDS plugin will be in place, and local service endpoints for accessing the graph database should be ready.
Now click on the `Details` link and find the port number for the [Bolt protocol](https://neo4j.com/docs/bolt/current/bolt/).
In our example `7687` is the Bolt port number.

Next, open a browser window to our GitHub public repo for this tutorial:

  - <https://github.com/Senzing/ERKG>

Clone the repo by copying its URL from GitHub, as shown in the "Clone public repo" figure.
Then use the following steps to create your **working directory** on your desktop/laptop for this tutorial:

```
git clone https://github.com/Senzing/ERKG.git
cd ERKG
```

After connecting into your working directory, create a file called `.env` which provides the credentials (Bolt URL, DBMS username, password) needed to access the database in Neo4j Desktop through Bolt:

```
NEO4J_BOLT=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASS=Z1ngs3n!
```

Neo4j Desktop provides many useful tools, including a browser for exploring your graph database and running [Cypher queries](https://neo4j.com/docs/cypher-manual/current/introduction/), and the [Bloom data visualization tool](https://neo4j.com/product/bloom/).
You can also export and import "dumps" of your database on disk, to manage backups.

Now you're good to go!
For the rest of this tutorial, keep this Neo4j Desktop application running in the background.
Even so, mostly we will access Neo4j through the [GDS library](https://neo4j.com/docs/graph-data-science/current/installation/neo4j-desktop/) using Python code.


## The input datasets

[ pull markdown+images from `datasets.ipynb` ]

We'll be working with three datasets to run entity resoultion and build a knowledge graph.
To start, let's set up a Python environment and install the libraries we'll need, then run code examples inside a [Jupyter](https://jupyter.org/) notebook.
We show use of Python 3.11 here, although other recent versions should well too.

Set up a virtual environment for Python and load the required dependencies:

```
python3.11 -m venv venv
source venv/bin/activate
python3 -m pip install -U pip wheel setuptools
python3 -m pip install -r requirements.txt
```

This tutorial uses several popular libraries that are common in data science work:

```
icecream >= 2.1
ipywidgets >= 8.1
jupyterlab >= 4.1
jupyterlab_execute_time >= 3.1
matplotlib >= 3.8
graphdatascience[networkx] >= 1.9
python-dotenv >= 1.0
seaborn >= 0.13
tqdm >= 4.66
watermark >= 2.4
```

Now run the 


	1. Set up env for Python, Jupyter, Neo4j, etc.
	2. Link to sources: SafeGraph POI, DoL WHISARD, SBA PPP
	3. Load each dataset into a Pandas dataframe
		- Explore the ranges of fields available
	    - Which details could be useful for constructing a KG?
	4. Use the GDS wrapper in Python
		- <https://github.com/neo4j/graph-data-science-client>
		- <https://neo4j.com/docs/graph-data-science/current/>
		- Docs for Cypher <https://neo4j.com/docs/cypher-manual/current/introduction/>
	5. Load records into Neo4j `:Record`​ nodes/props


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


## Examine the results
(**Jupyter**)

pull from `2.results.ipynb`

    1. Load entities into Pandas, run light summary analysis
    2. Use the GDS wrapper over the Neo4j driver in Python
    3. Connect the KG
		1. Load entities into Neo4j `:Entity` nodes/props
		2. Connect entities with resolved records, add props
		3. Connect entities with related entities, add props
		4. Simple initial schema on Desktop Browser: 
			- `CALL db.schema.visualization()`
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
		- Senzing follow-ups
