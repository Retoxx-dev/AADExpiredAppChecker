import os

print("----------------- INITIALIZING --------------------")
#################################################################
# GENERAL
#################################################################
EXPIRE_DAYS = int(os.getenv("EXPIRE_DAYS", 10))
print(f"Setting EXPIRE_DAYS to {EXPIRE_DAYS}")
SECRET_EXPIRATION_DAYS = int(os.getenv("SECRET_EXPIRATION_DAYS", 30))
print(f"Setting SECRET_EXPIRATION_DAYS to {SECRET_EXPIRATION_DAYS}")

#################################################################
# AZURE IDENTITY
#################################################################
AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID", "")
AZURE_CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET", "")

#################################################################
# AZURE KEY VAULT
#################################################################
AZURE_KEYVAULT_URI = os.getenv("AZURE_KEYVAULT_URI")
print(f"Setting AZURE_KEYVAULT_URI to {AZURE_KEYVAULT_URI}")

#################################################################
# AZURE MONITOR
#################################################################
AZURE_MONITOR_ENDPOINT = os.getenv("AZURE_MONITOR_ENDPOINT")
AZURE_MONITOR_RULE_ID = os.getenv("AZURE_MONITOR_RULE_ID")
AZURE_MONITOR_STREAM_NAME = os.getenv("AZURE_MONITOR_STREAM_NAME")
if AZURE_MONITOR_ENDPOINT and AZURE_MONITOR_RULE_ID and AZURE_MONITOR_STREAM_NAME:
    print(f"Setting AZURE_MONITOR Environment Variables")

#################################################################
# SCRIPT BEHAVIOUR
#################################################################
SCRIPT_BEHAVIOUR = os.getenv("SCRIPT_BEHAVIOUR", "local")
if SCRIPT_BEHAVIOUR == "azuremonitor":
    print("Setting SCRIPT_BEHAVIOUR to azuremonitor")
    if not AZURE_MONITOR_ENDPOINT:
        raise ValueError("AZURE_MONITOR_ENDPOINT must be set if SCRIPT_BEHAVIOUR=azuremonitor")
    if not AZURE_MONITOR_RULE_ID:
        raise ValueError("AZURE_MONITOR_RULE_ID must be set if SCRIPT_BEHAVIOUR=azuremonitor")
    if not AZURE_MONITOR_STREAM_NAME:
        raise ValueError("AZURE_MONITOR_STREAM_NAME must be set if SCRIPT_BEHAVIOUR=azuremonitor")

if SCRIPT_BEHAVIOUR == "keyvault":
    print("Setting SCRIPT_BEHAVIOUR to keyvault")
    if not AZURE_KEYVAULT_URI:
        raise ValueError("AZURE_KEYVAULT_URI must be set if SCRIPT_BEHAVIOUR=keyvault")

CREATE_NEW_SECRET = os.getenv("CREATE_NEW_SECRET")
if CREATE_NEW_SECRET not in ["true", "false"]:
    raise ValueError("CREATE_NEW_SECRET must be set to true or false")

DELETE_OLD_SECRET = os.getenv("DELETE_OLD_SECRET")
if DELETE_OLD_SECRET not in ["true", "false"]:
    raise ValueError("DELETE_OLD_SECRET must be set to true or false")


if SCRIPT_BEHAVIOUR not in ["keyvault", "azuremonitor", "local"]:
    raise ValueError("SCRIPT_BEHAVIOUR must be set to keyvault, azuremonitor or local")
    
print("---------------------------------------------------")