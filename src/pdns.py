# core
import json

# community
import requests

# custom
import bastille

PDNS_HOST = '192.168.130.25'
PDNS_API_PORT = 8081
PDNS_API_TOKEN = 'changeme'
PDNS_ZONE = 'kungfoo.local'
PDNS_API_URL_BASE = f'http://{PDNS_HOST}:{PDNS_API_PORT}/api/v1/servers'

def updateRecord(jail):
  print (f'pdns: update')

def addRecord(jail):
  print (f'pdns: add')
  url = PDNS_API_URL_BASE + f'/localhost/zones/{PDNS_ZONE}.'
  headers = {
    "X-API-Key": PDNS_API_TOKEN,
    "Content-Type": "application/json"
  }
  payload = {
    "rrsets": [{
      "name": f"{jail[bastille.JAIL_KEY_NAME]}.{PDNS_ZONE}.", 
      "type": "A", 
      "ttl": 600, 
      "changetype": "REPLACE", 
      "records": [{
        "content": jail[bastille.JAIL_KEY_IP], 
        "disabled": False
      }]
    }]
  }
  print (json.dumps(payload, indent=2))
  try:
    response = requests.patch(url, headers=headers, json=payload)
    response.raise_for_status()  # Raise an exception for bad status codes
  except Exception as err:
    print (f'ERROR: {err}')

def deleteRecord(jail):
  print (f'pdns: deleting {jail[bastille.JAIL_KEY_NAME]}.{PDNS_ZONE}.')
  url = PDNS_API_URL_BASE + f'/localhost/zones/{PDNS_ZONE}.'
  headers = {
    "X-API-Key": PDNS_API_TOKEN,
    "Content-Type": "application/json"
  }
  payload = {
    "rrsets": [{
      "name": f"{jail[bastille.JAIL_KEY_NAME]}.{PDNS_ZONE}.", 
      "type": "A", 
      "changetype": "DELETE"
    }]
  }
  try:
    response = requests.patch(url, headers=headers, json=payload)
    response.raise_for_status()  # Raise an exception for bad status codes
  except Exception as err:
    print (f'ERROR: {err}')

def updatePdns(jail):
  records = getRecord(jail[bastille.JAIL_KEY_NAME])
  if records is None:
    # error: ignore update
    return None

  # empty array: no matching record = add
  if len(records) == 0:
    return addRecord(jail)

  # update
  # pdns api update and add are the same
  addRecord(jail)
#  updateRecord(jail)

def getRecord(name):
  # Configuration
  url = PDNS_API_URL_BASE + f'/localhost/zones/{PDNS_ZONE}.' + \
    f'?rrset_name={name}.{PDNS_ZONE}.&rrset_type=A' 

  headers = {
    "X-API-Key": PDNS_API_TOKEN,
    "Content-Type": "application/json"
  }

  try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for bad status codes

    zone_data = response.json()

    ret = []
    if "rrsets" in zone_data:
      for rrset in zone_data["rrsets"]:
        if rrset["type"] == "A":
          if "records" in rrset:
            for record in rrset["records"]:
              ret.append(record['content'])
              # print(f"  - Content: {record['content']}, Disabled: {record['disabled']}")
    return ret

  except requests.exceptions.RequestException as e:
    print(f"Error getting zone records: {e}")
    if response is not None:
      print(f"Response status code: {response.status_code}")
      try:
        print(f"Response body: {response.json()}")
      except json.JSONDecodeError:
        print(f"Response body: {response.text}")

  return None