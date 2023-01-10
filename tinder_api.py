import json
import requests
from TinderApi.api import matches
from TinderApi import tinder
# Import configurations
import config


class TinderAPI:
    def __init__(self):
        self.tinderIns = tinder.Tinder(debug=True, x_auth_token=config.TINDER_TOKEN)
        # tinder.Tinder.login(self, "0735150205", "folkefd@gmail.com", store_auth_token=True)

    def swipe_right(self):
        users_to_swipe = tinder.Swipe.get_users(self.tinderIns)
        for user in users_to_swipe:
            liked = self.tinderIns.swipe.like_user(user["user_id"])  # LIKE USER
            print(liked)  # -> {'status': 200, 'match': False, 'user_id': 'some_user_id', 'likes_left': 100}
            return  # This is her as a block. Removing this will probobly get your account banned

    def get_matches(self, messages):
        return tinder.Matches.get_matches(self.tinderIns, with_messages=messages)

    # Send message does not work.
    def send_message(self, match_id, message):
        url = f"{self.base_url}/v2/matches/{match_id}/messages"
        data = json.dumps({"message": message})
        response = requests.post(url, headers=self.headers, data=data)

        if response.status_code != 200:
            raise ValueError(f"Failed to send message. {response.text}")
