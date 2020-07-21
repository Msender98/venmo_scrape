from venmo_scrape import Venmo_Scrape_Client
import pandas as pd
import config


'''
Script to pull data from venmo's api and save it locally. 
'''

access_token = Venmo_Scrape_Client.get_access_token(username = config.username,
                                        password = config.password, device_id = config.device_id)

scrape = Venmo_Scrape_Client(access_token = access_token)


#initial user
my_user = scrape.user.get_my_profile()

user_df, transaction_df, new_user_ids, error_ids = scrape.scrape_data_to_df(user = my_user)

print(new_user_ids)

user_df.to_csv('venmo_users.csv')
transaction_df.to_csv('venmo_transactions.csv')

scrape.log_out(f'Bearer {access_token}')



