import os
import glob
import logging
from dotenv import load_dotenv
load_dotenv(override=True)

# Document loaders and splitters
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Azure components import
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores import AzureSearch

# setup logging
logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("indexer")

def index_docs():
    '''
    Reads the PDFs, chunks them, and upload them Azure AI Search
    '''

    # define paths, we look for data folder
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_folder = os.path.join(current_dir,"../../backend/data")

    # Check the environment variables
    logger.info("="*60)
    logger.info("Environment Configuration CHeck:")
    logger.info(f"AZURE_OPENAI_ENDPOINT : {os.getenv('AZURE_OPENAI_ENDPOINT')}")
    logger.info(f"AZURE_OPENAI_API_VERSION : {os.getenv('AZURE_OPENAI_API_VERSION')}")
    logger.info(f"Embedding Deployment : {os.getenv('AZURE_OPENAI_EMBEDDING_DEPLOYMENT' , 'text-embedding-3-small')}")
    logger.info(f"AZURE_SEARCH_ENDPOINT : {os.getenv('AZURE_SEARCH_ENDPOINT')}")
    logger.info(f"AZURE_SEARCH_INDEX_NAME : {os.getenv('AZURE_SEARCH_INDEX_NAME')}")
    logger.info("="*60)

    # validate the required environment variables
    required_vars = [
        "AZURE_OPENAI_ENPOINT",
        "AZURE_OPENAI_API_KEY",
        "AZURE_SEARCH_ENDPOINT",
        "AZURE_SEARCH_API_KEY",
        "AZURE_SEARCH_INDEX_NAME"
    ]

    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        logger.error(f"Missing required environment variavles: {missing_vars}")
        logger.error("Please check your .env file and ensure all the variables are set")
        return
    
    # Intialize the embedding model : turns text into vectors
    try:
        logger.info("Initializing Azure Open AI Embeddings......")
        embeddings = AzureOpenAIEmbeddings(
            azure_deployment = os.getenv('AZURE_OPENAI_EMBEDDING_DEPLOYMENT', 'text-embedding-3-small')
            azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key = os.getenv("AZURE_OPENAI_API_KEY"),
            openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01"),
        )
        logger.info("Embeddings model initialized succesfully")
    except Exception as e:
        logger.error(f"Failed to initialize embeddings: {e}")
        logger.error("Please verify your Azure OpenAI deployment name and endpoint.")
        return

        # Initialize the Azure Search
    try:
        logger.info("Initializing Azure AI SEARCH vector store......")
        embeddings = AzureOpenAIEmbeddings(
            azure_search_endpoint = os.getenv('AZURE_SEARCH_ENDPOINT')
            azure_search_key = os.getenv("AZURE_SEARCH_API_KEY"),
            index_name = index_name,
            embedding_function = embeddings.embed_query,
        )
        logger.info("Vector Store intialized for index: {index_name}")
    except Exception as e:
        logger.error(f"Failed to initialize Azure Search: {e}")
        logger.error("Please verify your Azure search endpoint, API Key and index name.")
        return
    
    # Find PDF files
    pdf_files = glob.glob(os.path.join(data_folder), "*.pdf")
    if not pdf_files:
        logger.warning(f"No PDFs found in {data_folder}. Please add files.")