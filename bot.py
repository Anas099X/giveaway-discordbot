import discord, os
from giveaway import Giveaway
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.default()

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
giveaway_group = app_commands.Group(name="giveaway", description="Commands related to giveaways")

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    await tree.sync()


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

    msg_embed = discord.Embed(title="Giveaway Created!", description=f"Giveaway Name: {name}\nDuration: {duration}\nWinners: {winners}", color=discord.Color.green())
    
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
            entries.append(str(interaction.user.name))
            giveaway.update(name, "entries", entries)
            await interaction.response.send_message("You have entered the giveaway!", ephemeral=True)

    giveaway = Giveaway()
    giveaway.create(name,[], winners, duration)
    await interaction.response.send_message(embed=msg_embed, view=Enter_Giveaway()) 


# view tasks command
@giveaway_group.command(name="list",description="List giveaways")
async def view_giveaways_command(interaction: discord.Interaction):
    
    giveaways = Giveaway().get_all()
    
    class ViewTasks(discord.ui.LayoutView):
    
     container = discord.ui.Container(
        

        discord.ui.TextDisplay(format_giveaways(giveaways)),
        discord.ui.Separator(),
        discord.ui.ActionRow(
                discord.ui.Button(label="Back", style=discord.ButtonStyle.gray,custom_id="back"),
                discord.ui.Button(label="Next", style=discord.ButtonStyle.green,custom_id="next")
        ))
     
     @discord.ui.button(custom_id="next")
     async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        start_page_index = start_page_index + 10
        end_page_index = end_page_index + 10
        await interaction.response.edit_message(view=ViewTasks())

     @discord.ui.button(custom_id="back")
     async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        start_page_index = start_page_index - 10
        end_page_index = end_page_index - 10
        await interaction.response.edit_message(view=ViewTasks())
   


    await interaction.response.send_message(view=ViewTasks())



# delete giveaway command 
@giveaway_group.command(name="delete",description="Delete a giveaway")
async def delete_giveaway_command(interaction: discord.Interaction, giveaway_name: str, forced: bool = False):
    giveaway = Giveaway()
    giveaway.delete(giveaway_name)
    await interaction.response.send_message("Giveaway deleted!", ephemeral=True)


tree.add_command(giveaway_group)


client.run(os.getenv("DISCORD_TOKEN"))
