import requests
from stix2 import Filter, MemoryStore

def get_data_from_branch(domain):
    # Get the ATT&CK STIX data from MITRE/CTI
    url = "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/"
    stix_json = requests.get(f"{url}/{domain}/{domain}.json").json()
    return MemoryStore(stix_data=stix_json["objects"])

src = get_data_from_branch("enterprise-attack")

while True:
    # Prompt the user to enter a technique ID
    technique_id = input("Enter Technique ID: ")

    try:
        # Use the src MemoryStore object and the Filter 
        # object to query for attack-patterns with the given technique ID
        t_id = src.query([
            Filter("external_references.external_id", "=", technique_id),
            Filter("type", "=", "attack-pattern")
        ])[0]

        # Print information about the given technique id
        print(f"Type: {t_id['type']}")
        print(f"Technique ID: {t_id['external_references'][0]['external_id']}")
        print(f"Tactic Name: {t_id['kill_chain_phases'][0]['phase_name']}")
        print(f"Description: {t_id['description']}")

    except:
        # If no matching is found, print "Information not found!"
        print("Information not found!")