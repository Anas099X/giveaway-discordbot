import discord, os, random
from giveaway import Giveaway
from discord import app_commands
from dotenv import load_dotenv
from discord.ext import tasks
from datetime import datetime, timedelta

load_dotenv()
intents = discord.Intents.default()

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
giveaway_group = app_commands.Group(name="giveaway", description="Commands related to giveaways")

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    check_giveaways.start()
    await tree.sync()


@tasks.loop(seconds=5)
async def check_giveaways():
    giveaway_table = Giveaway()  # from database
    giveaway_list = giveaway_table.get_all()
    for giveaway in giveaway_list:
        if giveaway[3] <= datetime.now():

            #get giveaway msg channel
            channel = client.get_channel(giveaway[4])

            #get giveaway msg itself
            main_msg = await channel.fetch_message(giveaway[5])

            #check giveaway entries
            if giveaway[1]:
             winners_list = pick_winner(giveaway[1],giveaway[2])
             await main_msg.reply(f"**🎉 Winners are {' '.join(f'<@{w}>' for w in winners_list)}** 🎉")
            else:
             await main_msg.reply("**🎉 No one entered the giveaway! 🎉**")

            #remove giveaway after done
            giveaway_table.delete(giveaway[0])


def pick_winner(users,winners_count):
   
   #makes sure that winners count isnt larger than entires
   if winners_count > len(users):
    winners_count = len(users)

   winners = random.sample(users,winners_count)
   return winners
   

def format_input_time(giveaway):
   giveaway_time = giveaway
   num, unit = giveaway_time.split()
   num = int(num)

   if unit in ["second","seconds","s"]:
      return timedelta(seconds=num)
   elif unit in ["minute","minutes","m"]:
      return timedelta(minutes=num)
   elif unit in ["hour","hours","h"]:
      return timedelta(hours=num)
   elif unit in ["day","days","d"]:
      return timedelta(days=num)
   

def endtime(duration):

 end_time = datetime.now() + duration

 return end_time   
      


def format_giveaways(giveaways):
    formatted = []
    if giveaways:
     for giveaway in giveaways:
        formatted.append(f"- {giveaway[0]} Entries: {len(giveaway[1])} Winners: {giveaway[2]} End Time: {giveaway[3]}")
     return "\n".join(formatted)
    else:
        return "No giveaways found."

    
# add task command
@giveaway_group.command(name="create",description="Create a giveaway")
async def add_giveaway_command(interaction: discord.Interaction,name: str, duration: str, winners: int):

    input_duration = format_input_time(duration)
    embed_time = str(input_duration).split(",")[0]

    msg_embed = discord.Embed(title="Giveaway Created!", description=f"Giveaway Name: {name}\nDuration: {embed_time}\nWinners: {winners}\n\nCreated on {datetime.now().strftime("%d/%m/%Y")}", color=discord.Color.green())
    
    class Enter_Giveaway(discord.ui.View):
        @discord.ui.button(label="Enter Giveaway", style=discord.ButtonStyle.green, custom_id="enter")
        async def enter_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            giveaway = Giveaway()
            giveaway_data = giveaway.get_one(name)
            print(giveaway_data)
            entries = giveaway_data[0][1]
            if str(interaction.user.name) in entries:
                await interaction.response.send_message("You have already entered the giveaway!", ephemeral=True)
                return
            entries.append(str(interaction.user.id))
            giveaway.update(name, "entries", entries)
            await interaction.response.send_message("You have entered the giveaway!", ephemeral=True)

    giveaway = Giveaway()
    await interaction.response.send_message(embed=msg_embed, view=Enter_Giveaway())
    giveaway_message = await interaction.original_response()
    giveaway.create(name,[], winners, endtime(input_duration), giveaway_message.channel.id, giveaway_message.id)


# view tasks command
@giveaway_group.command(name="list",description="List giveaways")
async def view_giveaways_command(interaction: discord.Interaction):
    
    giveaways = Giveaway().get_all()
    
    class ViewTasks(discord.ui.LayoutView):
    
     container = discord.ui.Container(
        

        discord.ui.TextDisplay(format_giveaways(giveaways))
    )


   


    await interaction.response.send_message(view=ViewTasks())



# delete giveaway command 
@giveaway_group.command(name="end",description="Delete a giveaway")
async def end_giveaway_command(interaction: discord.Interaction, giveaway_name: str, forced: bool = False):
    giveaway = Giveaway()
    if forced:
     giveaway.delete(giveaway_name)
     await interaction.response.send_message("Giveaway ended without winners!", ephemeral=True)
    else:
       giveaway.update(giveaway_name,"end_time",datetime.now())
       await interaction.response.send_message("Ended giveaway. Announcing winner...", ephemeral=True) 


tree.add_command(giveaway_group)


client.run(os.getenv("DISCORD_TOKEN"))
