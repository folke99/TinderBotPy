from TinderApi import tinder

# Import configurations
import config


class TinderAPI:
    def __init__(self):
        self.tinderIns = tinder.Tinder(debug=True, x_auth_token=config.TINDER_TOKEN)
        # tinder.Tinder.login(self, "0735150205", "folkefd@gmail.com", store_auth_token=True)

    def swipe_right_api(self):
        users_to_swipe = tinder.Swipe.get_users(self.tinderIns)
        for user in users_to_swipe:
            liked = self.tinderIns.swipe.like_user(user["user_id"])  # LIKE USER
            print(liked)  # -> {'status': 200, 'match': False, 'user_id': 'some_user_id', 'likes_left': 100}
            return  # This is her as a block. Removing this will probobly get your account banned

    def get_matches_api(self, messages):
        return tinder.Matches.get_matches(self.tinderIns, with_messages=messages)

    # Send message might work not tested.
    def send_message_api(self, match_id, message):
        tinder.Matches.send_message(self.tinderIns, match_id, message)

    def get_messages_api(self, match_id):
        return tinder.Matches.get_messages(self.tinderIns.matches, match_id)

    def get_all_messages_api(self):
        return tinder.Matches.get_all_messages(self.tinderIns.matches)