import random
import threading
import time

from dotenv import load_dotenv
load_dotenv()

import tinder_api
import chatgpt_api
from models import Match

# Create instances of the APIs
tinder = tinder_api.TinderAPI()
chatgpt = chatgpt_api.ChatGptAPI()
threads = []


def create_match_objects():
    matches = []
    # Create Match objects for each match
    for match in tinder.get_matches_api(True):
        matches.append(Match(match_id=match["match_id"],
                             name=match["name"],
                             last_activity_date=match["last_active"],
                             tinder=tinder,
                             chatgpt=chatgpt))
    return matches


def start_match_threads(matches):
    # Use a thread for each match to check for new messages concurrently
    for match in matches:
        t = threading.Thread(target=match.wait_for_message)
        t.start()
        threads.append(t)


def add_match_to_threads(match, threads):
    t = threading.Thread(target=match.wait_for_message)
    t.start()
    threads.append(t)


# @param ratio: 0 - 100. 0 = 0% chance of swiping right. 100 = 100% chance of swiping right.
def auto_swipe(ratio=70):
    while True:
        rand = random.randint(0, 100)
        print("random: " + str(rand))
        if rand < ratio:
            print("swiping right")
            res = tinder.swipe_right_api()
        else:
            print("swiping left")
            tinder.swipe_left_api()
            res = False

        if res:
            if res["match"]:
                latest_match = tinder.get_matches_api(False)[0]
                match = Match(match_id=latest_match["match_id"],
                                     name=latest_match["name"],
                                     last_activity_date=latest_match["last_active"],
                                     tinder=tinder,
                                     chatgpt=chatgpt)
                match.message("Hej hej")
                add_match_to_threads(match)

            if res["likes_left"] == 0:
                print("no more likes left")
                time.sleep(14400)  # 4 hours
                break

        time.sleep(rand)


def start_autoswipe_thread(ratio=70):
    print("Starting autoswipe thread")
    t = threading.Thread(target=auto_swipe(ratio))
    t.start()
    print("Autoswipe thread started")
    return t


def wait_for_threads_to_finish():
    # Wait for all threads to finish
    for t in threads:
        t.join()


def main():
    matches = create_match_objects()
    start_match_threads(matches)
    threads.append(start_autoswipe_thread())
    wait_for_threads_to_finish()


if __name__ == "__main__":
    main()
