import logging
import os

from dotenv import load_dotenv


logger = logging.getLogger(__name__)
DEFAULT_LIMIT = 20

load_dotenv()
ELASTIC_SEARCH_SERVICE_URI = os.getenv("ELASTIC_SEARCH_SERVICE_URI")
if ELASTIC_SEARCH_SERVICE_URI is None:
    logger.error(
        "Update ELASTIC_SEARCH_SERVICE_URI to your cluster uri. Current value for ELASTIC_SEARCH_SERVICE_URI={"
        "ELASTIC_SEARCH_SERVICE_URI}")
    exit(-1)

# Password for the 'elastic' user generated by Elasticsearch
ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")
if ELASTIC_PASSWORD is None:
    logger.error(
        "Update ELASTIC_PASSWORD to your cluster uri. Current value for ELASTIC_PASSWORD={ELASTIC_PASSWORD}")
    exit(-1)


logger.info("Elastic Environment Variables received Successfully!")
