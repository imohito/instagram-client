Instagram-client
================

An instagram client to upload pictures on Instagram. 

This library is directly inspired from the official iOS Instagram app, by reverse engineering.

## Install

	python setup.py install

or

	pip install -e git+https://acoomans@bitbucket.org/acoomans/instagram-client.git#egg=Package


## Usage

Before anything, you will need the key and a device id. 
**Do NOT ask me for the key.**

First, import the client:

	from instagram_client import Instagram

Define the key and device id to user:

	Instagram.KEY = "" # do NOT ask me for the key 
	Instagram.DEVICEID = "00000000-0000-0000-0000-000000000000"

Now login and upload:

	client = Instagram()
	client.login("username", "password")
	media_id = client.upload('test.jpg')
	
For a picture to be fully available, you need to "configure" it. You can also add a caption during this step:
	
	client.configure(media_id, "My caption")


# Tests

Run the tests with:

	cd tests
	python test.py