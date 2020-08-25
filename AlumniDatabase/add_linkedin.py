from AlumniDatabase.AlumniFinder import LinkedInBot
from AlumniDatabase.secrets import LINKEDIN_USERNAME, LINKEDIN_PASSWORD
import pandas as pd
import sys


def main(data):
    # load the data into pandas
    df = pd.read_csv(data)

    # create a bot (and login)
    bot = LinkedInBot()
    bot.login(LINKEDIN_USERNAME, LINKEDIN_PASSWORD)
    input('Click enter when captcha is broken')

    # iterate over all the rows of the df
    for index, row in df.iterrows():
        # get the necessary data
        name = row['Name']
        profile = row['LinkedIn Profile']

        # search the term if there is no profile yet
        if pd.isnull(profile):
            print(f"Checking data for {name}")
            search = f"{name} Georgetown"
            new_profile = bot.find_best_match(search)
            df.loc[index, 'LinkedIn Profile'] = new_profile

            df.to_csv(data, index=False)

    bot.quit()


if __name__ == '__main__':
    data = sys.argv[1].strip().replace('\\', '')
    main(data)
