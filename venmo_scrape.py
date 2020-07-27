from venmo_api import Client
import pandas as pd
import datetime

class Venmo_Scrape_Client(Client):
    '''
    Extenstion to the Client object in the venmo_api module. Adds methods for scraping data from venmo. 

    Useful methods from the api: 
    get_user(user_id = user_id)

    '''  

    def user_scrape(self, user = None, user_id = None):
        '''
        Outputs user data from a venmo
        '''
        if not (user or user_id):
            raise ValueError('user must be a venmo.user.User object')
        elif not user:   
            user = self.user.get_user(user_id = user_id)

        item = {}
        item['username'] = user.username
        item['first_name'] = user.first_name
        item['last_name'] = user.last_name
        item['user_id'] = user.id
        item['phone'] = user.phone
        item['profile_picture_url'] = user.profile_picture_url
        item['is_active'] = user.is_active
        return item


    def transaction_scrape(self, transaction = None):
        '''
        Outputs data from a venmo transaction object

        '''
        if not transaction:
            raise ValueError('transaction must be a venmo.user.transaction object')

        item = {}
        item['actor_id'] = transaction.actor.id 
        item['date_completed'] = transaction.date_completed 
        item['date_created'] = transaction.date_created
        item['note'] = transaction.note
        item['target_id'] = transaction.target.id
        item['transaction_id'] = transaction.id
        item['status'] = transaction.status

        return item

    def all_transactions(self, user = None, user_id = None, year = 2019):
        '''
        Get all of the transactions of a venmo user after a given year
        '''
        if not (user or user_id):
            raise ValueError('user must be a venmo.user.User object')
        elif not user:   
            user = self.user.get_user(user_id = user_id)
        
        transactions = self.user.get_user_transactions(user = user)
        
        
        if len(transactions) == 0:
            return {}
        
        last_year = datetime.datetime.fromtimestamp(transactions[-1].date_created).year #will raise error if transactions are empty
        
        while last_year >= year:
            
            if len(transactions) == 0:
                return transactions

            last_year = datetime.datetime.fromtimestamp(transactions[-1].date_created).year
            new_transactions = self.user.get_user_transactions(user = user, before_id = transactions[-1].id)
            transactions = transactions + new_transactions
            
                
        return transactions

    def find_users(self, guess = None, user_df = None):
        '''
        Input a query, generally a name or username, and output a list of similar venmo user_ids
        '''

        if (guess is None):
            guess = input('Initial User Search')

        if (user_df is not None):
            past_users = user_df['user_id']
        else:
            past_users = []

        guesses = self.user.search_for_users(query = guess)
        
        new_users = [user.id for user in guesses if user.id not in past_users]

        if len(new_users) == 0:
            raise ValueError('Change the initial guess!')
        return new_users

    def scrape_data_to_df(self, user = None, user_id = None, user_df = None, transaction_df = None, year = 2019):
        '''
        Scrape data from a venmo user and output all of their connected users and transactions from after a given year. 

        Inputs are a user or user_id, and any existing venmo_transaction or venmo user dataframes.
        '''
        new_users = set()

        if not (user or user_id):
            raise ValueError('user must be a venmo.user.User object')
        elif not user:   
            user = self.user.get_user(user_id = user_id)

        try:
            transactions = self.all_transactions(user = user, year = year)

            connected_user_ids = {transaction.target.id for transaction in transactions}.union(
                                  {transaction.actor.id for transaction in transactions})
        except (ValueError, TypeError):
            transactions = {}
            user_error = set([user.id])
            print(f'{user.id} had an error while pulling transactions')
            return user_df, transaction_df, new_users, user_error

        if (user_df is None):
            user_df = pd.DataFrame(self.user_scrape(user = user), index = [0])

        if (transaction_df is None):
            #if there are 0 transactions this should raise an error
            transaction_df = pd.DataFrame(self.transaction_scrape(transaction = transactions[0]), index = [0])

        past_users = set(user_df['user_id'])
        past_transactions = set(transaction_df['transaction_id'])
        

        for con_user_id in connected_user_ids:
            if con_user_id not in past_users:
                user_df = user_df.append(self.user_scrape(user_id = con_user_id), ignore_index = True)
                new_users = new_users.union({con_user_id})
                past_users = past_users.union({con_user_id})
                
        print(len(transactions))
        for transaction in transactions:
            if transaction.id not in past_transactions:
                transaction_df = transaction_df.append(self.transaction_scrape(transaction = transaction), ignore_index = True)
                transaction_set = past_transactions.union({transaction.id})



        

        return user_df, transaction_df, new_users, set()

