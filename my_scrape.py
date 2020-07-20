from venmo_scrape import Venmo_Scrape_Client
import pandas as pd
import config


'''
Script to pull data from venmo's api and save it locally.

Not close to working!
'''

access_token = Venmo_Scrape_Client.get_access_token(username = config.username,
                                        password = config.password, device_id = config.device_id)

scrape = Venmo_Scrape_Client(access_token = access_token)



my_user = scrape.user.get_my_profile()

#example methods from Venmo_Scrape_Client
# print(scrape.user_scrape(user = my_user))
# transactions = scrape.user.get_user_transactions(user = my_user)
# #print(transactions)
# print(scrape.transaction_scrape(transactions[0]))


#One dataframe to store users information


user_df = pd.DataFrame(scrape.user_scrape(user = my_user), index = [0])

transactions, users_initial = scrape.user_transaction_scrape(my_user)



#One dataframe to store transactions
transaction_df = pd.DataFrame()

print(user_df)



scrape.log_out(f'Bearer {access_token}')



