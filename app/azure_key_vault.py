from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

from azure.core.exceptions import ClientAuthenticationError

import logging

import datetime

import settings

credential = DefaultAzureCredential()

if settings.AZURE_KEYVAULT_URI:
    kv_client = SecretClient(credential=credential, vault_url=settings.AZURE_KEYVAULT_URI)  

def create_secret(secret_name: str, secret_value: str, expires_on: datetime):
    secret_name = secret_name.replace(" ", "-").replace("_", "-")
    try:
        logging.info(f"Creating secret {secret_name} that expires on {expires_on}")
        kv_client.set_secret(secret_name, secret_value, expires_on=expires_on)
        logging.info(f"Secret {secret_name} created successfully")
    except ClientAuthenticationError:
        print(f"Could not authenticate to Key Vault")
    except Exception as e:
        print(f"Error: {e}")
        