import discord
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_components import *
from discord_slash.model import ButtonStyle
import random
import asyncio

#token
import credentials

# import music
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='#',  # prefix commands
                      case_insensitive=True,  # typing A or a does not differ
                      intents=intents)
slash = SlashCommand(client, sync_commands=True)

guild_id = [436955269700780042]

# start Bot
@client.event
async def on_ready():
    # status
    activity = discord.Game(name="#help", type=3)
    await client.change_presence(status=discord.Status.idle, activity=activity)
    print("Bot is ready!")

    #emoji
    Channel = client.get_channel(958032546044719104)
    Text= "Clique nos emojis abaixo para pegar seus respectivos cargos"
    Moji = await Channel.send(Text)
    await Moji.add_reaction('👻')
    await Moji.add_reaction('🤖')
@client.event
async def on_reaction_add(reaction, user):
    Channel = client.get_channel(958032546044719104)
    if reaction.message.channel.id != Channel.id:
        return
    if reaction.emoji == "👻":
      Role = discord.utils.get(user.guild.roles, name="FokiMember")
      await user.add_roles(Role)
    if reaction.emoji == "🤖":
      Role = discord.utils.get(user.guild.roles, name="Programmer")
      await user.add_roles(Role)

# welcome and goodbye
@client.event
async def on_member_join(member):
   await client.get_channel(839676654112342016).send(f"{member.mention} entrou no servidor!")

@client.event
async def on_member_remove(member):
   await client.get_channel(839676654112342016).send(f"{member.mention} saiu do servidor!")

# random number
@slash.slash(name='sorteio', description='Descricao', guild_ids = guild_id)
async def _dado(ctx: SlashContext, numsorteio):
    number = random.randint(1, int(numsorteio))
    embed_t = discord.Embed(
        title = 'Número Aleatório',
        description = F'Números de 0 a {numsorteio}\n\nO número sorteado foi **{number}**',
        colour = 4915330
    )
    print(ctx.author)
    await ctx.send(embed=embed_t, content=f'')

# clean chat
@slash.slash(name="limparchat",guild_ids= guild_id)
@commands.has_permissions(manage_messages=True)
async def _limparchat(ctx: SlashContext, qnt):
    await ctx.send(f'Você apagou {qnt} com sucesso.', hidden=True)
    await ctx.channel.purge(limit=int(qnt))

# moderation

# ban
@slash.slash(name='ban', description='Descricao', guild_ids = guild_id)
@commands.has_permissions(ban_members=True)
async def _ban(ctx: SlashContext,
               membro: discord.Member,
               motivo = 'Sem motivo registrado'):
    await membro.ban(reason=motivo)
    await ctx.send(f"O membro `{membro}` foi banido! A razão foi {motivo}")

# kick
@slash.slash(name='kick', description='Descricao', guild_ids = guild_id)
@commands.has_permissions(kick_members=True)
async def _kick(ctx: SlashContext,
               membro: discord.Member,
               motivo = 'Sem motivo registrado'):
    await membro.kick(reason=motivo)
    await ctx.send(f"O membro `{membro}` foi kickado! A razão foi {motivo}")


# perolas
@slash.slash(name="perolas",guild_ids= guild_id)
async def _perolas(ctx: SlashContext):
    perolas = [
        create_button(custom_id="josh",style=ButtonStyle.red,label='Josh'),
        create_button(custom_id="carlos", style=ButtonStyle.red, label='Carlos'),
        create_button(custom_id="serjoca", style=ButtonStyle.red, label='Serjoca')
    ]

    action_perolas = create_actionrow(*perolas)
    mensagem = await ctx.send('Escolha sua opção', components=[action_perolas])

    def check(m):
        return m.channel == ctx.channel and m.author == ctx.author
    try:
        opcoes = await wait_for_component(client=client,components=perolas,timeout=300,check=check)
    except asyncio.TimeoutError:
        await ctx.send('Seu tempo esgotou.')
    else:
        resposta = opcoes.custom_id
        if resposta == 'josh':
            await ctx.send('OXE!!! QUEM É?')
        elif resposta == 'carlos':
            await ctx.send('VAI SE LASCAR!')
        elif resposta == 'serjoca':
            await ctx.send('X1 Carteira? Você toma bomba menor!')

# music bot
intents = discord.Intents.default()
intents.members = True

testing = False


client.remove_command('help')

for filename in os.listdir('cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(credentials.token)