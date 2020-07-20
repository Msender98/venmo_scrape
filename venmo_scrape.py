from venmo_api import Client



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

    def user_transaction_scrape(self, user = None, user_id = None):
        '''
        Inputs a user object and outputs a set of users they have interacted with and a list 
        of their transactions.
        '''

        if not (user or user_id):
            raise ValueError('user must be a venmo.user.User object')
        elif not user:   
            user = self.user.get_user(user_id = user_id)


        try:
            transactions = self.user.get_user_transactions(user_id = user.id)
            users = {transaction.target.id for transaction in transactions}.union(
                                {transaction.actor.id for transaction in transactions})
            
        except:
            transactions = []
            users = {user.id}

        return transactions, users 
