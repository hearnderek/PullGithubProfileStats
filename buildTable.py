import requests
import json
import os
from collections import Counter
import shutil
import stat
# pull json from the API and build a table


url = "https://api.github.com/users/hearnderek/repos"
response = requests.get(url)
data = json.loads(response.text)

if os.path.exists("RepoInformation.md"):
    os.remove("RepoInformation.md")

# open file to write to
with open('RepoInformation.md', "w") as f:
    f.write("# Repo Information\n")

    f.write("| name | description |\n")
    f.write("|-|-|\n")
    for item in data:
        name = str(item['name'])
        description = str(item['description'])
        giturl = item['html_url']
        f.write("|" + name + "|" + description + "|\n")

        # clone each repo
        os.system("git clone " + giturl)

        # remove .git folder
        for gitdir in os.listdir("."):
            if os.path.isdir(gitdir):
                # making the read-only files writeable
                for root, dirs, files in os.walk(".\\" + gitdir):  
                    for dir in dirs:
                        os.chmod(os.path.join(root, dir), stat.S_IWRITE)
                    for file in files:
                        os.chmod(os.path.join(root, file), stat.S_IWRITE)
                
                # the actual recursive delete
                shutil.rmtree(".\\"+gitdir+"\\.git", ignore_errors=True)
        
        
        # find count of the different files extensions in repo
        counter = Counter()

        for gitdir in os.listdir("."):
            for root, dirs, files in os.walk(".\\" + gitdir):
                # if string contains .
                for file in files:
                    # check if file is hidden
                    if "." in file and not file.startswith("."):
                        extension = file.split(".")[-1]
                        counter[extension] += 1

        # sort counter by size descending
        sorted_counter = sorted(counter.items(), key=lambda x: x[1], reverse=True)
        f.write("Within the repo, \"" + name +"\", the most common file extensions are:\n")
        for item in sorted_counter:
            f.write(item[0] + ": " + str(item[1]) + "\n")

        # delete the repo
        for gitdir in os.listdir("."):
            if os.path.isdir(gitdir):
                print("deleting:", gitdir)
                shutil.rmtree(".\\"+gitdir, ignore_errors=True)
            

