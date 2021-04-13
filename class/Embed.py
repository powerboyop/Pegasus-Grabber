import discord

class EmbedGenerator():
    def __init__(self):
        self.footer = "github.com/Its-Vichy/Pegasus-Grabber  | V0.1"
        self.title  = "**`🦄` Pegasus**"
        self.color = 0x000001
    
    def generate_embed(self, fields):
        embed = discord.Embed(title = self.title, color= self.color)
        embed.set_footer(text = self.footer)
        embed.timestamp

        for name, value in fields.items():
            embed.add_field(name = name, value = value)
        
        return embed