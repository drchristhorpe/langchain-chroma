from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma

import toml
import os

# load config
config = toml.load('config.toml')

# set env vars for openai
os.environ["OPENAI_API_KEY"] = config["OPENAI_API_KEY"]

# set the persist directory to the value in the config
persist_directory = config["PERSIST_DIR"]

# create the embedding function
embedding = OpenAIEmbeddings()


# Now we can load the persisted database from disk, and use it as normal. 
vectordb = Chroma(persist_directory=persist_directory, 
                  embedding_function=embedding)

# create the retriever
retriever = vectordb.as_retriever()

# query ChromaDB
query = "What are T follicular helper cells?"
print ('Searching')
docs = retriever.get_relevant_documents(query)



# create the retriever
retriever = vectordb.as_retriever(search_kwargs={"k": 2})

print (retriever.search_type)

# create the chain to answer questions 
qa_chain = RetrievalQA.from_chain_type(llm=OpenAI(), 
                                  chain_type="stuff", 
                                  retriever=retriever, 
                                  return_source_documents=True)



def process_llm_response(llm_response, query):
    """
    This is a function to process the response from the LLM

    Args:
        llm_response (dict): the response from the LLM
        query (str): the query that was sent to the LLM

    Returns:
        None
    """
    print ('')
    print(query)
    print('')
    print(llm_response['result'])
    print('\n\nSources:')
    for source in llm_response["source_documents"]:
        if llm_response["source_documents"] is not None:
            print(source.metadata['source'])
    pass


# full example
llm_response = qa_chain(query)
print (process_llm_response(llm_response, query))


