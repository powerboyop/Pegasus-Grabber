import requests


class Checker():
    def __init__(self, token):
        self.status_code = requests.get(f'https://discordapp.com/api//sso?token={token}').status_code
        self.token = token
        
    def get_informations(self):
        if self.status_code == 400:
            profile = requests.get(f'https://discordapp.com/api/v8/users/@me', headers= {'Authorization': self.token, 'content-type': 'application/json'}).json()

            resp =  {
                'Token': self.token,
                'Tag': f"{profile['username']}#{profile['discriminator']}", 
                'ID': profile['id'], 
                'Mail': profile['email'], 
                'Phone': profile['phone'], 
                'Verified': profile['verified'],
                'Locale': profile['locale'],
                'Avatar': f"https://cdn.discordapp.com/avatars/{profile['id']}/{profile['avatar']}.png"
            }

            return resp
        else:
            return 'invalid'