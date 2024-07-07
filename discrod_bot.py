import logging
import asyncio

import discord

import config


class DiscordBot:
    def __init__(self):
        self.discord_bot = None
        self.logger = logging.getLogger("discord-bot")

    async def _send_message(self, channel_id, message):
        @self.discord_bot.event
        async def on_ready():
            channel = self.discord_bot.get_channel(channel_id)
            if channel:
                await channel.send(message)
                self.logger.debug(f"message to channel {channel_id} sent")
            else:
                self.logger.error(f"Channel {channel_id} not found")

            await self.discord_bot.close()

        await self.discord_bot.start(config.DISCORD_BOT_TOKEN)
        await self.discord_bot.http._HTTPClient__session.close()

    def send_message(self, channel_id, message):
        try:
            self.discord_bot = discord.Client(intents=discord.Intents.default())
            asyncio.run(self._send_message(channel_id, message))

        except Exception:
            self.logger.exception(f"Error while sending message to {channel_id}, continuing")
