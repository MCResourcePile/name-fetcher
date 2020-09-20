import os, sys, json, requests
from optparse import OptionParser

def main(directory, options):
    uuids = []

    for root, dirs, files in os.walk(directory):
        for f in files:
            if f.lower().endswith((".json")):
                filename = f
                f = os.path.join(root, f)
                with open(f, "r") as f:
                    json_data = f.read()
                data = json.loads(json_data)
                if "data" in data:
                    print("Searching for UUIDs in " + filename, flush=True)
                    maps = data["data"]["maps"]
                    for map in maps:
                        for author in map["authors"]:
                            if author["uuid"] not in uuids:
                                uuids.append(author["uuid"].replace("-", ""))
    count = str(len(uuids))
    print(count + " UUIDS found\n", flush=True)
                                
    api = "https://api.ashcon.app/mojang/v2/user/"
    names = dict()
    
    #uuids = uuids[0:5]

    for i, uuid in enumerate(uuids):
        print("Fetching username for " + uuid + " (" + str(i+1) + " of " + count + ")", flush=True)
        r = requests.get(api + uuid)
        if "username" in r.json():
            username = r.json()["username"]
            names.update({uuid: username})

    with open("uuids.json", "w") as out:
        json.dump(names, out, indent=4)
    
if __name__ == "__main__":
    usage = "usage: %prog <dir>"
    parser = OptionParser(usage = usage)
    (options, args) = parser.parse_args()
    
    if len(sys.argv) == 1:
        parser.error("No directory specified")
        
    directory = sys.argv[1]
    directory = os.path.normpath(directory)
    if not os.path.exists(directory):
        parser.error("No such directory as " + directory)
        
    main(directory, options)
    
    sys.exit(0)
    