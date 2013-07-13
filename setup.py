from setuptools import setup

config = {
	'name': 'instagram-client',
	'version': '0.1',
	'description': 'Upload pictures to instagram',
	'license': 'LICENSE.txt',
	'url': 'https://bitbucket.org/acoomans/instagram-client',
	'author': 'Arnaud Coomans',
	'install_requires': ['requests'],
	'packages': ['instagram_client'],
}

setup(**config)