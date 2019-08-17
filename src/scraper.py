import praw
import json
import os

class Scraper():

    def __init__(self):
        self.reddit        = None
        self.client_id     = "tdTIOW5-AuN68Q"
        self.client_secret = "0zrUdfbcn4AMFWSnUYhkUT7TVU8"
        self.user_agent    = "Python:emojify_bot:v1.0.0 (by /u/Blubfisch)"
        self.post_dir      = r"../posts/"

    def make_reddit_obj(self):

        self.reddit = praw.Reddit(client_id = self.client_id,
                                  client_secret = self.client_secret,
                                  user_agent = self.user_agent)
        return self.reddit

    def scrape(self, subreddit, limit = 1):

        for submission in self.reddit.subreddit(subreddit).top("all", limit = limit):
            post_id = submission.id
            
            if self.is_scraped(post_id): continue

            comments = self.deep_scrape_comments(submission)
            fpath = self.post_dir + post_id + ".txt"

            with open(fpath, "a+") as json_file:
                json.dump(comments, json_file)


    def deep_scrape_comments(self, submission, deep_replace = True):
        
        if deep_replace:
            # expand all "read more comments" tags
            submission.comments.replace_more(limit = None)

        comment_queue = submission.comments[:] # Seed with top-level
        comments = []
            
        while comment_queue:
            comment = comment_queue.pop(0)
            comment_dict = self.to_dict(comment, 
                    fields = ("id", "body", "ups"))

            comments.append(comment_dict)
            comment_queue.extend(comment.replies)
        return comments

    def to_dict(self, submission, fields):
        vars_dict = vars(submission)
        return {field:vars_dict[field] for field in fields}

    def set_post_dir(self, post_dir):
        self.post_dir = post_dir
        return

    def is_scraped(self, sub_id):
        if sub_id + ".txt" in os.listdir(self.post_dir):
            return True
        else:
            return False


