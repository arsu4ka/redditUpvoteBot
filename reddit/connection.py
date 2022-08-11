from reddit.reddit_action import RedditProfile
from loguru import logger


def read_txt(path: str) -> list:
    res = []
    with open(path, "r") as file:
        for line in file.readlines():
            if line.strip() == "":
                return res
            cred_list = line.strip().split(":")
            res.append({
                "username": cred_list[0],
                "password": cred_list[1],
                "host": cred_list[2],
                "port": cred_list[3]
            })
    return res


def run(fromFile: bool, data: str, reddit_post: str):
    if fromFile:
        try:
            cred = read_txt(data)
        except:
            raise "Invalid file path!"
    else:
        try:
            tempList = data.split(":")
            cred = [{
                "username": tempList[0],
                "password": tempList[1],
                "host": tempList[2],
                "port": tempList[3]  
            }]
        except:
            raise "Invalid credentials input!"
    
    for acc in cred:
        try:
            profile = RedditProfile(
                username=acc["username"],
                password=acc["password"],
                proxy={"host": acc["host"], "port": acc["port"]}
            )
            profile.login()
            profile.upvote(reddit_post=reddit_post)
        except:
            continue
    
    logger.info("Actions completed! Check previous output to understand if everything went successfully.")

    