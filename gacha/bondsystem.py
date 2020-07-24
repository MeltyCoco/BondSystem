import discord
from discord.ext.commands import CheckFailure
from discord.ext.commands.errors import BadArgument
import asyncio
import random
import json
import logging

from typing import Any, List

from redbot.core import Config, checks, commands, bank
from redbot.core.utils.chat_formatting import humanize_list
from redbot.core.utils.predicates import MessagePredicate
from redbot.core.data_manager import bundled_data_path, cog_data_path


from redbot.core.bot import Red

Cog: Any = getattr(commands, "Cog", object)

log = logging.getLogger("red.cogs.adventure")

class Bondsystem(Cog):
    """Marry shit"""

    __author__ = "MeltyCoco"
    __version__ = "0.0.1"


    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(
            self, identifier=3169503212009969, force_registration=True
        )

        self.config.register_member(
            # What cards you got
            inventory=[],
            # What you want
            wishlist=None,
        )

        self.card_data: dict = None

#    async def initialize(self):
#        await self.bot.wait_until_ready()
#        try:
#            with open("cog_data_path(self)/default/cards.json") as f:
#                self.card_data = json.load(f)
#        except Exception as err:
#            log.exception("There was an error starting up the cog", exc_info=err)

    @commands.group(autohelp=True)
    @checks.admin_or_permissions(manage_guild=True)
    async def bondset(self, ctx):
        """Settings for this gacha"""
        pass

    @bondset.command(name="toggle")
    async def bondset_toggle(self, ctx: commands.Context, on_off: bool = None):
        """Toggle Bond System for server

        If 'on_off' is not provided, the state will be flipped."""
        target_state = (
            on_off
            if on_off
            else not (await self.config.guild(ctx.guild).toggl())
        )
        await self.config.guild(ctx.guild).toggle.set(target_state)
        if target_state:
            await ctx.send("Bond System is now enabled.")
        else:
            await ctx.send("Bond System is now disabled.")

    @checks.is_owner()
    @bondset.command(name="rollprice")
    async def bondset_rollprice(self, ctx: commands.Context, price: int):
        """Set the price for rolling"""

        if price <= 0:
            await ctx.send("Why the fuck would I go into debt for their sorry ass?")
        await self.config.guild(ctx.guild).rollprice.set(price)
        await ctx.tick()

        #        @commands.command()
        #        async def wish(self, ctx: commands.Context, card: card.name = None):
        #            """Add a card to your wishlist"""

        #        if not await self.config.guild(ctx.guild).toggle():
        #            return await ctx.send("Bitch, you can't gacha in this server")
        #        if not card:
        #            await self.configmember(ctx.quthor).wishlist.set(None)

    @commands.command()
    async def gacharoll(self, ctx: commands.Context, amount: int = 1):
        """pulls a card from the current card list"""
        await ctx.send("command got")

        await self.bot.wait_until_ready()
        try:
            with open("cog_data_path(self)/default/cards.json") as f:
                self.card_data = json.load(f)
            await ctx.send("Read the file")
        except Exception as err:
            log.exception("There was an error starting up the cog", exc_info=err)
            await ctx.send("Failed to read file")
        await ctx.send("card list is processed")

        for x in range(0, amount):
            await ctx.send("command run " + str(x))
            await ctx.send(self.card_data[0])
#            tempcard = random.randint(0, len(self.card_data))
#            await ctx.send("The card you got was, " + self.card_data[tempcard] + " from the series " + self.card_data[tempcard].series)
