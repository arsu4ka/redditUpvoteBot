from reddit import syncProfile
from loguru import logger
import time, random


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
                "port": cred_list[3],
                "proxy_user": cred_list[4],
                "proxy_pass": cred_list[5]
            })
    return res


def sync_run(credentials, reddit_post, upvote, sleep_range):
    for acc in credentials:
        try:
            profile = syncProfile.RedditProfile(
                acc["username"],
                acc["password"],
                {"host": acc["host"], "port": acc["port"], "proxy_user": acc["proxy_user"], "proxy_pass": acc["proxy_pass"]}
            )
            profile.login()
            time.sleep(random.randrange(sleep_range[0], sleep_range[1]))
            profile.vote(reddit_post, upvote)
        except:
            continue


def async_run():
    pass
    

def run(fromFile: bool, data: str, reddit_post: str, upvote: bool, sleep_range: tuple, sync: bool = True):
    if fromFile:
        try:
            cred = read_txt(data)
        except:
            logger.error("Invalid file path!")
            return
    else:
        try:
            tempList = data.strip().split(":")
            for i in range(len(tempList)):
                tempList[i] = tempList[i].strip()
            cred = [{
                "username": tempList[0],
                "password": tempList[1],
                "host": tempList[2],
                "port": tempList[3] ,
                "proxy_user": tempList[4],
                "proxy_pass": tempList[5]
            }]
        except:
            logger.error("Invalid credentials input!")
            return
    
    sync_run(cred, reddit_post, upvote, sleep_range) if sync else async_run()

    logger.info("Actions completed! Check previous output to understand if everything went successfully.")
    
