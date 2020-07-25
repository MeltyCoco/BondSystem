from .bondsystem import Bondsystem
from redbot.core import data_manager


async def setup(bot):
    bond = Bondsystem(bot)
    data_manager.bundled_data_path(bond)
    bot.add_cog(bond)