from instagrapi import Client

username = "poetrypoetryfever"
password = "YOlajideAgarau1994@"

cl = Client()
cl.login(username, password)
cl.dump_settings(f"insta_session_{username}.json")
print(f"Session exported to insta_session_{username}.json") 