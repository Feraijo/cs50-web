from collections import deque
import json

class Message():
    counter = 0
    
    def __init__(self, text, user, timestamp):
        self.id = f'm{Message.counter}'
        Message.counter += 1
        self.user = user
        self.text = text
        self.timestamp = timestamp
    
    def __str__(self):
        return json.dumps(self.__dict__)        

class Chat():

    counter = 0   

    def __init__(self, name):
        self.name = name
        self.id = f'chan{Chat.counter}'
        Chat.counter += 1
        self.history = deque(maxlen=100)

    def __str__(self):
        d = self.__dict__
        d['history'] = list(d['history'])
        return json.dumps(d)        

    def add_message(self, message):
        self.history.append(str(message))

    def get_msg_by_id(self, msg_id):
        return [m for m in self.history if json.loads(m)['id'] == msg_id][0]

    def delete_message(self, msg):
        self.history.remove(msg)        

    def get_history(self):
        return list(self.history)
        

if __name__ == '__main__':
    names = ['Default channel', 'Chan1']
    chans = [Chat(n) for n in names]

    for i in range(4):
        m = Message(f'sdfsdf {i}', 'Eli', '25-01-2020 16:45')
        chans[0].add_message(m)
    
    print(chans[0].history)

    q = chans[0].get_msg_by_id(('m1'))
    chans[0].delete_message(q)

    print(chans[0].history)

