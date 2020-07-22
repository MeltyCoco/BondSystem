from .bondsystem import Bondsystem

async def setup(bot):
    bot.add_cog(Bondsystem(bot))