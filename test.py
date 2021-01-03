import os
import json
from library import Resources
def updatePlugin():
    with open('selectedFile.json') as r:
        temp = json.load(r)
        fileSelected = temp['File']
    for item in os.listdir(fileSelected+'/plugins/'):
        if '.jar' or '.zip' in item:
            ResourceID = item.split('.')[0]
            ResourceDate = item.split('.')[2]
            for key in Resources.ResourceVersions(ResourceID, size=1000, sort="+releaseDate"):
                if key['releaseDate'] > int(ResourceDate):
                    ResourceDate = key['releaseDate']
                if ResourceDate == key['releaseDate']:
                    DownloadInfo = [key['resource'], key['id']]
            print(DownloadInfo)
updatePlugin()
