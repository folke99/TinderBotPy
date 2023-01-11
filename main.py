import json
import random
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

import tinder_api
import chatgpt_api
import models
import utils


def main():
    # Create instances of the APIs
    # tinder = tinder_api.TinderAPI()
    chatgpt = chatgpt_api.ChatGptAPI()

    # Works
    # r = chatgpt.generate_response("Are you there?")
    # print(r)
    # tinder.swipe_right()

    # @param: True gives matches with messages False gives without
    # r = tinder.get_matches(True)
    # print(r)

    # Get the list of matches
    # matches = tinder.get_matches()

if __name__ == "__main__":
    main()
