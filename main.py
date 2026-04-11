import os
import discord
import asyncio
import time
from flask import Flask
from threading import Thread

# ===== WEB (Railway) =====
app = Flask(__name__)

@app.route("/")
def home():
    return "OK", 200

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

def start_web():
    Thread(target=run_web, daemon=True).start()

start_web()

# ===== DISCORD =====
client = discord.Client(self_bot=True)

# ===== CONFIG =====
prefix = "."
start_time = time.time()

# ===== STATUS COM UPTIME =====
async def rotacao_status():
    await client.wait_until_ready()
    while True:
        try:
            tempo = int(time.time() - start_time)

            horas = tempo // 3600
            minutos = (tempo % 3600) // 60
            segundos = tempo % 60

            uptime = f"{horas}h {minutos}m {segundos}s"

            await client.change_presence(
                status=discord.Status.online,
                activity=discord.Activity(
                    type=discord.ActivityType.playing,
                    name=f"After Effects 2023"
                )
            )

            await asyncio.sleep(15)

        except Exception as e:
            print("Erro status:", e)
            await asyncio.sleep(5)

# ===== EVENTOS =====
@client.event
async def on_ready():
    print(f"🟢 Logado como {client.user}")
    client.loop.create_task(rotacao_status())

@client.event
async def on_message(message):
    if message.author.id != client.user.id:
        return

    content = message.content.strip()
    print("COMANDO:", content)

    # ===== .setstatus =====
    if content.startswith(f"{prefix}setstatus"):
        try:
            args = content.split()

            if len(args) < 2:
                await message.edit(content="Uso: .setstatus online/dnd/idle/invisible")
                return

            status_map = {
                "online": discord.Status.online,
                "idle": discord.Status.idle,
                "dnd": discord.Status.dnd,
                "invisible": discord.Status.invisible
            }

            status_arg = args[1].lower()

            if status_arg in status_map:
                await client.change_presence(status=status_map[status_arg])
                await message.edit(content=f"Status: {status_arg}")
            else:
                await message.edit(content="Status inválido")

        except Exception as e:
            await message.edit(content=f"Erro: {e}")

    # ===== .say =====
    elif content.startswith(f"{prefix}say"):
        try:
            args = content.split(" ", 2)

            if len(args) == 2:
                try:
                    await message.delete()
                except:
                    pass
                await message.channel.send(args[1])
                return

            if args[1].isdigit():
                canal = client.get_channel(int(args[1]))
                texto = args[2] if len(args) > 2 else "..."

                if canal:
                    try:
                        await message.delete()
                    except:
                        pass
                    await canal.send(texto)
                else:
                    await message.edit(content="Canal não encontrado")
            else:
                texto = content[len(f"{prefix}say "):]
                try:
                    await message.delete()
                except:
                    pass
                await message.channel.send(texto)

        except Exception as e:
            await message.edit(content=f"Erro: {e}")

# ===== RUN =====
token = os.environ.get("TOKEN")

if not token:
    raise Exception("TOKEN não definido")

client.run(token)
