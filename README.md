# PokerBot



# Installation

## Starting Steps
### 1: Create a Discord Account
1. Visit [Discord.com](https://discord.com/) to register for an account.



### 2: Create/Use a server for the bot.

1. If you already have a server that you can invite a bot to, you may skip the following steps
1. On the Discord application, create a server by pressing the green plus icon located to the left, with the caption "Add a Server"
1. Then select "Create My Own" and select any prefered option. You may change the name of the server your creating. Afterwards, select the "Create" button.
1. You now have a server to run the bot on.

## Method 1: Invite the bot to your Discord Server  
1. Use this [Discord invite link](https://discord.com/api/oauth2/authorize?client_id=850462222508490803&permissions=8&scope=bot). 
1. You will be redirected to a Discord page that requests where the bot should operate. A list of servers you are a member of will be listed below. Select the appropriate server. 
1. Proceed through the steps they provide you. 
1. Once authorized, your bot has successfully been invited to your server. The bot should be online, which is depicted as a green dot beside the bot’s profile picture. This means that the bot is online and ready to operate. If the bot is offline (depicted as a gray dot), then the bot is offline and not ready to use; proceed to method number 2. 



## Method 2: Run the bot locally on your machine 
### Prerequisites
- Install [discord.py](https://discordpy.readthedocs.io/en/stable/intro.html) library.
- Clone the [repository](https://github.com/lolpre/PokerBot).

### Steps:

### 1: Make bot appication in developer's portal.

1. Go to Discord's [Developer Portal](https://discord.com/developers/applications)
1. Click the new application button and set any name for the application.
1. After creating the new application, click the menu and select the  section labeled "Bot". In this page select the "Add Bot" button and confirm.
1. You may set the username of the bot to anything, preferebly Poker Bot.

### 2: Collect Bot Token
1. Go to the Discord [Developer Portal](https://discord.com/developers/applications)
1. Go to the section labeled "Bot". 
1. Under Token, click on "Copy" and paste it into the source code. For Poker Bot, the token should be pasted in the pokerbot.py file, line 15: TOKEN = os.getenv("TOKEN"). Replace the TOKEN that is in quotes with the token you have copied. 



### 3: Invite the bot
1. Click on the Application you have created. 
1. Go to the section labeled "OAuth2". 
1. In scopes, click on the "Bot" check box. 
1. Copy the link created below the Scopes list, and go to the link. 
1. Refer to Method 1 for the remaining steps. 

### 4: Running the Bot
1. Run the pokerbot.py file on your local machine. 
1. Once the bot goes online (depicted with a green dot beside its profile picture), the bot is now available to use. Have fun playing Poker!



