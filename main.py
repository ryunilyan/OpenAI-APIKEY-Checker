import disnake
from disnake.ext import commands
import aiohttp

api_url = "https://api.openai.com/v1/chat/completions"

# Discord Botのセットアップ
intents = disnake.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')


async def chatgpt_api_req(api_key, text, model):
    messages = [
        {"role": "system", "content": "Hello!"},
        {"role": "user", "content": text}
    ]
    payload = {
        "messages": messages,
        "max_tokens": 1000,
        "temperature": 1,
        "n": 1,
        "model": model
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(api_url, headers=headers, json=payload) as response:
            result = await response.json()
            print(result)
            return result, response.status

@bot.command()
async def api(ctx, api_key: str):
    async def test_api_request(api_key, model):
        try:
            result, status = await chatgpt_api_req(api_key, "hello", model)
            if status == 200:
                return ":green_circle:"
            else:
                return ":red_circle:"
        except Exception as e:
            print(f"Error: {e}")
            return ":red_circle:"

    gpt_3_5_status = await test_api_request(api_key, "gpt-3.5-turbo")
    gpt_4_status = await test_api_request(api_key, "gpt-4")
    await ctx.send(f"Key: {gpt_3_5_status}\nGPT-4: {gpt_4_status}")



bot.run("token")
