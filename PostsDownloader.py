#work in progress, some bugs

import praw
import time
import urllib
import urllib2
import sys
import imghdr
import os
import random

class PostsDownloader(object):

    def __init__(self):
        self.r = praw.Reddit(user_agent='postsdownloader')
        self.all_posts = []
        os.chdir(os.path.dirname(os.path.realpath(__file__)))

    def download(self, website, extra=None):
        #reddit images
        if website == "reddit":
            subreddit = extra
            submissions = self.r.get_subreddit(subreddit).get_top(limit=5)
            for submission in submissions:
                if submission.is_self is False and urllib.urlopen(submission.url).getcode() == 200:
                    #imgur submissions
                    if "imgur.com" in submission.domain:
                        image_id = submission.url.split("/")[-1]
                        if "jpg" in image_id:
                            submission_url = "http://i.imgur.com/" + image_id
                            self.all_posts.append([submission.title, submission_url, "robot/reddit/" + subreddit])
                        elif "png" in image_id:
                            submission_url = "http://i.imgur.com/" + image_id
                            self.all_posts.append([submission.title, submission_url, "robot/reddit/" + subreddit])
                        elif "gif" in image_id:
                            submission_url = "http://i.imgur.com/" + image_id
                            self.all_posts.append([submission.title, submission_url, "robot/reddit/" + subreddit])
                        else:
                            url = "http://i.imgur.com/" + image_id + ".jpg"
                            image = "img.jpg"
                            urllib.urlretrieve(url, image)
                            image_extension = imghdr.what(image)
                            if image_extension == "jpeg":
                                submission_url = "http://i.imgur.com/" + image_id + ".jpg"
                                self.all_posts.append([submission.title, submission_url, "robot/reddit/" + subreddit])
                            elif image_extension == "png":
                                submission_url = "http://i.imgur.com/" + image_id + ".png"
                                self.all_posts.append([submission.title, submission_url, "robot/reddit/" + subreddit])
                            elif image_extension == "gif":
                                submission_url = "http://i.imgur.com/" + image_id + ".gif"
                                self.all_posts.append([submission.title, submission_url, "robot/reddit/" + subreddit])
                            else:
                                print(submission.url + " was not uploaded.")
                            os.remove(image)
                    #livememe submissions
                    elif "livememe.com" in submission.domain:
                        submission_url = submission.url
                        self.all_posts.append([submission.title, submission_url, "robot/livememe"])
                    #minus submissions
                    elif "i.minus.com" in submission.domain:
                        submission_url = submission.url
                        self.all_posts.append([submission.title, submission_url, "robot/minus"])
                    #other submissions
                    else:
                        url = submission.url
                        image = "img.jpg"
                        urllib.urlretrieve(url, image)
                        image_extension = imghdr.what(image)
                        if image_extension == "jpeg":
                            submission_url = submission.url
                            self.all_posts.append([submission.title, submission_url, "robot/other"])
                        elif image_extension == "png":
                            submission_url = submission.url
                            self.all_posts.append([submission.title, submission_url, "robot/other"])
                        elif image_extension == "gif":
                            submission_url = submission.url
                            self.all_posts.append([submission.title, submission_url, "robot/other"])
                        else:
                            print(submission.url + " was not uploaded.")
                        os.remove(image)
        #9gag images
        elif website == "9gag":
            print("Downloading images from 9gag...")
        #websites that will not work with this application
        else:
            print("The website (" + website + ") you requested images from does not work with this application.")

    def save(self):
        random.shuffle(self.all_posts)
        for post in self.all_posts:
            print(post[1])
            urllib.urlretrieve(post[1], "image")
            image_ext = imghdr.what("image")
            os.rename("image", post[1].split("/")[-1].split(".")[0] + "." + image_ext)
        time.sleep(3)

posts = PostsDownloader()
posts.download("reddit", "AdviceAnimals")
#posts.download("reddit", "pics")
#posts.download("reddit", "funny")
#posts.download("reddit", "gifs")
#posts.download("9gag")
#9gag downloads not yet implemented
posts.save();
