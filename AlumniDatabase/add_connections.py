from AlumniDatabase.secrets import USERNAME, PASSWORD
from AlumniDatabase.AlumniFinder import LinkedInBot
import pandas as pd

# make the bot
bot = LinkedInBot()

# login
bot.login(USERNAME, PASSWORD)

# import the data
data = pd.read_excel(
    'AlumniDatabase/GUSIF Alumni Database.xlsx', sheet_name='Alumni')

# reassign the headers
data.columns = data.loc[4]

data = data.loc[5:]

links = data['Linkedin Link']

for link in links:
    bot.connect(link)

bot.quit()
