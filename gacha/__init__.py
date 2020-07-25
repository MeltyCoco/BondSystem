from .bondsystem import Bondsystem
from redbot.core import data_manager


async def setup(bot):
    tycoon = Bondsystem(bot)
    data_manager.bundled_data_path(tycoon)
    bot.add_cog(Bondsystem)