import names
import lorem
import requests
import random


class User:

    def __init__(self, max_posts, max_likes, address):
        self.max_posts = max_posts
        self.max_likes = max_likes
        self.address = address
        self.username = names.get_first_name() 
        self.password = 'StrongPassword'
        self.access_token = ''
        self.refresh_token = ''
        self.posts = 0
        self.likes = 0
        print('User creation: %s'%(self.username))
        self.register()
        self.auth()

    def auth(self):
        headers = {
            'Content-Type': 'application/json'
        }
        resp = requests.post(
            self.address + '/users/token',
            json = {
                'username': self.username,
                'password': self.password
            },
            headers=headers
        )

        if resp.status_code == 200:
            self.access_token = resp.json()['access']
            self.refresh_token = resp.json()['refresh']
            print('User authenticated')
        else:
            print('Authentication failed')
            print(resp.json())
            print(resp.text)

    def register(self):
        headers = {
            'Content-Type': 'application/json'
        }
        resp = requests.post(
            self.address + '/users',
            json = {
                'username':self.username,
                'password':self.password
            },
            headers=headers
        )
        if resp.status_code == 201:
            print('User created')
        else:
            print('Registration failed')
            print(resp.json())
            print(resp.text)

    def create_post(self):
        if self.posts < self.max_posts:
            headers = {
                'Authorization': 'Bearer %s'%(self.access_token),
                'Content-Type': 'application/json'
            }
            resp = requests.post(
                self.address + '/posts',
                json = {
                    'name': 'Random post',
                    'content': lorem.sentence()
                },
                headers=headers
            )
            if resp.status_code == 201:
                self.posts+=1
                print('Post created')
            else:
                print('Post creation failed')
        else:
            print('Post limit reached')

    def like_post(self):
        if self.likes < self.max_likes:
            headers = {
                'Authorization': 'Bearer %s'%(self.access_token)
            }
            post = random.randint(1,10)
            resp = requests.post(
                self.address + '/posts/like/' + str(post),
                headers=headers
            )
            if resp.status_code == 201:
                self.likes += 1
                print('Post %i liked!'%(post))
            else:
                print('Post like failed or post does not exist')
        else:
            print('Like limit reached')

    def dislike_post(self):
        headers = {
            'Authorization': 'Bearer %s'%(self.access_token)
        }
        post = random.randint(1,50)
        resp = requests.delete(
            self.address + '/posts/like/' + str(post),
            headers=headers
        )
        if resp.status_code == 204:
            self.likes -= 1
            print('Post %i disliked!'%(post))
        else:
            print('Post dislike failed or post does not exist')