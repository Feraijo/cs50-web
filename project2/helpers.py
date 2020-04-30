from collections import deque

class Message():
    
    def __init__(self, text, user):
        self.user = user
        self.text = text
    
    def __str__(self):
        return f'{self.user}: {self.text}'

class Chat():

    counter = 0   

    def __init__(self, name):
        self.name = name
        self.id = f'chan{Chat.counter}'
        Chat.counter += 1
        self.history = deque(maxlen=100)

    def __str__(self):
        return str({'name':self.name, 'id': self.id, 'history':list(self.history)})

    def add_message(self, message):
        self.history.append(str(message))
        pass

if __name__ == '__main__':
    names = ['Default channel', 'Chan1']
    chans = [Chat(n) for n in names]

    for i in range(123):
        m = Message(f'sdfsdf {i}', 'Eli')
        chans[0].add_message(m)
    
    i = 'chan1'
    print([ch.name for ch in chans if ch.id == i])