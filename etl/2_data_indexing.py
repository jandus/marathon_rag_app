from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import (
    Settings,
    VectorStoreIndex,
    StorageContext
)
from llama_index.core.objects import (
    SQLTableNodeMapping,
    ObjectIndex,
    SQLTableSchema,
)

# Vector Store
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore

from llama_index.core import SQLDatabase
from sqlalchemy import (
    create_engine,
)

# OPENAI API KEY
from utils import load_key

# Set up environment variable to connect to OPENAI
load_key()

# Set llm Configuration Variables Variables
Settings.llm = OpenAI(model="gpt-3.5-turbo")
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small") # "text-embedding-ada-002"  <- default  other option -> model="text-embedding-3-small"

engine = create_engine('sqlite:///../db/marathon.db')
sql_database = SQLDatabase(engine, include_tables=["marathon_results"])



db = chromadb.PersistentClient(path="../chroma_db") # initialize client, setting path to save data
# create collection
chroma_collection = db.get_or_create_collection("boston_marathon")
# assign chroma as the vector_store to the context
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)


# manually set extra context text
marathon_results_text = (
    "This table stores information regarding the finishers of the Boston Marathon of 2015, 2016 and 2017.\n"
    "Description of this table was taken from the metadata of the original files obtained from Kaggle."
    "It's important to highlight that the Boston Marathon is the oldest marathon run in the US as it is the only" 
    "marathon (other than olympic trails) that most of the participants have to qualify to participate.\n"
    "For the professional runners, it's a big accomplishment to win the marathon."
    " For most of the other participants, it's an honor to be part of it.\n"
    "Content:\n\nIt contains the name which is the name of the runner formated as '[First Name],[Last Name]', it also contains other fileds which names are self descriptive\n\n"
    "The half marathon time is the time at kilometer 21, and complete marathon time is overall time."
    "Acknowledgements:\n\nData was scrapped from the official marathon website - http://registration.baa.org/2017/cf/Public/iframe_ResultsSearch.cfm\n\n"
    "Link: https://www.kaggle.com/datasets/rojour/boston-results\n"
    "Author: Rojour https://www.kaggle.com/rojour"
)

table_node_mapping = SQLTableNodeMapping(sql_database)
table_schema_objs = [
    (SQLTableSchema(table_name="marathon_results", context_str=marathon_results_text))
]


obj_index = ObjectIndex.from_objects(
    table_schema_objs,
    table_node_mapping,
    index_cls = VectorStoreIndex,
    storage_context=storage_context,
    embed_model=Settings.embed_model,
    show_progress=True,
)