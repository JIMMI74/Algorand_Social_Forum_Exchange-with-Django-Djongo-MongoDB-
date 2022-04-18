# Algorand_Social_Forum_Exchange-with-MongoDB
1) Install python 3.7/3.8/3.9
2) install Mongodb Compass
3) Create a virtual enviroment command (virtualenv .)then (.  bin/activate) with MAC
5) Install packages pip install -r requirements.txt
6) After python manage.py runserver, go to admin and enter Ordermanager and enter a number(usually '0'),then click save
7) The images of the homepage is left empty, just to insert the photos as you like and create a page as you see fit. It is sufficient to go to admin and PrincipalHome to add the photos from the PC or to take those displayed in the MEDIA folder.
8) If you are the admin you can go to the social page and create a section for users to discuss.
9) After registering, you are automatically assigned ALGO coins and 10,000 USD which you can view in your wallet.
10) After creating the discussion section, registered users will be able to comment and use it as a forum. The user also has his own social profile.
11) a) You can buy and sell Algo using coinmarketcap called CEX b)Place a sell or buy price order for coins within the DEX (decentralized exchange between users)
12) If you place a buy order in the dex you cannot make a sell order, but you can cancel your order if there was no "matching" with another user.
13) If you place a buy order in the dex you cannot make a sell order, but you can cancel your order if there was no "matching" with another user
the same thing is done with a sell order.

13)If you have placed a buy order, you can place subsequent orders at a price equal to or higher than the first order entered.

14)You can view the status of your order in the public status to check if it is open or concluded.

15)You also have a personal profile to see all your DEX transactions or CEX a wallet where you can check your gain / loss balance, number of coins and USD availability.

16) when you want to buy coins from coinmarketcap you pay a 1% commission, while when you want to sell on the Exchange the commission is reduced to 0.5%.

17) The sale on the Exchange is calculated taking into consideration the weighted average of the purchases in Cex and the weighted average of the purchases in DEX.

18) The arithmetic average between the two will be the "average charged price" used for the sale and for the realization of your gain or loss.

19) At the moment the profit follows a FloatField field, but it will be changed to a decimal, to make it more precise.

20)
