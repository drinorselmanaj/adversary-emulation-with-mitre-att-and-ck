from stix2 import Filter, MemoryStore

# Create a new MemoryStore object
src = MemoryStore()
# Load STIX data from the "enterprise-attack.json" 
# file into the MemoryStore object
src.load_from_file("enterprise-attack.json")

while True:
    # Prompt the user to enter a group ID
    group_id = input("Enter Group ID: ")

    try:
        # Use the src MemoryStore object and the Filter object 
        # to query with the given group ID
        g_id = src.query([
            Filter("external_references.external_id", "=", group_id)
        ])[0]

        # Print information about the object with the given group ID
        print(f"Aliases: {g_id['aliases']}")
        print(f"Description: {g_id['description']}")

    except:
        # If no matching is found, print "Information not found!"
        print("Information not found!")