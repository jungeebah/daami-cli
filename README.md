# daami-cli
Cli for daamireview.com

## Requirement
To run the command will need to have a google APi Key. Contact the slack channel for the key.
For initial setup you will require an API key and project directory of daamireview.

## Installation
For installation (Use virtualenv if possible)
>virtualenv setup
```bash
virtualenv daami
source daami/bin/activate
# for windows
.\daami\bin\activate.ps1 
```
then install the package
```bash
pip install daami-cli
```

## Usage
For first time setup
```bash
daami-cli setup 
Project: (provide your daamireview folder path)
Api key: (the api key )
Tmdb key : (the tmdb key)
Author: (your author name)
```
Once done use review to create the review in _posts folder 
```bash
daami-cli review
Title: (article title)
Movie: (movie name being reviewed)
Language: (the language the movie is in)
Rating: (a floating num)
```



