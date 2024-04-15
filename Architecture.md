# RAG Project Architecture

## High-Level Architecture
The RAG project consists of the following components:
- LLM orchestrator: LlamaIndex
- LLM: OpenAI
- Embeddings: OpenAIEmbedding(model="text-embedding-3-small") 
- Relational data: Sqlite
- Vector Store: ChromaDB
- API Interface: FastAPI.

## Data Flow
1. Data loaded from Kaggle in csv format.
2. Data cleaned and loaded to Sqlite. (script:./etl/1_data_loading.py)
3. Vector generated and stored in Chroma DB (script:./etl/2_data_indexing.py)
4. Input Query: User provides a natural language query.
5. Retrieval: Retriever module retrieves vectors from the vector store.
6. Generation: Generator module generates a response based on the retrieved information and input query.
7. Output Response: The generated response is returned to the user.

## Constraints
1. **Data Model**: Due to time constrains, the data model is a denormalized table. For future improvements, this model would store data as follows:
Create a dimension model following star schema. Fact Table: Results of marathoners; Time Dimension: Date and time information; Marathon dimension: Marathon name, description, and characteristics; Geography dimension: to store countries and cities; Runners Dimension: to store runners names and other information like category (Slowly Changing dimension).

2. I considered structured data, because I am a marathon fan and since last year I was thinking how to help Boston Organizers to get data from runners without the need to learn sql. This kind of API could connect with other sports apps to help organizers get important information. Due to the limited time, I could not scrape information from different marathons, and I used a Kaggle dataset.

3. Because of the size of the application currently is not considered to have cache embeddings. However, it would be useful to consider for escalation after many iterations and user base growth.

4. In the future the application can also get data from weather, and sentiment from social media to provide more information to organizers and provide customized services to their runners.


## Dependencies
- Python 3.10.8
- LLama Index
- Open AI
- FastAPI
- Pydantic
- Pandas
- Sqlalchemy
- ChromaDB

## Data Source
Acknowledgements: 
    Data obtained from Kaggle https://www.kaggle.com/datasets/rojour/boston-results.
    Author: Rojour https://www.kaggle.com/rojour
    Data was scrapped from the official marathon website - http://registration.baa.org/2017/cf/Public/iframe_ResultsSearch.cfm\n\n"

## Scalability and Performance
The RAG project is designed to scale with large datasets and handle multiple concurrent requests efficiently. Performance optimizations are implemented to minimize response latency.

## Project Structure

The project directory structure is organized as follows:

Root/
│
├── config/
│
├── src/
│
├── etl/
│
├── db/
│
├── chromadb/
│
├── raw_data/
│
└── test/


## Root Directory (/root)

The root directory serves as the main directory for the project.

## Directories
- **config**: Contains json file to store and keep OPEN AI safe.
- **src**: Contains the source code files for the project.
- **etl**: Contains scripts related to Extract, Transform, Load (ETL) processes.
- **db**: Contains database-related files.
- **chromadb**: Contains files related to vector databases.
- **raw_data**: Contains csv files with raw data.
- **test**: Contains test scripts for testing the project.

### Files
- main.py - Script to start FastAPI server.
- API response test.ipynb - Notebook that serves as user testing.
- requirements.tx - Python dependencies.
- ./src/1_data_loading.py - Script to read raw data, clean and store in a relational database.
- ./src/2_data_indexing.py - Script to generate and store embeddings.
