import openai
import os
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader, DirectoryLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain_community.document_loaders import AmazonTextractPDFLoader


# Set the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set AWS region
os.environ["AWS_DEFAULT_REGION"] = "us-west-1"

loader = AmazonTextractPDFLoader(
    "s3://test123pdf4langchain/Starting Out with Java_ Early O - Tony Gaddis.pdf"
)
documents = loader.load()
print(f"Number of documents loaded: {len(documents)}")


# # Load the custom dataset
# loader = DirectoryLoader("mydata/")
# documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

# Embed the documents and store them in a vector database
embeddings = OpenAIEmbeddings(openai_api_key=openai.api_key)
docsearch = Chroma.from_documents(texts, embeddings)

# Create the ConversationalRetrievalChain
llm = OpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"))
chain = ConversationalRetrievalChain(
    llm=llm,
    retriever=docsearch.as_retriever(search_kwargs={"k": 1}),
    use_memory=True,  # Enable LLM to use its own knowledge
    use_doc=True,  # Enable usage of document retrieval
)


# Create the ConversationalRetrievalChain
llm = OpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"))
# chain = ConversationalRetrievalChain(
#     llm=llm,
#     retriever=docsearch.as_retriever(search_kwargs={"k": 1}),
#     use_memory=True,  # Enable LLM to use its own knowledge
#     use_doc=True,  # Enable usage of document retrieval
# )

chain = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(model="gpt-3.5-turbo"),
    retriever=docsearch.as_retriever(search_kwargs={"k": 1}),
)


# Function to handle conversational interactions
def converse(chain, max_history=5):
    chat_history = []
    while True:
        query = input("Prompt: ")
        if query.lower() in ["quit", "q", "exit"]:
            break

        # Call the chain with the user's query and chat history
        result = chain({"question": query, "chat_history": chat_history})
        print(result["answer"])

        # Append to chat history and maintain its size
        chat_history.append((query, result["answer"]))
        if len(chat_history) > max_history:  # Maintain chat history size
            chat_history.pop(0)


# Run the conversational interaction function
if __name__ == "__main__":
    converse(chain)
