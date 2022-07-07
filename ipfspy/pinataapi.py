# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/04_pinataapi.ipynb (unless otherwise specified).

__all__ = ['generate_apikey', 'list_apikeys', 'revoke_apikey', 'upload_file', 'upload_jsonfile', 'pin', 'unpin',
           'edit_hash', 'get_pinned_jobs', 'get_pinned_files', 'get_datausage']

# Cell
#hide
import requests
import json

# Cell
def generate_apikey(cred:str,#JWT
                    key_name:str, #Key name
                    pinlist:bool=False,#list pins
                    userPinnedDataTotal:bool=False, #total data stored
                    hashMetadata:bool=True, #metadata
                    hashPinPolicy:bool=False, #policy
                    pinByHash:bool=True, #pin cid
                    pinFileToIPFS:bool=True,#upload file to IPFS
                    pinJSONToIPFS:bool=True,#upload json to IPFS
                    pinJobs:bool=True,#see pin jobs
                    unpin:bool=True,#unpin ipfs cid
                    userPinPolicy:bool=True #establish pin policy

):

    url = "https://api.pinata.cloud/users/generateApiKey"

    payload = json.dumps({
      "keyName": key_name,
      "permissions": {
        "endpoints": {
          "data": {
            "pinList": pinlist,
            "userPinnedDataTotal": userPinnedDataTotal
          },
          "pinning": {
            "hashMetadata": hashMetadata,
            "hashPinPolicy": hashPinPolicy,
            "pinByHash": pinByHash,
            "pinFileToIPFS": pinFileToIPFS,
            "pinJSONToIPFS": pinJSONToIPFS,
            "pinJobs": pinJobs,
            "unpin": unpin,
            "userPinPolicy": userPinPolicy
          }
        }
      }
    })
    headers = {
      'Authorization': f'Bearer {creds}',
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response


# Cell
def list_apikeys(creds:str
):

    url = "https://api.pinata.cloud/users/apiKeys"

    payload={}
    headers = {
      'Authorization': f'Bearer {creds}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response


# Cell
def revoke_apikey(creds:str,
                  revoke_apikey:str
):
    url = "https://api.pinata.cloud/users/revokeApiKey"

    payload = json.dumps({
      "apiKey": revoke_apikey
    })
    headers = {
      'Authorization': f'Bearer {creds}',
      'Content-Type': 'application/json'
    }

    response = requests.request("PUT", url, headers=headers, data=payload)

    return response


# Cell
def upload_file(cred:str,#JWT key
                name:str, #filename
                fpaths:list, #filepaths
                metadata:dict, #metadata
                cid_version:str="1", #IPFS cid
                directory:bool=False #upload directory
):

    pinataMetadata = dict({"name":name,"keyvalues":{}})
    pinataMetadata["name"] = name
    pinataMetadata["keyvalues"].update(metadata)

    pinataOptions = dict({"cidVersion":cid_version,"directory":directory})


    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"

    payload={"pinataOptions":json.dumps(pinataOptions),"pinataMetadata":json.dumps(pinataMetadata)}

    if directory:
        print("feature is not ready yet")

    files=[('file',(name,open(fpaths,'rb'),'application/octet-stream'))]

    headers = {
      'Authorization': f'Bearer {creds}'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    return response

# Cell
def upload_jsonfile(cred:str,#JWT key
                name:str, #filename
                fpaths:list, #filepaths
                metadata:dict, #metadata
                cid_version:str, #IPFS cid
                directory:bool=False #upload directory
):

    url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"

    payload = json.dumps({
      "pinataOptions": {
        "cidVersion": cid_version
      },
      "pinataMetadata": {
        "name": name,
        "keyvalues": metadata
      },
      "pinataContent": {"file":fpaths}
    })
    headers = {
        'Authorization': f'Bearer {creds}',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response

# Cell
def pin(cred:str,#JWT key
        cid:str, #IPFS cid
        fn=None, #Name of file
        pinataMetadata=None #Add keys and values associated with IPFS CID
):

    url = "https://api.pinata.cloud/pinning/pinByHash"

    payload = json.dumps({
      "hashToPin": cid,
      "pinataMetadata": {
        "name": fn,
        "keyvalues": pinataMetadata
      }
    })
    headers = {
      'Authorization': f'Bearer {creds}',
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


# Cell
def unpin(cred:str,#JWT Key
          cid:str #IPFS CID
):

    url = f"https://api.pinata.cloud/pinning/unpin/{cid}"

    payload={}
    headers = {
      'Authorization': f'Bearer {cred}'
    }

    response = requests.request("DELETE", url, headers=headers, data=payload)

    print(response)

# Cell
def edit_hash(cred:str,#JWT Key
              cid:str, #IPFS CID
              name:str, #filename
              metadata=None #Add keys and values associated with IPFS CID
):

    url = "https://api.pinata.cloud/pinning/hashMetadata"

    pinataMetadata = dict({"name":name,"keyvalues":{}})
    pinataMetadata["keyvalues"].update(metadata)
    pinataMetadata["ipfsPinHash"] = cid

    payload = json.dumps(pinataMetadata)
    headers = {
      'Authorization': f'Bearer {cred}',
      'Content-Type': 'application/json'
    }

    response = requests.request("PUT", url, headers=headers, data=payload)

    return response


# Cell

def get_pinned_jobs(cred:str,# JWT Key
                    params=None # filtering pinned jobs
):

    '''
    'sort' - Sort the results by the date added to the pinning queue (see value options below)
    'ASC' - Sort by ascending dates
    'DESC' - Sort by descending dates
    'status' - Filter by the status of the job in the pinning queue (see potential statuses below)
    'prechecking' - Pinata is running preliminary validations on your pin request.
    'searching' - Pinata is actively searching for your content on the IPFS network. This may take some time if your content is isolated.
    'retrieving' - Pinata has located your content and is now in the process of retrieving it.
    'expired' - Pinata wasn't able to find your content after a day of searching the IPFS network. Please make sure your content is hosted on the IPFS network before trying to pin again.
    'over_free_limit' - Pinning this object would put you over the free tier limit. Please add a credit card to continue pinning content.
    'over_max_size' - This object is too large of an item to pin. If you're seeing this, please contact us for a more custom solution.
    'invalid_object' - The object you're attempting to pin isn't readable by IPFS nodes. Please contact us if you receive this, as we'd like to better understand what you're attempting to pin.
    'bad_host_node' - You provided a host node that was either invalid or unreachable. Please make sure all provided host nodes are online and reachable.
    'ipfs_pin_hash' - Retrieve the record for a specific IPFS hash
    'limit' - Limit the amount of results returned per page of results (default is 5, and max is 1000)
    'offset' - Provide the record offset for records being returned. This is how you retrieve records on additional pages (default is 0)
    '''

    base_url = 'https://api.pinata.cloud/pinning/pinJobs/'

    header = {'Authorization': f'Bearer {cred}'}

    response = requests.get(base_url, headers=header,params=params)

    return response

# Cell
def get_pinned_files(cred:str,# JWT Key
                     params=None # Filter returned pinned files
):

    '''
    Query Parameters = params

    hashContains: (string) - Filter on alphanumeric characters inside of pin hashes. Hashes which do not include the characters passed in will not be returned.
    pinStart: (must be in ISO_8601 format) - Exclude pin records that were pinned before the passed in 'pinStart' datetime.
    pinEnd: (must be in ISO_8601 format) - Exclude pin records that were pinned after the passed in 'pinEnd' datetime.
    unpinStart: (must be in ISO_8601 format) - Exclude pin records that were unpinned before the passed in 'unpinStart' datetime.
    unpinEnd: (must be in ISO_8601 format) - Exclude pin records that were unpinned after the passed in 'unpinEnd' datetime.
    pinSizeMin: (integer) - The minimum byte size that pin record you're looking for can have
    pinSizeMax: (integer) - The maximum byte size that pin record you're looking for can have
    status: (string) -
        * Pass in 'all' for both pinned and unpinned records
        * Pass in 'pinned' for just pinned records (hashes that are currently pinned)
        * Pass in 'unpinned' for just unpinned records (previous hashes that are no longer being pinned on pinata)
    pageLimit: (integer) - This sets the amount of records that will be returned per API response. (Max 1000)
    pageOffset: (integer) - This tells the API how far to offset the record responses. For example,
    if there's 30 records that match your query, and you passed in a pageLimit of 10, providing a pageOffset of 10 would return records 11-20.
    '''

    base_url = 'https://api.pinata.cloud/data/pinList?'

    header = {'Authorization': f'Bearer {cred}'}

    response = requests.get(base_url, headers=header,params=params)

    return response

# Cell
def get_datausage(cred:str,# JWT Key
                  params=None # Filter returned data usage statistics
):

    header = {'Authorization': f'Bearer {cred}'}

    base_url = 'https://api.pinata.cloud/data/userPinnedDataTotal'

    response = requests.get(base_url, headers=header,params=params)

    return response