from setuptools import setup, find_packages

setup(
	name='searchx',
	version='1.0.1',
	packages=find_packages(),
	install_requires=[
		"cloudscraper",
		"httpx",
		"bs4"
	],
	author='RedPiar',
	author_email='Regeonwix@gmail.com',
	description='SearchX is a powerful library for convenient searching.',
	long_description=open('README.md').read(),
	long_description_content_type='text/markdown',
	url='https://github.com/RedPiarOfficial/searchx/',
	classifiers=[
		'Programming Language :: Python :: 3',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
	],
	python_requires='>=3.8',
	keywords=[
		"search",
		"google",
		"bing",
		"x",
		"translation",
		"image-search",
		"image"
	],
)
