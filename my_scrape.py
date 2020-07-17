from venmo_scrape import Venmo_Scrape_Client
import config

'''
Script to pull data from venmo's api and save it locally.

Not close to working!
'''

access_token = Venmo_Scrape_Client.get_access_token(username = config.username,
                                        password = config.password, device_id = config.device_id)

scrape = Venmo_Scrape_Client(access_token = access_token)



my_user = scrape.user.get_my_profile()

print(scrape.user_scrape(user = my_user))

scrape.log_out(f'Bearer {access_token}')

