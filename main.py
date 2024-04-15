from fastapi import FastAPI
from pydantic import BaseModel

from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings
from llama_index.core import VectorStoreIndex

import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.core import PromptTemplate

# OPENAI API KEY
import os
from src.utils import load_key

description = """
Marathon Results API helps you get ask questions about finishers in boston marathon 2015, 2016 and 2017. 🚀

## Get Question

You can ask questions about boston Marathon using human language **read items**.

## Sample Questions

You will be able to:

* **Query about users Boston Marathon finishers, you can list based on different variables, you can also ask if they ran negative split** 

"""

# Set up environment variables
load_key()                                                              # Setup OPENAI Key
# Set Model and Embedding
Settings.llm = OpenAI(model="gpt-3.5-turbo")
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")  # "text-embedding-ada-002"  <- default  other option -> model="text-embedding-3-small"

app = FastAPI(
    title="Marathon results",
    description=description,
    summary="This API allows you to ask questions about Boston Marathon finishers using natural language. This is for Marathon applications which help Marathon organizers to get data without knowing SQL and in a simple way",
    version="0.0.1",
)

class Question(BaseModel):
    question: str

# initialize client
db = chromadb.PersistentClient(path="./chroma_db")

# get collection
chroma_collection = db.get_or_create_collection("boston_marathon")

# assign chroma as the vector_store to the context
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# load your index from stored vectors
index = VectorStoreIndex.from_vector_store(
    vector_store, storage_context=storage_context, embed_model=Settings.embed_model,
)

template = (
    "You are helping Marathon Organizers or Marathon Runners to find information"
    "We have provided context information below. \n"
    "---------------------\n"
    "{context_str}"
    "\n---------------------\n"
    "Given this information, please answer the question: {query_str}\n"
)
qa_template = PromptTemplate(template)



@app.get("/get_question/")
async def get_question(question: Question):
    """
    Retrieve an answer to a question related to the Boston Marathon results from the years: 2015, 2016 and 2017.

    - **question**: User question related to Boston Marathon results (string).

    Example question: "What was the average finishing time for runners aged 30-40 in the Boston Marathon 2019?"
    """

    # Use the custom prompt when querying
    data = question.question
    query_engine = index.as_query_engine(text_qa_template=qa_template)
    answer = query_engine.query(data) 
 
    return answer.response


@app.get("/data_information/")
async def get_sample():
    return [
        {
            "Data Source Description": """
                Infomration about Boston Marathon was obtained from Kaggle.
                It's important to highlight that the Boston Marathon is the oldest marathon run in the US as it is the only
                marathon (other than olympic trails) that most of the participants have to qualify to participate.
                For the professional runners, it's a big accomplishment to win the marathon.
                For most of the other participants, it's an honor to be part of it.
                Content: It contains the name which is the name of the runner formated as '[First Name],[Last Name]', it also contains other fileds which names are self descriptive
                Acknowledgements:Data was scrapped from the official marathon website - http://registration.baa.org/2017/cf/Public/iframe_ResultsSearch.cfm\n\n
                Original Data Link: https://www.kaggle.com/datasets/rojour/boston-results\n
                Author: Rojour https://www.kaggle.com/rojour
            """
        }
]

#run it 
#uvicorn main:app --reload
# test from browser
#   http://localhost:8000/


