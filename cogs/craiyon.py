import discord
from discord.ext import commands, tasks

from cogs.utils.utils import NoImageError, generate_image


class Craiyon(commands.Cog):
    image_context: commands.Context = None
    running: bool = False

    @commands.Cog.listener()
    async def on_ready(self):
        self._draw.start()

    @tasks.loop(seconds=1)
    async def _draw(self) -> None:
        if self.image_context is not None:
            self.running = True

            message = self.image_context.message
            message_content = " ".join(message.content.split(" ")[1:])

            craiyon_embed = discord.Embed(
                title=f"Generating {message_content}",
                url="https://craiyon.com",
                description="Craiyon is thinking... (This may take up to 3 minutes)",
                color=0xffae00
            )
            wait = await message.reply(embed=craiyon_embed)
            print(f"Requesting {message_content}")

            try:
                file_path = await generate_image(message_content)
                print('Got Image | Sending...')
                await self.image_context.message.reply(file=discord.File(file_path))
            except NoImageError:
                embed = discord.Embed(
                    title="Error",
                    url="https://craiyon.com",
                    description="An Error Occurred | This may be due to mass requests, "
                                "consider waiting a few minutes before retrying",
                    color=0xffae00
                )
                await message.channel.send(embed=embed)

            await wait.delete()

            self.running = False
            self.image_context = None
            self.prompt = None

    @commands.command(name="draw", aliases=["d", "craiyon"])
    async def draw(self, ctx: commands.Context) -> None:
        """
        Generates images using https://craiyon.com
        e.g `c!draw red tree` will generate a red tree using https://craiyon.com,
        """

        message = ctx.message

        if not self.running:
            self.image_context = ctx
        else:
            await message.channel.send('Bot currently in use. Please wait...')

    @commands.slash_command(name="drawing", description="slash command for draw")
    async def drawing(self, ctx: discord.ApplicationContext, prompt: discord.Option(str)):
        if not self.running:
            self.running = True
            craiyon_embed = discord.Embed(
                title=f"Generating {prompt}",
                url="https://craiyon.com",
                description="Craiyon is thinking... (This may take up to 3 minutes)",
                color=0xffae00
            )
            await ctx.respond(embed=craiyon_embed)
            print(f"Requesting {prompt}")
            try:
                file_path = await generate_image(prompt)
                print('Got Image | Sending...')
                await ctx.respond(file=discord.File(file_path))
            except NoImageError:
                embed = discord.Embed(
                    title="Error",
                    url="https://craiyon.com",
                    description="An Error Occurred | This may be due to mass requests, "
                                "consider waiting a few minutes before retrying",
                    color=0xffae00
                )
                await ctx.respond(embed=embed)
            self.running = False
        else:
            await ctx.respond('Bot currently in use. Please wait...')
