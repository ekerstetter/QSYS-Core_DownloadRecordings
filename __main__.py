import requests
from pathlib import PurePath


def main():
    
    #Configure these
    username = "ECP"
    password = "ambu&kZLmXA%"
    core_IP = "10.101.55.48"
    
    
    cred_json = {
        "username": username,
        "password": password
    }

    # Get Token
    r = requests.post(f"https://{core_IP}/api/v0/logon",
                      json=cred_json, verify=False)
    token = r.json()["token"]

    # List All Recordings in Directory
    headers_json = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    r = requests.get(
        f"https://{core_IP}/api/v0/cores/self/media/Recordings", headers=headers_json, verify=False)
    list_of_recordings = [sub['path'] for sub in r.json()]
    headers_json = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/octet-stream"
    }
    headers_delete_json = {
        "Authorization": f"Bearer {token}"
    }

    # Loop through list_of_recordings and download, then delete files.
    for file in list_of_recordings:

        with requests.get(f"https://{core_IP}/api/v0/cores/self/media/{file}", headers=headers_json, verify=False, stream=True) as r:
            with open(PurePath(file), 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        requests.delete(
            f"https://{core_IP}/api/v0/cores/self/media/{file}", headers=headers_delete_json, verify=False)


if __name__ == "__main__":
    main()
