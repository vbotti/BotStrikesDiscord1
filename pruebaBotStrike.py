import asyncio
from random import randint
import discord
import math
from discord import User

TOKEN = 'NTA3OTI5NzY0NDE0MDk1MzY5.Dr43qw.Kj16fyIPJLdEWNeqg2OW6tX5JNs'
client = discord.Client()
listaStrikes = []

async def getMiembros():
    members = client.get_all_members()
    msg =[]
    for member in members:
        msg.append(str(member))
    return msg

async def getUsuario(usuario):
    members = client.get_all_members()
    x = 0
    for member in members:
        if usuario in str(member).lower():
            print(member)
            x = 1
            return str(member).lower()

    if x == 0:
        return "0"


async def getUsuarioObjeto(usuario):
    members = client.get_all_members()
    for member in members:
        if usuario in str(member).lower():
            return member

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself

    if message.author == client.user:
        return

    if message.content.startswith('?ping'):
        await client.send_message(message.channel, '?pong {0.author.mention}'.format(message))

    if message.content.startswith('?hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('?strike'):
        usuario = str(message.content)
        usuario = usuario.replace('?strike ', "")
        usuario = usuario.strip().lower()
        usuario = await getUsuario(usuario)

        if usuario == "0":
            await client.send_message(message.channel, 'El usuario no existe {0.author.mention}'.format(message))
            return

        if usuario in listaStrikes:
            aux = listaStrikes.index(usuario)
            num = listaStrikes[aux +1]
            num = int(num) + 1
            mencionado = await getUsuarioObjeto(usuario)
            if str(num) == "3":


                msg = mencionado.mention + " ha sido muteado 20 segundos"
                listaStrikes[aux+1] = "0"

                await client.server_voice_state(await getUsuarioObjeto(usuario), mute=True)
                await client.send_message(message.channel, msg)
                await asyncio.sleep(20)
                await client.server_voice_state(await getUsuarioObjeto(usuario), mute=False)


            else:
                listaStrikes[aux+1] = str(num)
                msg = 'El usuario ' + mencionado.mention + ' tiene ahora ' + str(num) + ' strikes, puesto por  {0.author.mention}'.format(message)
                await client.send_message(message.channel, msg)

        else:
            listaStrikes.append(usuario)
            listaStrikes.append("1")
            mencionado = await getUsuarioObjeto(usuario)
            msg = 'El usuario ' + mencionado.mention + ' tiene ahora 1 strike, puesto por  {0.author.mention}'.format(message)
            await client.send_message(message.channel, msg)


    if message.content.startswith('?kick'):

        mensaje = (message.content).split(' ')
        victor = await getUsuario("hiimvistor")
        print(victor)
        koko = await getUsuario("koko")
        print(message.author)
        print(str(message.author))
        if str(message.author).lower() == victor or message == koko:
            print()
            if getUsuarioObjeto(mensaje[1]!=None):
                await client.kick(await getUsuarioObjeto(mensaje[1]))

                await client.send_message(message.channel, ':zap:' + "El invocador " + mensaje[1] + " se ha desconectado")

            else:
                await client.send_message(message.channel, "No existe ese usuario")

    if message.content.startswith('?paz'):
        jorge = await getUsuarioObjeto("jorge")
        pulpo = await getUsuarioObjeto("pulpi")
        msg = ':angel: :angel: '+ jorge.mention + ' perdona al inocente de ' +pulpo.mention+ ", el solo quiere la PAZ :angel: :angel:".format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('?dado'):
        msg = randint(1,6)
        await client.send_message(message.channel, "El número es ------------------> " + str(msg))

    if message.content.startswith('?borrar'):
        men = (message.content).split(' ')
        try:
            async for mensaje in client.logs_from(message.channel, limit=int(men[1])):
                await client.delete_message(mensaje)
        except:
            return

    if message.content.startswith('?limpiar'):
        list = []
        try:
            async for mensaje in client.logs_from(message.channel, limit=100):
                if mensaje.author == client.user or '?' in mensaje.content or '!' in mensaje.content:
                    list.append(mensaje)
            await client.delete_messages(list)

        except:
            return

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)