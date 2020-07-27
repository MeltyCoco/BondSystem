import discord
from discord.ext.commands import CheckFailure
from discord.ext.commands.errors import BadArgument
import asyncio
import json
import logging
from random import choice, choices

from typing import Any, List

from redbot.core.utils.menus import menu, commands, DEFAULT_CONTROLS
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

        self.config.register_guild(
            toggle=True,
            rollprice=100000
        )

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

    async def _grab_random_rarity(self):
        """grabs a random rarity"""
        # EVERYTIME YOU ADD A RARITY, BE SURE TO ADD IT HERE AND WEIGHT IT
        raritylist = ["normal", "rare", "super rare", "super super rare", "ultra rare"]
        raritygrabbed = choices(raritylist, weights=[40, 50, 8, 2, 1])
        raritystring = raritygrabbed[0]
        return raritystring

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

        # every ten rolls, give grant 1 extra roll!
        if (int(amount / 10) >= 1):
            amount += int(amount / 10)

        # Creates a rarity list, and then give it weights so that more common are more common
        raritylist = ["normal", "rare", "super rare", "super super rare", "ultra rare"]
        raritygrabbed = choices(raritylist, weights=[40, 50, 7, 2, 1], k=amount)

        # Start creating pages for the embed command
        allcard = []

        await ctx.send("You've rolled " + str(amount) + " of times")
        for x in range(0, amount):
            raritystring = raritygrabbed[x]
            # grabs a rarity from the rarity list above
            card_options = self.card_data[raritystring]

            # Grabs a random card of the rarity grabbed and then creates the embed card for that card
            cardrolled = choice(card_options)
            embed = discord.Embed(title=cardrolled["name"], description=cardrolled["series"])
            embed.set_thumbnail(url=cardrolled["image"])
            embed.add_field(name="Rarity", value=raritystring, inline=False)
            embed.add_field(name="Birthday", value=cardrolled["birthday"], inline=False)
            embed.add_field(name="Quote", value=cardrolled["quote"], inline=False)
            embed.set_footer(text="I know you want another gacha hit")

            # adds the card to the pages
            allcard.append(embed)
        # Print out the pages as a menu (pages doesn't work for some reason)
        await menu(ctx, pages=allcard, controls=DEFAULT_CONTROLS, message=None, page=0, timeout=60)
