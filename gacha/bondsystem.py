import discord
from discord.ext.commands import CheckFailure
from discord.ext.commands.errors import BadArgument
import asyncio
import json
import logging
from random import choice

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


    def __init__(self, user: discord.User):
        self.user = user
        self.config = Config.get_conf(
            self, identifier=3169503212009969, force_registration=True
        )
        self.inventory = {}
        self.wishlist = {}

    def __str__(self):
        return (
            "Name {}\n"
            "Inventory: {}\n"
            "Wishlist: {}".format(self.user, self.inventory, self.wishlist)
        )

    def __repr__(self):
        return "{} - {} - {}".format(
            self.user, self.inventory, self.wishlist,
        )

    async def _send_message(channel, message):
        """Sends a message"""

        em = discord.Embed(description=message, color=discord.Color.green())
        await channel.send(embed=em)

    async def _load_card_list(self):
        """reloads the card list"""
        card_data_fp = bundled_data_path(self) / "default" / "cards.json"
        with card_data_fp.open() as json_data:
            self.card_data = json.load(json_data)

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
        await self._load_card_list()

        card_options = self.card_data["cards"]

        for x in range(0, amount):
            await ctx.send("command run " + str(x + 1))
            cardrolled = choice(card_options)
            em = discord.Embed(color=discord.Color.green())  # , description='\a\n')
            em.set_thumbnail(url=cardrolled["image"])
            em.set_author(name=cardrolled["name"])
            em.add_field(name="series:",value=cardrolled["series"])
            await ctx.send(embed=em)
#            await self.config.user(self.user).inventory.append