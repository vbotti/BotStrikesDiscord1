import asyncio

import discord

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
        else:
            return None

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
            if str(num) == "3":


                msg ='@' + usuario + " ha sido muteado 20 segundos"
                listaStrikes[aux+1] = "0"

                await client.server_voice_state(await getUsuarioObjeto(usuario), mute=True)
                await asyncio.sleep(20)
                await client.server_voice_state(await getUsuarioObjeto(usuario), mute=False)

            else:
                listaStrikes[aux+1] = str(num)
                msg = 'El usuario @' + str(usuario) + ' tiene ahora ' + str(num) + ' strikes, puesto por  {0.author.mention}'.format(message)

        else:
            listaStrikes.append(usuario)
            listaStrikes.append("1")
            msg = 'El usuario @' + str(usuario) + ' tiene ahora 1 strike, puesto por  {0.author.mention}'.format(message)

        await client.send_message(message.channel, msg)
    if message.content.startswith('?kick'):

        mensaje = (message.content).split(' ')
        if getUsuarioObjeto(mensaje[1]!=None):
            await client.kick(await getUsuarioObjeto(mensaje[1]))

            await client.send_message(message.channel, ':zap:' + "El invocador " + mensaje[1] + " se ha desconectado")

        else:
            await client.send_message(message.channel, "No existe ese usuario")


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)