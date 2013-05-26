from client import Instagram

client = Instagram()
client.login("", "")
media_id = client.upload('test.jpg')
client.configure(media_id, "My caption")
