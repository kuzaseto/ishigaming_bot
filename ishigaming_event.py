import os
from discord import *
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
# from random import randint


load_dotenv(dotenv_path=f"/Users/frigi/Documents/bot_discord/ishigaming/config")

intents = Intents.all()
bot = commands.Bot(command_prefix='i!', help_command=None, intents=intents)


@bot.event
async def on_ready():
    print("ishigaming event")
    await bot.get_channel(1133014961203982377).send('Bot bump et goulag allumé')
    await bot.change_presence(activity=Activity(type=ActivityType.listening, name="Aide pour les bumps et autres choses à venir"))
    # msg_bump = None
    # async for message in bot.get_channel(895427428896370718).history():
    #     for embed in message.embeds:
    #         if 
    # await asyncio.sleep(480)
    # await bot.get_channel(895427428896370718).send('Pensez à bump le serveur <@&1117402655271157770>')


def endwith(phrase,word):
    enleve = [',','.','?',' ',';','!','^','*','/','\\','|','(',')','[',']','\"','-','_']
    while phrase[-1] in enleve:
        phrase = phrase[:-1]
    return phrase[-len(word):] == word
def contain(phrase,word):
    phrase = phrase.split()
    for i in phrase:
        if len(i) > len(word):
            for k in range(len(i)):
                phrase.append(i[k:k+len(word)])
    return word in phrase
def contain_list(phrase,word):
    for i in word:
        if contain(phrase,i): return True
    return False
@bot.event
async def on_message(message):
    if contain_list(message.content.lower(),['coubae','coubeh','couflop','oubaka','coiquou','quoicou']):
        goulag = utils.get(message.guild.roles, name='Goulag (tu l\'as cherché)')
        if goulag not in [i for i in message.author.roles]:
            await bot.get_channel(1133014961203982377).send(f'{message.author} au goulag')
            await message.author.add_roles(goulag, reason='La personne a dit un mot interdit')
        # else: await bot.get_channel(1133014961203982377).send(f'{message.author} en isolement') ; message.author.add_roles(utils.get(message.guild.roles,name='Rebut de la société'), reason='Arrête de forcer frérot')
    elif str(message.author) == 'DISBOARD#2760' and str(message.channel) == '৻bump৲':
        print('serveur bumpé')
        await asyncio.sleep(7200)
        await message.channel.send('Pensez à bump le serveur <@&1117402655271157770>')


bot.run(os.getenv('TOKEN'))