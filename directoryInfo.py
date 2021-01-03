import os
import time
import re
class directoryChecks():
    F = 50
    def directoryScan(self):
        print(self.fileSelected)
        for i in os.listdir(self.fileSelected):
            if i.startswith(("Spigot", "Bukkit", "Paper")):
                print(i)
                return(True)
            else:
                pass
class directoryGrab():
    def DirectorySearchForJar(self):
        for i in os.listdir(self.fileSelected):
            if i.startswith(("Spigot", "Bukkit", "Paper")):
                return(i)
            else:
                print(i)
class directoryChange():
    def eulaTrue(self):
        while not os.path.exists(f'{self.fileSelected}/eula.txt'):
            time.sleep(5)
        with open(f'{self.fileSelected}/eula.txt', 'r+') as f:
            text = f.read()
            text = re.sub('eula=false', 'eula=true', text)
            f.seek(0)
            f.write(text)
            f.truncate()
class directoryStore():
    def jsonFileSelected(self):
        w = '{"File":"'+self.fileSelected+'"}'
        with open('selectedFile.json', 'w') as f:
            f.write(w)
    def jsonServerSettings(self):
        w = '{"File":"'+self.fileSelected+'","xmxLineRam":"'+self.xmxLineRamText+'","xmxRamUnit":"'+self.xmxRamUnitText+'","xmsLineRam":"'+self.xmsLineRamText+'","xmsRamUnit":"'+self.xmsRamUnitText+'"}'
        with open('selectedFile.json', 'w') as f:
            f.write(w)