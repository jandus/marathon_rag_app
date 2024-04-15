# MARATHON RAG API Project

## Overview
This project introduces a Retrieval-Augmented Generator (RAG) model created for natural language processing tasks, accessible via an API. Specifically designed to facilitate inquiries regarding Boston Marathon results from the years 2015, 2016, and 2017, this tool help marathon organizers to extract pertinent information effortlessly, without the necessity of SQL or query languages knowledge.

In its current iteration, the project focuses on getting data exclusively from the Boston Marathon. However, with future iterations, the aim is to expand data acquisition to encompass Boston Qualifier marathons globally. By doing so, the project will provide assistance to Boston organizers in data validation and runner identification, while simultaneously offering support to other marathon organizations seeking runner information.

Information about architecture and folder structure please review ARCHITECTURE.md

## Usage
To use the RAG model, follow these steps:
1. Clone the repository.
2. Create and activate a new environment.
3. Install the dependencies.
    This project was developed with Python 3.10.8.
open a terminal and cd to the project root folder (/marathon_rag_app)
then execute following command:
pip install -r requirements.txt
4. Open an account in OPENAI.
    4.1 Open the account.
    4.2 Create a Key
    4.3 Copy the Key. 
    4.4 Create a new file under config folder and name it as config.json.
    4.5 Open the new file and copy the json below from "{" to "}" and replace <your key here> with your key.

```json
{
    "OPENAI_API_KEY": "<your key here>"
}
```

5. Start FastAPI Server.
    5.1 Open a Terminal or CMD.
    5.1 Change to root directory (/marathon_rag_app).
    5.2 execute command below:
    uvicorn main:app --reload
6. Start Using the API.
    6.1 You can test the API with different options:
        1. Open the notebook "API response test.ipynb"
            This notebook contains an example to use the application.
        2. Open API documentation http://localhost:8000/docs
            This page will show you usage of the API with all its methods. In this documentation you can request information.
        3. Use any http request tool like postman or curl.
7. Get response from the RAG model.

## Installation
To install the project dependencies, run:
pip install -r requirements.txt

## FAST API Server

### How to start FAST API Server
Change to root directory (/marathon_rag_app)
Execute following command:

```bash
uvicorn main:app --reload
```

## How to Stop FAST API Server
Type:
    Ctrl + c (This will terminate the service)

## Configuration
The RAG model can be configured using the following parameters:
- Structured csv data is loaded into a Sqlite database after cleaned and organized.
- Then Data is transformed in nodes and converted in Vectors.
- Vectors are stored in ChromaDB.
NOTE: These steps have been executed. No need to run it.

## Examples
Here are some examples of how to use the RAG model:
- Example 1: Querying for information about a Boston Marathon results such as "Who won Boston marathon 2015? did that person run a negative split? what was this person overall time and 5k time?"