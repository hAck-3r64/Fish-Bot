import aiofiles
import discord
import random
import json
from discord.ext import commands

fishList = []

roastList = ["Why so sad? Why? Why eat leaf your whole life hiyaaa, no be vegan or vegetarian, you get to have better life.",
             "Why not get A+? Why? You got B+, failure FAILURE! Hiyaaa my motha would have spank me with stick already hiyaaa.",
             "You're an Asian not a Bsian.",
             "Why so fat? Why? Did you eat the whole farm? Mulan would have sang a song if she saw you. *”Ancestors feel my pain, why does this person look like a chimpanzee? Why did they eat the cake and got the diabetes?”*",
             "When you cook, you hear sizzling, I hear my ancestors cry.",
             "NO No why do you put chili jam?! WHY are you a JAMIE OLIVER fan? Hiyaaa, I heard of chili oil, chili sauce and chili flakes, not chili jam what the hell. What now are you going to put peanut butter? Hiyaaa",
             "https://www.youtube.com/watch?v=-UsLpDdkGaU",
             "Why you so ugly? Why you look hairless? I should have threw you in trash can already. Hiyaa dont look like this :SExyeevee:",
             "You can't compare to me <@159985870458322944> you failure, can't even roast like me hiyaa my matha would have thrown me in trash can already hiyaa",
             "DONT MAKE ME LOSE MY FACE FAILURE hiyaaa",
             "**EMOTiONaL DAMaGE**",
             "Why are you a failure? Why, why?",
             "FAILURE, you FAILURE, why are you like this hiyaaa",
             "I will send you to Jesus.",
             "Useless, I tell you to do something, and you do it like a snail hiyaaa, USELESS"]

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
client = discord.Client()
bot.warnings = {}  # guild_id: {member_id: [count, [(admin_id, reason)]]}

m = {}

@bot.event
async def on_ready():
    for guild in bot.guilds:
        async with aiofiles.open(f"{guild.id}.txt", mode="a") as temp:
            pass

        bot.warnings[guild.id] = {}

    for guild in bot.guilds:
        async with aiofiles.open(f"{guild.id}.txt", mode="r") as file:
            lines = await file.readlines()

            for line in lines:
                data = line.split(" ")
                member_id = int(data[0])
                admin_id = int(data[1])
                reason = " ".join(data[2:]).strip("\n")

                try:
                    bot.warnings[guild.id][member_id][0] = + 1
                    bot.warnings[guild.id][member_id][1].append((admin_id, reason))

                except KeyError:
                    bot.warnings[guild.id][member_id] = [1, [(admin_id, reason)]]

    print(bot.user.name + " is online.")


@bot.event
async def on_guild_join(guild):
    bot.warnings[guild.id] = {}

@bot.command()
@commands.has_permissions(administrator=True)
async def warn(ctx, member: discord.Member = None, *, reason=None):
    if member is None:
        return await ctx.send("The provided member could not be found or you forgot to provide one.")

    if reason is None:
        return await ctx.send("Please provide a reason for warning this user.")

    try:
        first_warning = False
        bot.warnings[ctx.guild.id][member.id][0] += 1
        bot.warnings[ctx.guild.id][member.id][1].append((ctx.author.id, reason))

    except KeyError:
        first_warning = True
        bot.warnings[ctx.guild.id][member.id] = [1, [(ctx.author.id, reason)]]

    count = bot.warnings[ctx.guild.id][member.id][0]

    async with aiofiles.open(f"{ctx.guild.id}.txt", mode="a") as file:
        await file.write(f"{member.id} {ctx.author.id} {reason}\n")

    await ctx.send(f"{member.mention} has {count} {'warning' if first_warning else 'warnings'}.")

@bot.command()
@commands.has_permissions(administrator=True)
async def warnings(ctx, member: discord.Member = None):
    if member is None:
        return await ctx.send("The provided member could not be found or you forgot to provide one.")

    embed = discord.Embed(title=f"Displaying Warnings for {member.name}", description="", colour=discord.Colour.red())
    try:
        i = 1
        for admin_id, reason in bot.warnings[ctx.guild.id][member.id][1]:
            admin = ctx.guild.get_member(admin_id)
            embed.description += f"**Warning {i}** given by: <@{admin_id}> for: *'{reason}'*.\n"
            i += 1

        await ctx.send(embed=embed)

    except KeyError:  # no warnings
        await ctx.send("This user has no warnings.")

