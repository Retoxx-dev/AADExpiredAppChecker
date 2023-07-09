from azure.identity import DefaultAzureCredential
from msgraph.core import GraphClient

from datetime import datetime, timedelta
import logging
import json

import settings

credential = DefaultAzureCredential()
graph_client = GraphClient(credential=credential, logging_level=logging.DEBUG)

def get_filtered_applications():
    logging.info("Getting applications from Azure AD")
    applications = graph_client.get("/applications?$select=id,displayName,passwordCredentials")
    applications.raise_for_status()
    return applications.json()

def get_secrets_about_to_expire():
    logging.info(f"Getting secrets that expire in {settings.EXPIRE_DAYS} days")
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
                        logging.info(f"Secret {secret['displayName']} for {app['displayName']} expires in {time_diff} days")
    return expired_secrets

def create_new_app_secret(object_id, secret_name):
    now = datetime.now()
    calculated_expire_date = now + timedelta(days=settings.SECRET_EXPIRATION_DAYS)
    post_body = {
        "passwordCredential": {
            "displayName": secret_name,
            "endDateTime": calculated_expire_date.isoformat()
        }
    }
    result = graph_client.post(f"/applications/{object_id}/addPassword", data=json.dumps(post_body), headers={'Content-Type': 'application/json'})
    if result.status_code == 200:
        logging.info(f"Secret {secret_name} created successfully")
        return result.json()['secretText'], calculated_expire_date
    else:
        logging.fatal(f"Secret {secret_name} could not be created: {result.json()}")

def delete_old_app_secret(object_id, key_id):
    post_body = {
        "keyId": key_id
    }
    result = graph_client.post(f"/applications/{object_id}/removePassword", data=json.dumps(post_body), headers={'Content-Type': 'application/json'})
    if result.status_code == 204:
        logging.info(f"Secret with id of {key_id} for {object_id} deleted successfully")
    else:
        logging.fatal(f"Secret with id of {key_id} for {object_id} could not be deleted: {result.json()}")