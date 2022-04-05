import requests
import json
import os
from collections import Counter
import shutil
import stat
# pull json from the API and build a table

def main():
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
            repo = Repository(item['name'], str(item['description']), item['html_url'])
            
            f.write("|" + repo.name + "|" + repo.description + "|\n")

            gitdir = clone_git_repo(repo)
            
            # find count of the different files extensions in repo
            counter = Counter()

            for root, dirs, files in os.walk(".\\" + gitdir):
                # if string contains .
                for file in files:
                    # check if file is hidden
                    if "." in file and not file.startswith("."):
                        extension = file.split(".")[-1]
                        counter[extension] += 1

            # sort counter by size descending
            sorted_counter = sorted(counter.items(), key=lambda x: x[1], reverse=True)
            f.write("Within the repo, \"" + repo.name +"\", the most common file extensions are:\n")
            for item in sorted_counter:
                f.write(item[0] + ": " + str(item[1]) + "\n")

            delete_repo(gitdir)

class Repository:
    def __init__(self, name, description, giturl):
        self.name = name
        self.description = description
        self.giturl = giturl

def clone_git_repo(repo: Repository) -> str:
    os.system("git clone " + repo.giturl)
    delete_hidden_git_dir(repo.name)
    return repo.name

def get_git_dir() -> str:
    for dir in os.listdir("."):
        if os.path.isdir(dir):
            return dir
            break

def delete_hidden_git_dir(gitdir):
    if os.path.isdir(gitdir):
        # making the read-only files writeable
        for root, dirs, files in os.walk(".\\" + gitdir):  
            for dir in dirs:
                os.chmod(os.path.join(root, dir), stat.S_IWRITE)
            for file in files:
                os.chmod(os.path.join(root, file), stat.S_IWRITE)
        
        # the actual recursive delete
        shutil.rmtree(".\\"+gitdir+"\\.git", ignore_errors=True)

def delete_repo(gitdir):
    for gitdir in os.listdir("."):
        if os.path.isdir(gitdir):
            print("deleting:", gitdir)
            shutil.rmtree(".\\"+gitdir, ignore_errors=True)   

if __name__ == "__main__":
    main()
