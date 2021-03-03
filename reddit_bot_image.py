import praw
import os
import requests
import shutil
import time
from imgg import*
from tele_bot1 import send_to_telebot


def authenticate():
    print("Authenticating...")
    reddit = praw.Reddit(
        "batbot",
        user_agent="<YOUR USERNAME HERE> first reddit test bot v0.2" ## write your username here as the agent
    )
    print("Authenticated as {}\n".format(reddit.user.me()))
    return reddit


def image_download(image_url, filename):
    req = requests.get(image_url, stream=True)
    if req.status_code == 200:
        req.raw.decode = True
        final_url = imgbb_main(image_url) ## pass the url to upload
        return final_url
    else:
        print("FAILED!")
        return 1




def bot_search_url(reddit, subreddit, new_post, comments_replied_to):

    for comment in subreddit.comments():
        if "!cp" in comment.body and comment.id not in comments_replied_to:
            # print("String 'bat' found in {}".format(dir(comment)))
            # print("bat found in comment id: {} link: {} submission:{} permalink:{} link title: {} link permalink {}"
            # .format(comment.id,comment.link_url,comment.submission, comment.permalink, comment.link_title, comment.link_permalink))
            submission_id = comment.submission
            image_url = reddit.submission(submission_id).url
            filename = image_url.split("/")[-1]
            if any(extension in image_url for extension in ('.jpg', '.png', '.jpeg', '.gif')):
                print("Possible to download image_url --> {} --> {}\n".format(image_url, comment.link_title))
                final_url = image_download(image_url, filename)
                #comment.reply(final_url)
                if final_url == 1:
                    with open('saved_comments.txt', 'a') as f:
                        f.write(comment.id+"\n")
                    return
                else:
                    #print("Replied to comment with {}\n".format(final_url))
                    send_to_telebot(final_url, comment.link_title)
                    with open('saved_comments.txt', 'a') as f:
                        f.write(comment.id+"\n")
                        #comments_replied_to = get_saved_comments() ## to read the file once so that we can search the id again in next loop

            else:
                print("Invalid Image --> {} --> {}\n".format(image_url, comment.link_permalink))
                with open('saved_comments.txt', 'a') as f:
                    f.write(comment.id+"\n")



def get_saved_comments():
    if not os.path.isfile("saved_comments.txt"):
        comments_replied_to = []
    else:
        with open("saved_comments.txt", 'r') as f:
            comments_replied_to = f.read()
            comments_replied_to = comments_replied_to.split("\n")
            comments_replied_to = list(filter(None, comments_replied_to))
    #print(comments_replied_to)
    return comments_replied_to

def main():
    reddit = authenticate()

    while True:
        sub_list = ['test', 'memes','funny', 'blursedimages']
        for i in sub_list:
            print(i)
            subreddit = reddit.subreddit(i)
            new_post = subreddit.new()
            comments_replied_to = get_saved_comments()
            print("Saved ID's: {}".format(comments_replied_to))
            bot_search_url(reddit, subreddit, new_post, comments_replied_to)
            time.sleep(3)


if __name__ == "__main__":
    main()
