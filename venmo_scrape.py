from venmo_api import Client



class Venmo_Scrape_Client(Client):
    '''
    Extenstion to the Client object in the venmo_api module. Adds methods for scraping data from venmo. 

    Useful methods from the api: 
    get_user(user_id = user_id)

    '''  

    def user_scrape(self, user = None):
        '''
        wdwd
        '''
        if not user:
            raise ValueError('user must be a venmo.user.User object')

        item = {}
        item['username'] = user.username
        # item['username'] = user.username
        # item['username'] = user.username
        # item['username'] = user.username
        # item['username'] = user.username
        return item

    def transaction_scrape(self,user = None):

        if not user:
            raise ValueError('user must be a venmo.user.User object')
        pass