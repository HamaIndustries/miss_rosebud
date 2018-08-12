from chatterbot import ChatBot

import re

class holder():
    def __init__(self, channel, client):
        print('bbbbbbbb')
        self.chatbot = ChatBot(
            'Miss Rosebud',
            trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
        )
        
        wishid = '304080356900995092'
        logs = client.logs_from(channel, limit=100)
        print(logs)
        #a = logs.next()
        #b = logs.next()
        trainlist = []
        print('aaaaaaa')
        for i in logs:
            print(i.content)
            if not re.match('[A-Z]|[a-z]', i.content):
                continue
            
            a = b
            b = i

            print(i.content)
            
            if a.author.id != wishid and b.author.id == wishid:
                trainlist += [a.content, b.content]
                
        self.chatbot.train(trainlist)

    #chatbot.train("chatterbot.corpus.english")

    def train(self, channel, client):
        pass
