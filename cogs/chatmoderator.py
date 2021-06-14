from googleapiclient.discovery import build
import discord
from discord.ext import commands


class ChatModeratorCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
      
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(status=discord.Status.idle, activity=discord.Game('Moderating Chats!'))

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):


        API_KEY = "" #API Key for perspective api
        client = build(
            "commentanalyzer",
            "v1alpha1",
            developerKey=API_KEY,
            discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
            static_discovery=False,
        )
        analyze_request = {
            'comment': {'text': message.content},
            'requestedAttributes': {'PROFANITY': {}}
        }

        response = client.comments().analyze(body=analyze_request).execute()



        # Profanity Detection
        if not message.author.bot:
            channel = self.bot.get_channel()  #ID of channel that will contain the reported messages
            score = response["attributeScores"]["PROFANITY"]["summaryScore"]["value"] * 100
            print(score)
            if score > 75:
                message_url = message.jump_url
                embed = discord.Embed(author=message.author, title="Toxic Message Detected", url=message_url,
                                      color=discord.Colour.red())

                url = message.author.avatar_url

                embed.add_field(name="Message", value=message.content, inline=True)
                embed.add_field(name="Profanity Score", value=str(score)[:5], inline=True)
                embed.add_field(name="Author ID", value=message.author.id, inline=False)

                embed.set_footer(icon_url=url, text="Message Sent By " + str(message.author))
                await channel.send(embed=embed)




def setup(bot):
    bot.add_cog(ChatModeratorCog(bot))
