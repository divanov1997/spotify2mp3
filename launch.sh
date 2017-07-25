#!/bin/bash

# activate virtual environment
source spotify2mp3/bin/activate

# set spotify api variables
export SPOTIPY_CLIENT_ID='8a8fcf350f174bdc8fd015706c48176c'
export SPOTIPY_CLIENT_SECRET='5c79acf72e5241e6b4621405ab3ca7be'
export SPOTIPY_REDIRECT_URI='https://example.com/callback'

python script.py danilivanov.ivanov@gmail.com

deactivate
