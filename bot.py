# import os
from interactions import *
# from dotenv import load_dotenv
import asyncio
from random import randint
import praw


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
    await bot.get_channel(1133014961203982377).send('Bot allumé')
    await bot.change_presence(activity=Activity(name='Made by kuzaseto3371',type=ActivityType.LISTENING))

# S'exécute lorsqu'un message est envoyé
@listen()
async def on_message_create(event):
    message = event.message

    # Si un bump est fait
    if str(message.author) == 'DISBOARD#2760' and str(message.channel.name) == '৻bump৲':
        await bot.get_channel(1133014961203982377).send(f'serveur bumpé')
        print('serveur bumpé')
        await asyncio.sleep(7200)
        await message.channel.send('Pensez à bump le serveur <@&1117402655271157770>')

    # Si la personne est un con
    elif contain_list(message.content.lower(),['coubae','coubeh','couflop','oubaka','coiquou','quoicou']):
        goulag = utils.get(message.guild.roles, name='Goulag (tu l\'as cherché)')
        if goulag not in [i for i in message.author.roles]:
            await bot.get_channel(1133014961203982377).send(f'{message.author} au goulag')
            await message.author.add_role(role=goulag)

# Support mastermind
class Mastermind:
    def __init__(self, tries:int = 12):
        self.tries = tries
        self.secret_number = randint(1,6)*1000+randint(1,6)*100+randint(1,6)*10+randint(1,6)

    def test(self, truc:int):
        if truc != self.secret_number: 
            self.tries -= 1
            x = 0
            y = 0
            number = list(str(self.secret_number))
            for i in range(4):
                if str(truc)[i] in number:
                    x += 1
                    number.remove(str(truc)[i])
                if str(truc)[i] == str(self.secret_number)[i]:
                    y += 1
            return [False,x,y]
        else: return [True]

@slash_command(name='mastermind', description='Jouer au Mastermind')
@slash_option(name='playing', description='Commencer une nouvelle partie ou continuer la précédente', opt_type=OptionType.INTEGER, required=True, choices=[SlashCommandChoice(name='Start', value=1), SlashCommandChoice(name='Continue', value=0)])
@slash_option(name='nombre', description='Nombre à tester (entre 1111 et 6666)', required=True, opt_type=OptionType.INTEGER, min_value=1111, max_value=6666)
async def mastermind_function(ctx: SlashContext, playing: int, nombre: int):
    if playing == 1:
        globals()[str(ctx.author.id)+'_mastermind'] = Mastermind()
        await ctx.send(f'Une nouvelle partie est lancée')
    if not globals()[str(ctx.author.id)+'_mastermind'].test(nombre)[0]:
        if globals()[str(ctx.author.id)+'_mastermind'].tries == 0:
            await ctx.channel.send(f'Partie Terminée vous n\'avez pas trouvé le code secret qui était {globals()[str(ctx.author.id)+"_mastermind"].secret_number}')
            globals()[str(ctx.author.id)+'_mastermind'] = Mastermind()
        else:
            await ctx.send(f'Vous n\'avez pas trouvé le code secret mais vous avez {globals()[str(ctx.author.id)+"_mastermind"].test(nombre)[1]} bon(s) nombre(s) et vous en avez {globals()[str(ctx.author.id)+"_mastermind"].test(nombre)[2]} placé(s) au bon endroit')
    else: await ctx.send(f'Vous avez réussi à trouver le code secret qui était {globals()[str(ctx.author.id)+"_mastermind"].secret_number}. Bien joué !') ; globals()[str(ctx.author.id)+'_mastermind'].restart()

class Cooldown:
    def __init__(self, time: int = 60, state: bool = False):
        self.time = int(time)
        self.temps_restant = 0
        self.state = bool(state)

    async def en_cours(self):
        self.state = True
        self.temps_restant = self.time
        while self.temps_restant > 0:
            await asyncio.sleep(1)
            self.temps_restant -= 1
        self.fini()
    
    def fini(self):
        self.state = False
goulag = Cooldown(300)
command_meme = Cooldown(10)

async def check_role_goulag(ctx: BaseContext):
    return goulag in [i for i in ctx.author.roles]

@slash_command(name='fuite', description='Haha mystère')
@check(check_role_goulag)
async def fuite_function(ctx=SlashContext):
    goulag_role = utils.get(ctx.guild.roles,name='Goulag (tu l\'as cherché)')
    if not goulag.state:
        await ctx.channel.send('Vous tentez de vous échapper')
        proba = randint(0,1000)
        if proba <= 25: await ctx.send(f'{ctx.author} a réussi à s\'échapper') ; ctx.author.remove_role(goulag_role, reason='À fui')
        else: await ctx.send(f'{ctx.author} n\'a pas réussi à s\'échapper')
        await goulag.en_cours()
    else: await ctx.send(f'Vous ne pouvez pas retenter de vous échapper pour le moment. Vous pouvez retenter dans {goulag.temps_restant}s')

