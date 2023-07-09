from azure.identity import DefaultAzureCredential
from azure.monitor.ingestion import LogsIngestionClient
from azure.core.exceptions import HttpResponseError

credential = DefaultAzureCredential()

import logging, sys

import settings

logger = logging.getLogger('azure.monitor.ingestion')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)

if settings.AZURE_MONITOR_ENDPOINT:
    logs_client = LogsIngestionClient(credential=credential, endpoint=settings.AZURE_MONITOR_ENDPOINT, logging_enable=True)
    
def ingest_secrets_about_to_expire(logs):
    rule_id = settings.AZURE_MONITOR_RULE_ID
    try:
        logs_client.upload(rule_id, stream_name=settings.AZURE_MONITOR_STREAM_NAME, logs=logs)
    except HttpResponseError as e:
        print(f"Upload failed: {e}")