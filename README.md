# Algorand_Social_Forum_Exchange-with-MongoDB

As a student,the aim was to create a Lightning Network, where the user buys coins from the centralized exchange paying commissions, but then, can exchange the coins or sell them or buy them from other users without commissions, and then sell them back to the centralized system, always looking for an eventual profit


1) Install python 3.7/3.8/3.9
2) install Mongodb Compass
3) Click cd  Algorand_Social_Forum_Exchange.......or If you wish to create a virtual enviroment, you can do it with the command (virtualenv .)then (.  bin/activate) with MAC
4) Install packages pip install -r requirements.txt
5) Click python manage.py runserver
6) Then you have to go in ADMIN and enter Ordermanager and enter a number(usually '0'),then click save
7) The images of the homepage is left empty, just to insert the photos as you like and create a page as you see fit. It is sufficient to go to admin and PrincipalHome to add the photos from the PC or to take those displayed in the MEDIA folder.
8) If you are the admin you can go to the social page and create a section for users to discuss.
9) After registering, you are automatically assigned ALGO coins and 1.000 USD which you can view in your wallet.
10) After creating the discussion section, registered users will be able to comment and use it as a forum. The user also has his own social profile.
11) a) You can buy and sell Algo using coinmarketcap called CEX b)Place a sell or buy price order for coins within the DEX (decentralized exchange between users)
12) If you place a buy order in the dex you cannot make a sell order, but you can cancel your order if there was no "matching" with another user.
13) If you place a buy order in the dex you cannot make a sell order, but you can cancel your order if there was no "matching" with another user
the same thing is done with a sell order.
14)If you have placed a buy order, you can place subsequent orders at a price equal to or higher than the first order entered.
15)You can view the status of your order in the public status to check if it is open or concluded.
16)You also have a personal profile to see all your DEX transactions or CEX a wallet where you can check your gain / loss balance, number of coins and USD availability.
17) when you want to buy coins from coinmarketcap you pay a 1% commission, while when you want to sell on the Exchange the commission is reduced to 0.5%.
18) The sale on the Exchange is calculated taking into consideration the weighted average of the purchases in Cex and the weighted average of the purchases in DEX.
19) when buying from the exchange you can buy either at market or limit price. The limit price is a price at or below the market for up to 10% of the market price.
20) when you sell exchanges you can do so at either market or limit price. The limit price is a price at or above the market price for up to 10% of the market price.
21) The weighted average between the two averages will be the "average carrying price" used to sell to Coinmarketcap and realize your gain or loss.
22) At the moment the profit follows a FloatField field, but it will be changed to a decimal, to make it more precise.
