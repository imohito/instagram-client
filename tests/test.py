from instagram_client import Instagram

Instagram.KEY = "" # do NOT ask me for the key
Instagram.DEVICEID = "00000000-0000-0000-0000-000000000000"

client = Instagram()
client.login("username", "password")
media_id = client.upload('test.jpg')
client.configure(media_id, "My caption")
