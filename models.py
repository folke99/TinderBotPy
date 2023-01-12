import random
import time
import config


class Match:
    def __init__(self, tinder, chatgpt, match_id: str, name: str, last_activity_date: str):
        self.conversation_state = []
        self.tinder = tinder
        self.chatgpt = chatgpt
        self.match_id = match_id
        self.name = name
        self.last_activity_date = last_activity_date
        self.cache = {"tinder_användare": [], "chatGPT": []}
        self.on_init = True

    def message(self, message):
        message = message.strip()
        # self.tinder.send_message_api(self.match_id, message)
        self.cache["chatGPT"].append(message)
        print(f"Sent message to {self.name}: {message}")
        print(self.cache)

    def get_messages(self):
        return self.tinder.get_messages_api(self.match_id)

    def wait_for_message(self):
        while True:
            print("Checking for new messages...")
            if self.on_init:
                messages_init = self.get_messages()
                for message in messages_init:
                    if message["from"] == config.MY_TINDER_ID:
                        self.cache["chatGPT"].append(message["message"])
                    else:
                        self.cache["tinder_användare"].append(message["message"])

                if messages_init[0]["from"] == config.MY_TINDER_ID:
                    print("Latest message was from me waiting for more messages...")
                    pass
                else:
                    print("On initialization: Latest message was from them, sending message...")
                    message = messages_init[0]["message"]
                    prompt = f"Rollspela att du svarar på Tinder. Det inkommande medelandet är: {message}." \
                             f" Och konversationen än så länge ser ut så här: {self.cache}, du är chatGPT"
                    response = self.chatgpt.generate_response(prompt)
                    self.message(response)
                self.on_init = False
            else:
                messages = []
                for message in self.get_messages():
                    if message["to"] == config.MY_TINDER_ID:
                        messages.append(message["message"])
                # check if there are any new messages
                if len(messages) > len(self.cache["tinder_användare"]) and len(messages) != 1:
                    # extract new messages
                    new_messages = messages[len(self.cache["tinder_användare"]):]
                    for message in new_messages:
                        print(f"New message from {self.name}: {message}")
                        # prompt = f"Roleplay answering a Tinder chat for all upcoming messages.
                        # The incoming message is: {message['message']}. And the conversation so far is {self.cache}"
                        prompt = f"Rollspela att du svarar på Tinder. Det inkommande medelandet är: {message}." \
                                 f" Och konversationen än så länge ser ut så här: {self.cache}, du är chatGPT"
                        response = self.chatgpt.generate_response(prompt)
                        self.cache["tinder_användare"].append(message)
                        # Send the response
                        self.message(response)
            time.sleep(random.randrange(7200, 14400))  # wait for 2-4 hours before checking again
