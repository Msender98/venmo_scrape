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


#initial user
my_user = scrape.user.get_my_profile()
transactions, users_initial = scrape.user_transaction_scrape(my_user)

#user dataframe initialization
user_df = pd.DataFrame(scrape.user_scrape(user = my_user), index = [0])
transaction_df = pd.DataFrame(scrape.transaction_scrape(transactions[0]), index = [0])

#Sets tracking what has been added to the dataframes:
user_set = {my_user.id}
transaction_set = {transactions[0].id}

for user in users_initial:
    if user.id not in user_set:
        user_df = user_df.append(scrape.user_scrape(user = user), ignore_index = True)
        user_set = user_set.union({user.id})

for transaction in transactions:
    if transaction.id not in transaction_set:
        transaction_df = transaction_df.append(scrape.transaction_scrape(transaction = transaction), ignore_index = True)
        transaction_set = transaction_set.union(transaction.id)

user_df.to_csv('venmo_users.csv')
transaction_df.to_csv('venmo_transactions.csv')

scrape.log_out(f'Bearer {access_token}')



