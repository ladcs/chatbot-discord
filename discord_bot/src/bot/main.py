from typing import Dict
import discord
import requests
from bot.env_loader import token, user_id, url, url_test


class MyClient(discord.Client):
    def __init__(self) -> None:
        intents: discord.Intents = discord.Intents.all()
        super().__init__(intents=intents)
        self.tree: discord.app_commands.CommandTree = discord.app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        await self.tree.sync()

    async def on_ready(self) -> None:
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")


client: MyClient = MyClient()


async def hello_handler(interaction: discord.Interaction) -> None:
    await interaction.response.send_message(
        f"Hello, {interaction.user.mention}!"
    )


async def prompt_handler(
    interaction: discord.Interaction,
    prompt: str,
    url_webhook: str = url
) -> None:
    if str(interaction.user.id) != user_id: # esse if é para restringir o uso do bot pelo id do usuário definido no .env
        await interaction.response.send_message(
            f"sorry {interaction.user.mention}, but I can't pay for all this token :'("
        )
        return
    guild_id = str(interaction.guild.id)
    channel_id = str(interaction.channel.id)
    data: Dict[str, str] = {
        "prompt": prompt,
        "user_id": str(interaction.user.id),
        "user_name": interaction.user.mention,
        "guild_id": guild_id,
        "channel_id": channel_id,
    }
    try:
        await interaction.response.send_message(
            prompt
        )
        response: requests.Response = requests.post(url_webhook, json=data)
        response.raise_for_status()

    except Exception as e:
        await interaction.followup.send(
            f"sorry {interaction.user.mention}, I can't cause: {e}"
        )


@client.tree.command(name="hello", description="say hello")
async def hello(interaction: discord.Interaction) -> None:
    await hello_handler(interaction)


@client.tree.command(name="prompt", description="call prompt")
async def prompt(
    interaction: discord.Interaction,
    prompt: str
) -> None:
    await prompt_handler(interaction, prompt)

@client.tree.command(name="test", description="call prompt test")
async def prompt(
    interaction: discord.Interaction,
    prompt: str
) -> None:
    await prompt_handler(interaction, prompt, url_test)


if __name__ == "__main__":
    client.run(token)
