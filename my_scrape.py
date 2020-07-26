from venmo_scrape import Venmo_Scrape_Client
import pandas as pd
import config
import pickle 

'''
Script to pull data from venmo's api and save it locally. 
'''
def scrape_level(users, levels, user_df = None, transaction_df = None):
    '''
    Function to help manage scarping venmo.  It starts with an initial set or list of users or user_ids then loops through that list, pulls
    those users data and their last 50 transactions. It then takes any users those users connected with and repeats on that set, 
    continuing that process for the input amount of levels. Option to input existing dataframes to add to. 
    
    Inputs:
    users = iterable group of venmo user objects or venmo user ids
    levels = amount of times to iterate through. Note the time of completion increases exponentially. As much as 50^n.
    user_df = dataframe of venmo user data. Contains name, username, user_id and profile_picture
    transaction_df = dataframe of venmo transaction data. Contains both user_ids of users's involved, a unique id and a note

    Returns:
    user_df = updated dataframe with venmo user 
    transaction_df = updated dataframe with venmo transaction data
    new_users = list of users which have not been added to the dataframe yet (neighbors of the last level of users)
    error_ids = list of errors of users
    
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
        print(f'{len(new_users)}')
        
        
        for user in new_users:
            
            user_df, transaction_df, new_users_add, new_error_id = scrape.scrape_data_to_df(user_id = user, user_df = user_df, 
                                                                                                transaction_df = transaction_df)
            new_users = new_users_add.union(new_users) 
            error_ids = error_ids.union(new_error_id)
            
        new_users = new_users - initial_users
        initial_users = new_users

        pickle.dump(new_users, open('new_users.p','wb'))
        pickle.dump(error_ids, open('error_ids.p','wb'))
        if (user_df is not None):
            user_df.to_pickle('user_data.p')
        if (transaction_df is not None) :
            transaction_df.to_pickle('transaction_data.p')

    return user_df, transaction_df, new_users, error_ids



access_token = Venmo_Scrape_Client.get_access_token(username = config.username,
                                        password = config.password, device_id = config.device_id)

scrape = Venmo_Scrape_Client(access_token = access_token)


#initial user
#my_user = scrape.user.search_for_users(query = 'Mike-Sender')

#Load previously created dataframes and set of new_users to scrape
user_df = pickle.load(open('user_data.p','rb'))
transaction_df = pickle.load(open('transaction_data.p','rb'))

#Find a new set of users by searching with venmo's api and a 
#new_users = scrape.find_users()
new_users = pickle.load(open('new_users.p','rb'))
#Scrape a set level of new users from the given set of users 
user_df, transaction_df, new_users, error_ids = scrape_level(new_users, 3) #user_df = user_df, transaction_df = transaction_df)


pickle.dump(new_users, open('new_users.p','wb'))
pickle.dump(error_ids, open('error_ids.p','wb'))

user_df.to_pickle('user_data.p')
transaction_df.to_pickle('transaction_data.p')

#user_df.to_csv('venmo_users.csv')
#transaction_df.to_csv('venmo_transactions.csv')

scrape.log_out(f'Bearer {access_token}')



