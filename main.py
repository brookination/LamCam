import cv2
import discord
from discord.ext import commands, tasks
import random
import os
import sys
import datetime

if not os.path.exists(os.path.realpath("catImages")):
    os.path.join(os.path.realpath("catImages"))

TOKEN = ""

try:
    with open('toyken', 'r') as tokenfile:
        TOKEN = tokenfile.read()
except:
    with open('toyken', 'x') as tokenfile:
        tokeninput = input("Put your token into the console: ")
        tokenfile.write(tokeninput)
        TOKEN = tokeninput
        print("Continuing script. If this doesn't work, then you didn't put your token in right.")


saved_context = None

# Initialize the bot
bot = commands.Bot(command_prefix='cat', intents=discord.Intents.all())

# Function to capture image from webcam
def capture_image():
    cap = cv2.VideoCapture(0)  # Open the webcam (change the index if you have multiple webcams)
    
    if not cap.isOpened():
        print("Error: Couldn't open webcam")
        return None
    
    # Capture a frame from the webcam
    ret, frame = cap.read()
    
    # Release the webcam
    cap.release()
    
    # Check if the frame was captured successfully
    if not ret:
        print("Error: Couldn't capture frame")
        return None
    
    return frame

@bot.command(name="Ctx")
async def get_context(ctx):
    global saved_context
    saved_context = ctx
    if not ctx == None:
        await ctx.send("Context saved! The 12:00 command is available!")

@tasks.loop(minutes=10)
async def send_12msg():
    global saved_context

    current_time = datetime.datetime.now(datetime.timezone.utc).astimezone(datetime.timezone(datetime.timedelta(hours=-6))) # This giant line of code makes me scared
    if current_time.hour == 12 or current_time.hour == 0:
        if saved_context == None:
            print("Context not saved. send_12msg() isn't available.")
            return
        send_image(saved_context, True)




@bot.command(name='Cam')
async def send_image(ctx, *twelve_msg):
    global saved_context  # Use the global variable
    # Capture image from webcam
    await ctx.typing()
    image_path = "catImages/" + str(random.randrange(10000000000000,99999999999999)) + ".jpg" # I *really* hope this isn't a problem later.
    image = capture_image()
    
    if image is None:
        await ctx.send("Error: Couldn't capture image")
        return
    
    # Save the image to a file
    cv2.imwrite(image_path, image)
    
    # Send the image to Discord
    with open(image_path, 'rb') as file:
        if twelve_msg:
            allowed_mentions = discord.AllowedMentions(everyone = True)
            await ctx.send(content="@everyone Car", file=discord.File(file), allowed_mentions = allowed_mentions)
        else:
            await ctx.send(content=ctx.author.mention, file=discord.File(file))
            if saved_context == None:
                await ctx.send("Please run \"catCtx\" to use the 12:00 daily function!")
        
    
    print("Image sent successfully")

# Command to trigger image capture and send

async def send_image_command(ctx):
    await send_image(ctx)

# Event handler for bot startup
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Run the bot
bot.run(TOKEN)
