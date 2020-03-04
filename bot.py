# coding: UTF-8
#heroku PostgreSQLに接続
import os
import discord
from discord.ext import commands
import asyncpg
from yarl import URL
#TOKENを環境変数から取得
TOKEN = os.environ.get("DISCORD_TOKEN")
bot = commands.Bot(command_prefix='t/',help_command=None)

#herokuではDBのurlが変わるため環境変数から取得
dburl = URL(os.environ.get("DATABASE_URL"))
host = dburl.host
user = dburl.user
database = dburl.path[1:]
port = dburl.port
password = dburl.password
print('host = ' + str(host))
print('user = ' + str(user))
print('database = ' + str(database))
print('port = ' + str(port))
print('password = ' + str(password))
#DBに接続
async def DB(SQL):
    conn = await asyncpg.connect(
        host = host ,
        user = user, 
        database = database, 
        port = port, 
        password = password
        )
    #SQLを実行
    values = await conn.fetch(SQL)
    #接続を切る
    await conn.close()
    return values

#SQL文をdiscordから実行
@bot.command()
async def sql(ctx,*,SQL):
    msg = await DB(SQL)
    await ctx.send(msg)
    
#bot.run
bot.run(TOKEN)
