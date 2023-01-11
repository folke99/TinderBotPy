from dotenv import load_dotenv
load_dotenv()
import tinder_api
import chatgpt_api
import threading
from models import Match


# Create instances of the APIs
tinder = tinder_api.TinderAPI()
chatgpt = chatgpt_api.ChatGptAPI()

matches = []
# Create Match objects for each match
for match in tinder.get_matches_api(True):
    matches.append(Match(match_id=match["match_id"], name=match["name"], last_activity_date=match["last_active"], tinder=tinder, chatgpt=chatgpt))

# Use a thread for each match to check for new messages concurrently
threads = []
for match in matches:
    t = threading.Thread(target=match.wait_for_message)
    t.start()
    threads.append(t)

# Wait for all threads to finish
for t in threads:
    t.join()
