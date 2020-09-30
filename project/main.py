import settings
import user
import random

users = []

for c in range(settings.NUMBER_OF_USERS):
    u = user.User(settings.MAX_POSTS_PER_USER, settings.MAX_LIKES_PER_USER, settings.ADDRESS)
    users.append(u)

usercount = len(users)

posts = 10

for c in range(posts):
    users[random.randint(0,usercount-1)].create_post()

likes = 10

for c in range(likes):
    users[random.randint(0,usercount-1)].like_post()
