from azure.identity import DefaultAzureCredential
from msgraph.core import GraphClient

from datetime import datetime, timedelta
import logging
import json

import settings

credential = DefaultAzureCredential()
graph_client = GraphClient(credential=credential, logging_level=logging.DEBUG)

def get_filtered_applications():
    applications = graph_client.get("/applications?$select=id,displayName,passwordCredentials")
    applications.raise_for_status()
    return applications.json()

def get_secrets_about_to_expire():
    expired_secrets = []
    applications = get_filtered_applications()
    if applications:
        for app in applications["value"]:
            if app['passwordCredentials']:
                for secret in app['passwordCredentials']:
                    password_expire_date_str = secret['endDateTime']

                    if "." in password_expire_date_str:
                        parsed_date = datetime.strptime(password_expire_date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
                    else:
                        parsed_date = datetime.strptime(password_expire_date_str, "%Y-%m-%dT%H:%M:%S%fZ")
                    
                    time_diff = (parsed_date.date() - datetime.now().date()).days
                            
                    if time_diff <= settings.EXPIRE_DAYS:
                        expired_secrets.append({"ApplicationId": app['id'], "Name": app['displayName'], 
                                                "SecretName": secret['displayName'], "ExpireDate": str(parsed_date.date()), 
                                                "DaysLeft": time_diff, "keyId": secret['keyId']})
            else:
                print(f"Application {app['displayName']} has no secrets")
    return expired_secrets

def create_new_app_secret(object_id, secret_name):
    now = datetime.now()
    calculated_expire_date = now + timedelta(days=settings.SECRET_EXPIRATION_DAYS)
    print(f"Setting new secret expiration date to {calculated_expire_date.date()}")
    post_body = {
        "passwordCredential": {
            "displayName": secret_name,
            "endDateTime": calculated_expire_date.isoformat()
        }
    }
    result = graph_client.post(f"/applications/{object_id}/addPassword", data=json.dumps(post_body), headers={'Content-Type': 'application/json'})
    if result.status_code == 200:
        print(f"Secret for {object_id} created successfully")
        return result.json()['secretText'], calculated_expire_date
    else:
        print(f"Secret for {object_id} could not be created: {result.json()}")

def delete_old_app_secret(object_id, key_id):
    print(f"Deleting old password for {object_id} with {key_id} key")
    post_body = {
        "keyId": key_id
    }
    result = graph_client.post(f"/applications/{object_id}/removePassword", data=json.dumps(post_body), headers={'Content-Type': 'application/json'})
    if result.status_code == 204:
        print("Secret deleted successfully")
    else:
        print(f"Secret for {object_id} could not be deleted: {result.json()}")