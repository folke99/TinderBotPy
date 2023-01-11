import random
import time


class Match:
    def __init__(self, tinder, chatgpt, match_id: str, name: str, last_activity_date: str):
        self.conversation_state = []
        self.tinder = tinder
        self.chatgpt = chatgpt
        self.match_id = match_id
        self.name = name
        self.last_activity_date = last_activity_date
        self.cache = {}
        #prompt = "Rolspela som om du chattade på Tinder, jag börjar skriva"
        #response = self.chatgpt.generate_response(prompt)
        #self.conversation_state.append({prompt: response})
        #print(self.conversation_state)

    def message(self, message):
        self.tinder.send_message_api(self.match_id, message)

    def get_messages(self):
        return self.tinder.get_messages_api(self.match_id)

    def wait_for_message(self):
        while True:
            messages = self.get_messages()
            # check if there are any new messages
            if len(messages) > len(self.conversation_state):
                # extract new messages
                new_messages = messages[len(self.conversation_state):]
                for message in new_messages:
                    print(f"New message from {self.name}: {message['message']}")
                    # Do something with the new message, like responding

                    #prompt = f"Rolplay answering a Tinder chat for all upcomming messages. The incoming message is: {message['message']}. And the conversation so far is {self.cache}"
                    prompt = f"Rollspela att du svarar på Tinder. Det inkommande medelandet är: {message['message']}. Och konversationen än så länge ser ut så här: {self.cache}"
                    response = self.chatgpt.generate_response(prompt)
                    self.cache[message['message']] = response
                    print(response)
                    # Send the response
                    #self.tinder.send_message_api(self.match_id, response)
            time.sleep(random.randrange(8000, 50000))  # wait for 8000-50000 seconds before checking again

    def wait_for_message2(self):
        while True:
            messages_raw = self.get_messages()
            messages = []
            for message in messages_raw:
                messages.append(message["message"])
            # check if there are any new messages
            if len(messages) > (len(self.conversation_state)-1):
                # extract new messages
                new_messages = messages[(len(self.conversation_state)-1):]
                for message in new_messages:
                    print(f"New message from {self.name}: {message}")
                    # Do something with the new message, like responding
                    gpt_response = self.chatgpt.generate_response(message)
                    print(gpt_response)    #self.message(gpt_response)
                    # Send a message here
                    self.conversation_state = messages
            time.sleep(random.randrange(8000, 50000))  # wait for 8000-50000 seconds before checking again
