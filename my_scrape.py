from venmo_scrape import Venmo_Scrape_Client
import pandas as pd
import config
import pickle 

'''
Script to pull data from venmo's api and save it locally. 
'''
def scrape_level(users, levels, user_df = None, transaction_df = None):
    '''
    Function to help manage scarping venmo.  It starts with an initial set or list of users or user_ids and dataframes to add to.  
    '''
    if isinstance(users,str):
        intial_users = set([users])
        new_users = set([users])
    else:
        initial_users = set(users)
        new_users = set(users)
    error_ids = set()
    new_users_add = set()
     

    for level in range(levels):
        print('*'*50)
        print(f'Starting level {level+1}')

        
        
        for user in new_users:

            user_df, transaction_df, new_users_add, new_error_id = scrape.scrape_data_to_df(user_id = user, user_df = user_df, 
                                                                                                transaction_df = transaction_df)
            new_users = new_users_add.union(new_users) 
            error_ids = set(error_ids).union(new_error_id)
        new_users = new_users - intial_users
        initial_users = new_users

        pickle.dump(new_users, open('new_users.p','wb'))
        pickle.dump(error_ids, open('error_ids.p','wb'))
        if user_df is not None:
            user_df.to_pickle('user_data.p')
        if transaction_df is not None :
            transaction_df.to_pickle('transaction_data.p')

    return user_df, transaction_df, new_users, error_ids

access_token = Venmo_Scrape_Client.get_access_token(username = config.username,
                                        password = config.password, device_id = config.device_id)

scrape = Venmo_Scrape_Client(access_token = access_token)


#initial user
my_user = scrape.user.get_my_profile()

#Run scrape on 6 levels of users
user_df, transaction_df, new_users, error_ids = scrape_level(my_user.id, 5)



pickle.dump(new_users, open('new_users.p','wb'))
pickle.dump(error_ids, open('error_ids.p','wb'))

user_df.to_pickle('user_data.p')
transaction_df.to_pickle('transaction_data.p')

user_df.to_csv('venmo_users.csv')
transaction_df.to_csv('venmo_transactions.csv')

scrape.log_out(f'Bearer {access_token}')



