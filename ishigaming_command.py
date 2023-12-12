import os
from discord import *
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
from random import randint
import praw

load_dotenv(dotenv_path="/Users/frigi/Documents/bot_discord/ishigaming/config")

intents = Intents.all()
bot = commands.Bot(command_prefix='i!', help_command=None, intents=intents)


@bot.event
async def on_ready():
    print("ishigaming command")
    await bot.get_channel(1133014961203982377).send('Bot commandes allumé')


class Mastermind:
    def __init__(self, tries:int = 12):
        self.tries = tries
        self.secret_number = randint(1,6)*1000+randint(1,6)*100+randint(1,6)*10+randint(1,6)

    def restart(self, tries:int = 12):
        self.__init__(tries)

    def test(self, truc:int):
        if truc != self.secret_number: 
            self.tries -= 1
            x = 0
            y = 0
            number = list(str(self.secret_number))
            for i in range(4):
                if str(truc)[i] in number: x += 1 ; number.remove(str(truc)[i])
                if str(truc)[i] == str(self.secret_number)[i]: y += 1
            return [False,x,y]
        else: return [True]

@bot.command(name='mastermind')
async def mastermind(ctx, truc:str):
    if truc.startswith('start'):
        if truc == 'start':
            globals()[str(ctx.author.id)+'_mastermind'] = Mastermind()
        elif truc.split(' ')[1].isdigit():
            globals()[str(ctx.author.id)+'_mastermind'].restart(int(truc.split(' ')[1]))
        await ctx.channel.send(f'Une nouvelle partie est lancée')
    elif truc.isdigit():
        if int(truc) > 1000 and int(truc) < 9999:
            machin = True
            for i in truc:
                machin = machin if int(i) >= 1 and int(i) <= 6 else False
            if machin == True:
                if not globals()[str(ctx.author.id)+'_mastermind'].test(truc)[0]:
                    if globals()[str(ctx.author.id)+'_mastermind'].tries == 0:
                        await ctx.channel.send(f'Partie Terminée vous n\'avez pas trouvé le code secret qui était {globals()[str(ctx.author.id)+"_mastermind"].secret_number}')
                        globals()[str(ctx.author.id)+'_mastermind'].restart()
                    else:
                        await ctx.channel.send(f'Vous n\'avez pas trouvé le code secret mais vous avez {globals()[str(ctx.author.id)+"_mastermind"].test(truc)[1]} bon(s) nombre(s) et vous en avez {globals()[str(ctx.author.id)+"_mastermind"].test(truc)[2]} placé(s) au bon endroit')
                else: await ctx.channel.send(f'Vous avez réussi à trouver le code secret qui était {globals()[str(ctx.author.id)+"_mastermind"].secret_number}. Bien joué !') ; globals()[str(ctx.author.id)+'_mastermind'].restart()
        else: await ctx.channel.send(f'Vous n\'avez pas saisi un code correct à essayer')
    else: await ctx.channel.send(f'Vous n\'avez pas saisi une commande valide')



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

@bot.command(name='fuite')
async def fuite(ctx):
    goulag_role = utils.get(ctx.guild.roles,name='Goulag (tu l\'as cherché)')
    if goulag_role in [i for i in ctx.author.roles]:
        if not goulag.state:
            await ctx.channel.send('Vous tentez de vous échapper')
            proba = randint(0,1000)
            if proba <= 25: await ctx.channel.send(f'{ctx.author} a réussi à s\'échapper') ; ctx.author.remove_roles(goulag_role, reason='À fui')
            else: await ctx.channel.send(f'{ctx.author} n\'a pas réussi à s\'échapper')
            await goulag.en_cours()
        else: await ctx.channel.send(f'Vous ne pouvez pas retenter de vous échapper pour le moment. Vous pouvez retenter dans {goulag.temps_restant}s')
    else: await ctx.channel.send('Vous n\'êtes actuellement pas au goulag')



have_goulag = []
have_isolement = []
@bot.command(name='role')
@commands.has_permissions(manage_roles=True)
async def addrole(ctx,user:Member,role:Role):
    # global have_goulag
    # global have_isolement
    if role in [i for i in user.roles]:
        await user.remove_roles(role)
        await ctx.channel.send(f'Le rôle {role.name} a été correctement retiré à {user.mention}')
        # if role.name == 'Goulag (tu l\'as cherché)' and user.name in have_goulag: have_goulag.remove(user.name)
        # elif role.name == 'Rebut de la société' and user.name in have_isolement: have_isolement.remove(user.name)
    else:
        await user.add_roles(role)
        await ctx.channel.send(f'Le rôle {role.name} a été correctement ajouté à {user.mention}')
        # if role.name == 'Goulag (tu l\'as cherché)' and user.name not in have_goulag: have_goulag.append(user.name)
        # elif role.name == 'Rebut de la société' and user.name not in have_isolement: have_isolement.append(user.name)

@addrole.error
async def addrole_error(ctx,error):
    if isinstance(error,commands.MissingPermissions):
        await ctx.channel.send(f'Vous n\'avez pas la permission d\'effectuer cette commande')
    elif isinstance(error,commands.BotMissingPermissions):
        await ctx.channel.send(f'Je n\'ai pas les permissions suffisantes pour effectuer cette action')
    # elif isinstance(error,commands.)