@bot.command()
async def asianroast(ctx):
    roast = random.choice(roastList)
    return await ctx.send(roast)

@bot.command()
async def test(ctx):
    return await ctx.send(":shrexy:")

@bot.command()
@commands.has_role(943932225261539388)
async def hi(ctx):
    return await ctx.send("hi")

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def say(ctx, *, response):
    response = response.replace("(", "")
    response = response.replace(")", "")
    await ctx.channel.purge(limit=1)
    await ctx.send(response)

@bot.command()
@commands.has_permissions(administrator=True)
async def purge(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

@bot.command()
async def elder(ctx):
    await ctx.send("We remember the Elder.")

@bot.command()
async def furry(ctx):
    await ctx.send("No.")

@bot.command()
async def hug(ctx, *, response):
    response = response.replace("(", "")
    response = response.replace(")", "")
    await ctx.send(f"<@{ctx.message.author.id}> gives {response} a big hug!")

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def boop(ctx, *, response):
    randomPercent = random.randint(0, 100)
    response = response.replace("(", "")
    response = response.replace(")", "")
    await ctx.send(f"<@{ctx.message.author.id}> just booped {response} with {randomPercent}% of their power!")

@bot.command()
async def addquote(ctx, *, response):
    response = response.replace("(", "")
    response = response.replace(")", "")
    async with aiofiles.open("quotes.txt", mode="a") as file:
        await file.write(f"{response}\n")
    await ctx.send(f"Added quote '{response}'.")

@bot.command()
async def boost(ctx):
    role = discord.utils.get(ctx.guild.roles, name="Server Booster")
    if role in ctx.author.roles:
        await ctx.send("lol thx for boosting")
    if not role in ctx.author.roles:
        await ctx.send("chat the boost command does nothing")

@bot.command()
async def quotes(ctx):
    await ctx.send(file=discord.File('quotes.txt'))

@commands.guild_only()
@bot.command()
async def pronouns(ctx, member: discord.Member = None):
    if member is None:
        return await ctx.send("The provided member could not be found or you forgot to provide one.")
    mrole = discord.utils.get(ctx.guild.roles, name="He/Him")
    frole = discord.utils.get(ctx.guild.roles, name="She/Her")
    trole = discord.utils.get(ctx.guild.roles, name="They/Them")
    qrole = discord.utils.get(ctx.guild.roles, name="Pronouns: Ask Me")
    arole = discord.utils.get(ctx.guild.roles, name="Any Pronouns")
    urole = discord.utils.get(ctx.guild.roles, name="Pronouns: Unsure")
    if mrole in member.roles:
        await ctx.send(f"{member} uses He/Him pronouns.")
    if frole in member.roles:
        await ctx.send(f"{member} uses She/Her pronouns.")
    if trole in member.roles:
        await ctx.send(f"{member} uses They/Them pronouns.")
    if qrole in member.roles:
        await ctx.send(f"Ask {member} for their pronouns.")
    if arole in member.roles:
        await ctx.send(f"{member} uses any pronouns.")
    if urole in member.roles:
        await ctx.send(f"{member} is unsure of their pronouns.")
    if not mrole in member.roles and not frole in member.roles and not trole in member.roles and not qrole in member.roles and not arole in member.roles and not urole in member.roles:
        await ctx.send(f"I am unsure what {member}'s pronouns are.")

@commands.guild_only()
@bot.command()
async def sexuality(ctx, member: discord.Member = None):
    if member is None:
        return await ctx.send("The provided member could not be found or you forgot to provide one.")
    srole = discord.utils.get(ctx.guild.roles, name="Straight")
    grole = discord.utils.get(ctx.guild.roles, name="Gay")
    lrole = discord.utils.get(ctx.guild.roles, name="Lesbian")
    brole = discord.utils.get(ctx.guild.roles, name="Bisexual")
    prole = discord.utils.get(ctx.guild.roles, name="Pansexual")
    crole = discord.utils.get(ctx.guild.roles, name="Cisgender")
    arole = discord.utils.get(ctx.guild.roles, name="Asexual")
    qrole = discord.utils.get(ctx.guild.roles, name="Queer")
    urole = discord.utils.get(ctx.guild.roles, name="SO: Unsure")
    if srole in member.roles:
        await ctx.send(f"{member} is straight.")
    if grole in member.roles:
        await ctx.send(f"{member} is homosexual.")
    if lrole in member.roles:
        await ctx.send(f"{member} is lesbian.")
    if brole in member.roles:
        await ctx.send(f"{member} is bisexual.")
    if prole in member.roles:
        await ctx.send(f"{member} is pansexual.")
    if crole in member.roles:
        await ctx.send(f"{member} is cisgender.")
    if arole in member.roles:
        await ctx.send(f"{member} is asexual.")
    if qrole in member.roles:
        await ctx.send(f"{member} is queer.")
    if urole in member.roles:
        await ctx.send(f"{member} is unsure of their sexuality.")
    if not srole in member.roles and not grole in member.roles and not lrole in member.roles and not brole in member.roles and not prole in member.roles and not crole in member.roles and not arole in member.roles and not qrole in member.roles and not urole in member.roles:
        await ctx.send(f"I am unsure what {member}'s sexuality is.")

@commands.guild_only()
@bot.command()
async def genderidentity(ctx, member: discord.Member = None):
    if member is None:
        return await ctx.send("The provided member could not be found or you forgot to provide one.")
    nrole = discord.utils.get(ctx.guild.roles, name="Non-Binary")
    trole = discord.utils.get(ctx.guild.roles, name="She/Her")
    if nrole in member.roles:
        await ctx.send(f"{member} is Non-Binary.")
    if trole in member.roles:
        await ctx.send(f"{member} is Transgender.")
    if not nrole in member.roles and not trole in member.roles:
        await ctx.send(f"I am unsure what {member}'s gender identity is. Try using !sexuality to see if they may be cisgender.")

@bot.command()
async def friendcode(ctx):
    await ctx.send("be mah fren 1212760143")

@bot.command()
async def commandslist(ctx):
    embed = discord.Embed(title="Fish Bot commands", description="", colour=discord.Colour.random())
    embed.description = "-!warn (admin only)\n" \
                        "Warns a member.\n" \
                        "\n" \
                        "-!warnings (admin only)\n" \
                        "Displays a member's warnings.\n" \
                        "\n" \
                        "-!asianroast\n" \
                        "**EMOTIONAL DAMAGE**\n" \
                        "\n" \
                        "-!test\n" \
                        "test\n" \
                        "\n" \
                        "-!hi (Supreme fish leader only)\n" \
                        "hi\n" \
                        "\n" \
                        "-!say\n" \
                        "Makes the bot say whatever you want.\n" \
                        "\n" \
                        "-!purge (admin only)\n" \
                        "Deletes the set amount of messages.\n" \
                        "\n" \
                        "-!elder (Twitch command)\n" \
                        "We remember the Elder.\n" \
                        "\n" \
                        "-!furry (Twitch command)\n" \
                        "No furry, we not furry.\n" \
                        "\n" \
                        "-!hug (Twitch command)\n" \
                        "Lets you give hugs!\n" \
                        "\n" \
                        "-!boop (Twitch command)\n" \
                        "Lets you boop with a percentage of your power!\n" \
                        "\n" \
                        "-!addquote (Twitch command)\n" \
                        "Adds a quote to the list.\n" \
                        "\n" \
                        "-!quotes (Twitch command)\n" \
                        "Shows the list of quotes.\n" \
                        "\n" \
                        "-!boost (Twitch command)\n" \
                        "chat the boost command does nothing\n" \
                        "\n" \
                        "-!pronouns\n" \
                        "Displays a member's pronouns.\n" \
                        "\n" \
                        "-!sexuality\n" \
                        "Displays a member's sexuality.\n" \
                        "\n" \
                        "-!genderidentity\n" \
                        "Displays a member's gender identity.\n" \
                        "\n" \
                        "-!friendcode\n" \
                        "Shows @hAck_3r64's Steam friend code.\n"
    embed.set_footer(text="Fish Bot is by @hAck_3r64\n"
                          "Fish Bot V1.3.3")
    await ctx.send(embed=embed)


bot.run("TOKEN")
