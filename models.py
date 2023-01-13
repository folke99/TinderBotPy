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
        self.tinder.send_message_api(self.match_id, message)
        self.cache["chatGPT"].append(message)
        print(f"Sent message to {self.name}: {message}")
        print(self.cache)
        return

    def get_messages(self):
        return self.tinder.get_messages_api(self.match_id)

    def wait_for_message(self):
        while True:
            if self.on_init:
                print("Handling init conversation...")
                messages_init = self.get_messages()
                print("messages_init: ",messages_init)
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
                    cache_string = ""
                    for key, value in self.cache.items():
                        if key == "tinder_användare":
                            cache_string += f"{key}:\n"
                            for message in value:
                                cache_string += f"- {message}\n"
                    #prompt = f"Rollspela att du svarar på Tinder medelanden. Det inkommande medelandet är: {messages_init[0]['message']}. If the messages from 'tinder_användare' are in english you should also answer in english!" \
                    #        f" Och konversationen än så länge ser ut så här:\n{cache_string}"
                    prompt = f"Roleplay answering a Tinder chat for all upcoming messages." \
                             f"The incoming message is: {messages_init[0]['message']}. PLEASE ANSWER IN THE APPROPRIATE LANGUAGE!. you are 'chatGPT' and you are chatting with 'tinder_användare' And the conversation so far is {cache_string}."

                    print("THIS IS THE PROMPT:     ", prompt)
                    response = self.chatgpt.generate_response(prompt)

                    self.message(response)
                self.on_init = False
            else:
                print("Checking for new messages...")
                messages = []
                for message in self.get_messages():
                    if message["to"] == config.MY_TINDER_ID:
                        messages.append(message["message"])
                print("messages: ", messages)
                print("cache: ", self.cache)
                # check if there are any new messages
                print("len(messages): " + str(len(messages)),
                      "len(self.cache['tinder_användare']): " + str(len(self.cache["tinder_användare"])))
                if len(messages) > len(self.cache["tinder_användare"]):
                    print("New messages found!")
                    # extract new messages
                    new_messages = messages[len(self.cache["tinder_användare"]):]
                    for message in reversed(new_messages):
                        print(f"New message from {self.name}: {message}")
                        cache_string = ""
                        for key, value in self.cache.items():
                            cache_string += f"{key}:\n"
                            for message_prompt in value:
                                cache_string += f"- {message_prompt}\n"
                        # prompt = f"Rollspela att du svarar på Tinder medelanden. Det inkommande medelandet är: {messages_init[0]['message']}. If the messages from 'tinder_användare' are in english you should also answer in english!" \
                        #        f" Och konversationen än så länge ser ut så här:\n{cache_string}"
                        prompt = f"Roleplay answering a Tinder chat for all upcoming messages." \
                                 f"The incoming message is: {message}. And the conversation so far is {cache_string}"
                        response = self.chatgpt.generate_response(prompt)
                        self.cache["tinder_användare"].append(message)
                        # Send the response
                        self.message(response)

            time_to_sleep = random.randint(60, 300)
            print(f"Sleeping for {time_to_sleep} seconds...")
            time.sleep(time_to_sleep)  # wait for 1-60 min before checking again