@bot.command(name='role_after')
@commands.has_permissions(manage_roles=True)
async def role_after(ctx,user:Member,role:Role,time:int):
    if role in [i for i in user.roles]:
        await ctx.channel.send(f'Le rôle {role.name} va être retiré à {user.mention} dans {time}min')
        await asyncio.sleep(time*60)
        await user.remove_roles(role)
        await ctx.channel.send(f'Le rôle {role.name} a été correctement retiré à {user.mention}')
    else:
        await ctx.channel.send(f'Le rôle {role.name} va être ajouté à {user.mention} dans {time}min')
        await asyncio.sleep(time*60)
        await user.add_roles(role)
        await ctx.channel.send(f'Le rôle {role.name} a été correctement ajouté à {user.mention}')

@role_after.error
async def role_after_error(ctx,error):
    if isinstance(error,commands.MissingPermissions):
        await ctx.channel.send(f'Vous n\'avez pas la permission d\'effectuer cette commande')
    elif isinstance(error,commands.BotMissingPermissions):
        await ctx.channel.send(f'Je n\'ai pas les permissions suffisantes pour effectuer cette action')



@bot.command(name='temprole')
@commands.has_permissions(manage_roles=True)
async def temprole(ctx,user:Member,role:Role,time:int):
    if role in [i for i in user.roles]:
        await user.remove_roles(role)
        await ctx.channel.send(f'Le rôle {role.name} est retiré à {user.mention} pendant {time}min')
        await asyncio.sleep(time*60)
        await user.add_roles(role)
    else:
        await user.add_roles(role)
        await ctx.channel.send(f'Le rôle {role.name} est ajouté à {user.mention} pendant {time}min')
        await asyncio.sleep(time*60)
        await user.remove_roles(role)

@temprole.error
async def temprole_error(ctx,error):
    if isinstance(error,commands.MissingPermissions):
        await ctx.channel.send(f'Vous n\'avez pas la permission d\'effectuer cette commande')
    elif isinstance(error,commands.BotMissingPermissions):
        await ctx.channel.send(f'Je n\'ai pas les permissions suffisantes pour effectuer cette action')


bot.command(name='clear')
@commands.has_permissions(manage_messages=True)
async def delete2(ctx, nbr:int):
    delete(ctx, nbr)

@bot.command(name='del')
@commands.has_permissions(manage_messages=True)
async def delete(ctx, nbr:int):
    messages = []
    async for message in ctx.channel.history(limit=nbr+1):
        messages.append(message)
    await ctx.channel.delete_messages(messages)

@delete.error
async def delete_error(ctx,error):
    if isinstance(error,commands.MissingPermissions):
        await ctx.channel.send(f'Vous n\'avez pas la permission d\'effectuer cette commande')
    elif isinstance(error,commands.BotMissingPermissions):
        await ctx.channel.send(f'Je n\'ai pas les permissions suffisantes pour effectuer cette action')



reddit = praw.Reddit(client_id='D0mDA-0QfOAXodqd9HanXw',
                     client_secret='zGxZIA7SKMHV5PGtpS3vFv3-wJ7w2w',
                     user_agent='u/god_staline')

@bot.command(name='meme')
async def meme(ctx,sub:str = None):
    if not command_meme.state:
        if sub == None or reddit.subreddit(sub).over18: memes_submissions = reddit.subreddit(['meme','memes','actu_memes','Animemes','FrenchMemes','hmmm','sciencememes','shitposting','wholesomememes','wholesomeanimemes'][randint(0,9)]).hot(limit=50)
        else: memes_submissions = reddit.subreddit(sub).hot(limit=50)
        post_to_pick = randint(1, 50)
        for i in range(0, post_to_pick): submission = next(x for x in memes_submissions if not x.stickied and not x.over_18)
        
        embed = Embed(title=submission.title,url='https://youtu.be/dQw4w9WgXcQ')
        embed.set_image(url = submission.url)
        await ctx.channel.send(embed=embed)
        await command_meme.en_cours()
    else: await ctx.channel.send(f'Veuillez attendre {command_meme.temps_restant}s')



@bot.event
async def on_member_join(member):
    global have_goulag
    global have_isolement
    if member.id in have_goulag: await member.add_roles(utils.get(member.guild.roles,name='Goulag (tu l\'as cherché)'),reason='tu n\'y échapperas pas') ; have_goulag.remove(member.id)
    if member.id in have_isolement: await member.add_roles(utils.get(member.guild.roles,name='Rebut de la société',reason='tu n\'y échapperas pas')) ; have_isolement.remove(member.id)
    if member.id in ['1080551007240589422','722421776801333280']: await member.add_roles(utils.get(member.guild.roles,name='Les psychopathes',reason='Tu vas pas t\'en débarasses comme ça'))

@bot.event
async def on_member_remove(member):
    print(i.name for i in member.roles)
    global have_goulag
    global have_isolement
    if utils.get(member.guild.roles,name='Goulag (tu l\'as cherché)') in [i for i in member.roles]: have_goulag.append(member.id)
    if utils.get(member.guild.roles,name='Rebut de la société') in [i for i in member.roles]: have_isolement.append(member.id)
    


bot.run(os.getenv('TOKEN'))