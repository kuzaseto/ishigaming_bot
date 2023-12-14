import os
from interactions import *
from dotenv import load_dotenv
import asyncio


bot = Client(intents=Intents.ALL)


# A certain word at the end of a phrase
def endwith(phrase: str,word: str) -> bool:
    '''
    Verify that a phrase end with a word
    @param phrase: (str) phrase in which search
    @param mot: (str) word searched
    @return: (bool)
    '''
    enleve = [',','.','?',' ',';','!','^','*','/','\\','|','(',')','[',']','\"','-','_']
    while phrase[-1] in enleve:
        phrase = phrase[:-1]
    return phrase[-len(word):] == word

# A certain word in a phrase
def contain(phrase: str,word: str) -> bool:
    '''
    Verify that a word is in a phrase
    @param phrase: (str) phrase in which search
    @param mot: (str) word searched
    @return: (bool)
    '''
    phrase = phrase.split()
    for i in phrase:
        if len(i) > len(word):
            for k in range(len(i)):
                phrase.append(i[k:k+len(word)])
    return word in phrase

# A certain word in a phrase, list version
def contain_list(phrase: list,word: str) -> bool:
    '''
    Verify that a word is in a phrase, list version
    @param phrase: (list) phrase in which search
    @param mot: (str) word searched
    @return: (bool)
    '''
    for i in word:
        if contain(phrase,i): return True
    return False

# Initialise les états du bot
@listen()
async def on_ready():
    print("ishigaming bot")
    await bot.get_channel(1133014961203982377).send('Bot allumé pour tests')
    await bot.change_presence(activity=Activity(name='En cours de reécriture',type=ActivityType.LISTENING))

# S'exécute lorsqu'un message est envoyé
@listen()
async def on_message_create(event):
    message = event.message

    # Si un bump est fait
    if str(message.author) == 'DISBOARD#2760' and str(message.channel) == '৻bump৲':
        print('serveur bumpé')
        await asyncio.sleep(7200)
        await message.channel.send('Pensez à bump le serveur <@&1117402655271157770>')

    # Si la personne est un con
    elif contain_list(message.content.lower(),['coubae','coubeh','couflop','oubaka','coiquou','quoicou']):
        goulag = utils.get(message.guild.roles, name='Goulag (tu l\'as cherché)')
        if goulag not in [i for i in message.author.roles]:
            await bot.get_channel(1133014961203982377).send(f'{message.author} au goulag')
            await message.author.add_role(role=goulag)


# bot.start(os.getenv('TOKEN'))
bot.start(open("/media/enzo/3D1C-9390/bots_discord/ishigaming_bot/config").readline().replace("\n",""))