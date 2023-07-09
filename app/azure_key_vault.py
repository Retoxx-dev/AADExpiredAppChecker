from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

from azure.core.exceptions import ResourceNotFoundError, ClientAuthenticationError

import datetime

import settings

credential = DefaultAzureCredential()

if settings.AZURE_KEYVAULT_URI:
    kv_client = SecretClient(credential=credential, vault_url=settings.AZURE_KEYVAULT_URI)  

def create_secret(secret_name: str, secret_value: str, expires_on: datetime):
    secret_name = secret_name.replace(" ", "-").replace("_", "-")
    try:
        print(f"Creating secret {secret_name} that expires on {expires_on}")
        kv_client.set_secret(secret_name, secret_value, expires_on=expires_on)
        print(f"Secret {secret_name} created")
    except ClientAuthenticationError:
        print(f"Could not authenticate to Key Vault")
    except Exception as e:
        print(f"Error: {e}")
        