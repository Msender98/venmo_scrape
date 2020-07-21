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

new_new_user_ids = new_user_ids

for new_user_id in new_user_ids:
    user_df, transaction_df, new_users_id_add, error_id_add = scrape.scrape_data_to_df(user_id = new_user_id, user_df = user_df, transaction_df = transaction_df)
    new_new_user_ids = new_new_user_ids.union(new_users_id_add)
    error_ids = set(error_ids).union(error_id_add)

print(len(new_new_user_ids))

user_df.to_pickle('user_data.p')
transaction_df.to_pickle('transaction_data.p')

user_df.to_csv('venmo_users.csv')
transaction_df.to_csv('venmo_transactions.csv')

scrape.log_out(f'Bearer {access_token}')



