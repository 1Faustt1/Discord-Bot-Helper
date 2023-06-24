import datetime
import random
import asyncio

import disnake
from disnake import *
from disnake.ext import commands
from censored_words import CENSORED_WORDS
from welcom_words import WELCOM_WORDS

bot = commands.Bot(command_prefix=".", help_command=None, intents=Intents.all())

# ивент

# старт бота
@bot.event
async def on_ready():
    print("Bot ready")

    await bot.change_presence(status=disnake.Status.online, activity=disnake.Game(".help, чтобы узнать все команды."))

#присоединение игрока
@bot.event
async def on_member_join(member):
    role = disnake.utils.get(member.guild.roles, id=0) # ID НУЖНОЙ РОЛИ
    channel = bot.get_channel(0)  # ID КАНАЛА С ПРИБЫВШИМИ
    await channel.send(f"{member.mention}{random.choice(WELCOM_WORDS)}")
    await member.add_roles(role)

# цензура
@bot.event
async def on_message(message):
    await bot.process_commands(message)

    for content in message.content.split():
        for censored_word in CENSORED_WORDS:
            if content.lower() == censored_word:
                if message.author.mention != "<@1118155741421895730>":
                    await message.delete()
                    await message.channel.send(f"{message.author.mention} ай-ай-ай, нельзя писать такие слова `_0.")
                    print(message.author.mention)

# Ошибки
@bot.event
async def on_command_error(ctx, error):
    print(error)

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{ctx.author}, у вас недостаточно прав для выполнения данной команды.")
    elif isinstance(error, commands.UserInputError):
        await ctx.send(embed=Embed(
            description=f"Чтобы узнать как пользоваться командой пропишите .help"
        ))

# команды

# администрация
# кик
@bot.command(name="kick")
@commands.has_permissions(kick_members=True, administrator=True)
async def kick(ctx, member: Member, *, reason="Нарушение правил"):
    channel = bot.get_channel(0) # ID КАНАЛА С ЛОГАМИ КИКА
    await channel.send(f"Администратор {ctx.author.mention} исключил пользователя {member.mention} по причине {reason}.")
    await member.kick(reason=reason)
    await ctx.message.delete()

# бан
@bot.command(name="ban", usage="ban <@user> <reason>")
@commands.has_permissions(ban_members=True, administrator=True)
async def ban(ctx, member: Member, *, reason="Нарушение правил"):
    channel = bot.get_channel(0) # ID КАНАЛА С ЛОГАМИ БАНА
    await channel.send(f"Администратор {ctx.author.mention} заблокировал пользователя {member.mention} по причине {reason}.")
    await member.ban(reason=reason)
    await ctx.message.delete()

# очистка чата
@bot.command(name="clear")
@commands.has_permissions(administrator=True)
async def clear(ctx, amount = 2):
    await ctx.channel.purge(limit=int(amount))

# мьют
@bot.command(name="mute")
@commands.has_permissions(administrator=True)
async def mute(ctx, member: Member, time=60, *, reason="Нарушение правил"):
    channel = bot.get_channel(0)  # ID КАНАЛА С ЛОГАМИ МУТА
    await member.timeout(reason=reason, duration=time)
    await channel.send(f"Администратор {ctx.author.mention} выдал мьют пользователю {member.mention} по причине {reason} на {time} секунд.")
    await ctx.message.delete()
#анмьют
@bot.command(name="unmute")
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: Member, *, reason="..."):
    channel = bot.get_channel(0)  # ID КАНАЛА С ЛОГАМИ АНМУТА
    await member.timeout(reason=reason, duration=None)
    await channel.send(f"Администратор {ctx.author.mention} снял мьют с пользователя {member.mention} по причине {reason}.")
    await ctx.message.delete()

# выдать пред
@bot.command(name="warn")
@commands.has_permissions(administrator=True)
async def warn(ctx, member: Member, *, reason="Нарушение правил"):
    channel = bot.get_channel(0)  # ID КАНАЛА С ЛОГАМИ ВАРНА
    role_w1 = disnake.utils.get(member.guild.roles, id=0) # ID НУЖНОЙ РОЛИ
    role_w2 = disnake.utils.get(member.guild.roles, id=0) # ID НУЖНОЙ РОЛИ
    role_w3 = disnake.utils.get(member.guild.roles, id=0) # ID НУЖНОЙ РОЛИ
    if role_w1 in member.roles:
        await member.add_roles(role_w2)
        await channel.send(f"Администратор {ctx.author.mention} выдал 2й варн пользователю {member.mention} по причине {reason}.")
    elif role_w1 and role_w2 in member.roles:
        await member.add_roles(role_w3)
        await channel.send(f"Администратор {ctx.author.mention} выдал 3й варн пользователю {member.mention} по причине {reason}.")
        await channel.send(f"ВНИМАНИЕ! У ПОЛЬЗОВАТЕЛЯ {member.mention} ИМЕЕТСЯ 3 ПРЕДУПРЕЖДЕНИЯ, ПРИ ВЫДАЧИ ЕЩЕ ОДНОГО ПРЕДУПРЕЖДЕНИЯЕ {member.mention} БУДЕН КИКНУТ С СЕРВЕРА!")
    elif role_w1 and role_w2 and role_w3 in member.roles:
        await channel.send(f"Пользователь {member.mention} был кикнут ботов из-за того, что у {member.mention} имел 3 варна.")
        await member.kick(reason="3 Варна.")
    else:
        await member.add_roles(role_w1)
        await channel.send(f"Администратор {ctx.author.mention} выдал 1й варн пользователю {member.mention} по причине {reason}.")

# Помощь
# плашка с командами
@bot.command(name="help")
async def help(ctx):
    embed = Embed(
        title="Команды",
        description=
                    f"Префикс - {bot.command_prefix} (точка)"
                    f"\n\n"
                    f"Для администрации:"
                    f"\n"
                    f"Бан - ban <name> <reason>"
                    f"\n"
                    f"Кик - kick <name> <reason>"
                    f"\n"
                    f"Мьют - mute <name> <time in seconds> <reason>"
                    f"\n"
                    f"Снять мьют - unmute <name> <reason>"
                    f"\n"
                    f"Очистить чат - clear <amount>"
                    f"\n\n"
                    f"Статистика:"
                    f"\n"
                    f"Твоя статистика - mystats"
                    f"\n\n"
                    f"Фан:"
                    f"\n"
                    f"Запретка от бота - zapretka"
                    f"\n\n"
                    f"Помощь:"
                    f"\n"
                    f"Все команды - help",
        color=0xFFC000,
    )
    await ctx.message.delete()
    await ctx.send(embed=embed)

# Статистика
@bot.command(name="mystats")
async def mystats(ctx):
    emb = Embed(title=f"Статистика {ctx.author}", color=0xFFC000)

    emb.set_footer(text=ctx.author, icon_url=ctx.author.avatar)

    await ctx.message.delete()
    await ctx.send(embed=emb)

# Сообщения от бота
@bot.command(name="zapretka")
async def zapretka(ctx):
    await ctx.message.delete()
    await ctx.send(random.choice(CENSORED_WORDS))

bot.run("TOKEN")
