import discord
from discord.ext.commands import CheckFailure
from discord.ext.commands.errors import BadArgument
import asyncio
import random
import json

from typing import Any, List

from redbot.core import Config, checks, commands, bank
from redbot.core.utils.chat_formatting import humanize_list
from redbot.core.utils.predicates import MessagePredicate

from redbot.core.bot import Red

Cog: Any = getattr(commands, "Cog", object)


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

        self.cardlist: dict = None

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

       # cardlist = json.loads("cards.json")
        for x in range(0, amount - 1):
            tempcard = random.randint(0, 4)
            #ctx.send("The card you got was, " + cardlist[tempcard] + " from the series " + cardlist[tempcard].series)
            ctx.send("You would have pulled a " + tempcard)