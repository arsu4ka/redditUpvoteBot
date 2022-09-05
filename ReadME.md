# Reddit Upvote Bot

A bot for mass reddit upvote action on a certaion post.

## Installation

Clone the repository using

```bash
git clone https://github.com/arsu4ka/redditUpvoteBot.git
```

or download it directly from github.

Then install all required packages:

```bash
pip install requirements.txt
```

## Usage

Main class is located at

```bash
./reddit/syncProfile.py
```

file.

If you want to use it with GUI interface you can just run

```bash
python3 manage.py
```

or interact directly with the GUI class using

```python
from reddit import App
```

import statement.

## Example of code

<b> Using RedditProfile class</b>

```python
from reddit import RedditProfile

# creating an instance of RedditProfile class
profile = RedditProfile(
    username="your_username",
    password="your_password",
    proxy = {"host": "your_proxy_host", "port": "your_proxy_port"}
)
# logging into account
profile.login()
# upvoting the post
profile.upvote(
    reddit_post="link_to_reddit_post"
)
```

<b>Using GUI through App class</b>

```python
from reddit import App

if __name__ == "__main__":
    app = App()
    app.mainloop()
```

<b>Using manage.py file</b>

```bash
python3 manage.py
```

## Note

If you use GUI App class or run program using manage.py file make sure to check the code at first in order to understand in which format your account data should be stored, otherwise something bad may happen.
