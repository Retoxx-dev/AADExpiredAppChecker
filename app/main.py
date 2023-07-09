import settings
import azure_key_vault as keyvault
import app_registration as app_reg

        
def main():
    expired_secrets = app_reg.get_secrets_about_to_expire()
    
    if expired_secrets:
        for secret in expired_secrets:
            if settings.DELETE_OLD_SECRET == "true":
                app_reg.delete_old_app_secret(secret['ApplicationId'], secret['keyId'])
            if settings.CREATE_NEW_SECRET == "true":
                new_secret = app_reg.create_new_app_secret(secret['ApplicationId'], secret['SecretName'])
            if settings.SCRIPT_BEHAVIOUR == "keyvault":
                keyvault.create_secret(f"{secret['Name']}-{secret['SecretName']}", new_secret[0], new_secret[1])
    else:
        print("No secrets to update")
               
if __name__ == "__main__":
    main()