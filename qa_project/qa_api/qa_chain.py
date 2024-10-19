import os
from dotenv import load_dotenv
from django.conf import settings
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.docstore.document import Document

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable")

# Load the document
data_file_path = os.path.join(settings.BASE_DIR, 'qa_api', 'data', 'data.txt')

# Read the file content
with open(data_file_path, 'r', encoding='windows-1251') as file:
    content = file.read()

# Create a Document object
document = Document(page_content=content)

# Split the document into chunks
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents([document])

# Create embeddings and load them into the vector store
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(texts, embeddings)

# Create a retriever from the vector store
retriever = vectorstore.as_retriever()

# Initialize the language model
llm = ChatOpenAI(temperature=0, model='ft:gpt-3.5-turbo-0125:personal::AK3ZlPRg')

# Create the RAG chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True
)

def ask_question(question):
    result = qa_chain({"query": question})
    return result["result"]