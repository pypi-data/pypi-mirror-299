import variables
from MrLou_modules.Cyberark.cyberark_api import CyberArkAPI

cyberark_api = CyberArkAPI(variables)
credentials = cyberark_api.get_credentials()

if credentials:
    print(f"Username: {credentials['Username']}")
    print(f"Password: {credentials['Password']}")
    print(f"Password Change In Process: {credentials['PasswordChangeInProcess']}")