have_goulag = []
have_isolement = []
@slash_command(name='role', description='Ajouter ou retirer un rôle')
@slash_default_member_permission(Permissions.MANAGE_ROLES)
@slash_option(name='member', description='Personne à qui ajouter ou retirer le rôle', opt_type=OptionType.USER, required=True)
@slash_option(name='role', description='Rôle à ajouter ou retirer', opt_type=OptionType.ROLE, required=True)
@slash_option(name='temps', description='Temps avant d\'ajouter ou retirer le rôle (min)', opt_type=OptionType.INTEGER, required=False)
async def role_function(ctx: SlashContext, role:Role, member:Member, temps: int | None = None):
    if role in [i for i in member.roles]:
        if temps != None:
            await ctx.send(f'Le rôle {role.name} va être retiré à {member.mention} dans {temps}min')
            await asyncio.sleep(temps*60)
        await member.remove_role(role)
        await ctx.send(f'Le rôle {role.name} a été correctement retiré à {member.mention}')
    else:
        if temps != None:
            await ctx.send(f'Le rôle {role.name} va être ajouté à {member.mention} dans {temps}min')
            await asyncio.sleep(temps*60)
        await member.add_role(role)
        await ctx.send(f'Le rôle {role.name} a été correctement ajouté à {member.mention}')

@slash_command(name='temprole', description='Ajouter ou retirer un rôle pendant une certaine durée')
@slash_default_member_permission(Permissions.MANAGE_ROLES)
@slash_option(name='member', description='Personne à qui ajouter ou retirer le rôle', opt_type=OptionType.USER, required=True)
@slash_option(name='role', description='Rôle à ajouter ou retirer', opt_type=OptionType.ROLE, required=True)
@slash_option(name='temps', description='Temps du rôle (min)', opt_type=OptionType.INTEGER, required=True)
async def temprole_function(ctx: SlashContext, member: Member, role: Role, temps: int):
    if role in [i for i in member.roles]:
        await member.remove_role(role)
        await ctx.send(f'Le rôle {role.name} est retiré à {member.mention} pendant {temps}min')
        await asyncio.sleep(temps*60)
        await member.add_role(role)
    else:
        await member.add_role(role)
        await ctx.send(f'Le rôle {role.name} est ajouté à {member.mention} pendant {temps}min')
        await asyncio.sleep(temps*60)
        await member.remove_role(role)

@slash_command(name='clear', description='Supprimer N messages')
@slash_default_member_permission(Permissions.MANAGE_MESSAGES)
@slash_option(name='nombre', description='Nombre de messages à supprimer', opt_type=OptionType.INTEGER, min_value=1, max_value=100, required=True)
async def clear_function(ctx: SlashContext, nombre:int):
    await ctx.channel.purge(deletion_limit=nombre, reason=f'Command clear by {ctx.author.display_name}')

reddit = praw.Reddit(client_id='',
                     client_secret='',
                     user_agent='',
                     check_for_async=False)

@slash_command(name='meme', description='Cherche un meme récent au hasard sur reddit')
@slash_option(name='sub', description='Subreddit dans lequel chercher le meme', opt_type=OptionType.STRING, required=False)
async def meme_function(ctx: SlashContext, sub: str | None = None):
    if not command_meme.state:
        if sub == None or reddit.subreddit(sub).over18: memes_submissions = reddit.subreddit(['meme','memes','actu_memes','Animemes','FrenchMemes','hmmm','sciencememes','shitposting','wholesomememes','wholesomeanimemes'][randint(0,9)]).hot(limit=50)
        else: memes_submissions = reddit.subreddit(sub).hot(limit=50)
        post_to_pick = randint(1, 50)
        for i in range(0, post_to_pick): submission = next(x for x in memes_submissions if not x.stickied and not x.over_18)
        
        embed = Embed(title=submission.title,url='https://youtu.be/dQw4w9WgXcQ')
        embed.set_image(url = submission.url)
        await ctx.send(embed=embed)
        await command_meme.en_cours()
    else: await ctx.channel.send(f'Veuillez attendre {command_meme.temps_restant}s')

@listen(events.MemberAdd)
async def on_member_join(member):
    global have_goulag
    global have_isolement
    if member.id in have_goulag: await member.add_roles(utils.get(member.guild.roles,name='Goulag (tu l\'as cherché)'),reason='tu n\'y échapperas pas') ; have_goulag.remove(member.id)
    if member.id in have_isolement: await member.add_roles(utils.get(member.guild.roles,name='Rebut de la société',reason='tu n\'y échapperas pas')) ; have_isolement.remove(member.id)
    if member.id in ['1080551007240589422','722421776801333280']: await member.add_roles(utils.get(member.guild.roles,name='Les psychopathes',reason='Tu vas pas t\'en débarasses comme ça'))

@listen(events.MemberRemove)
async def on_member_remove(member):
    print(i.name for i in member.roles)
    global have_goulag
    global have_isolement
    if utils.get(member.guild.roles,name='Goulag (tu l\'as cherché)') in [i for i in member.roles]: have_goulag.append(member.id)
    if utils.get(member.guild.roles,name='Rebut de la société') in [i for i in member.roles]: have_isolement.append(member.id)


# bot.start(os.getenv('TOKEN'))
bot.start(open("/path/to/token/file").readline().replace("\n",""))
