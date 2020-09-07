'''
 as of 3, september 2020:

 users: 75

 active: 20

 pageviews: 1000
'''


def twenty_percent_growth(users=0, active_users=0, pageviews=0):
    '''this function prints out a 30 percent projection growth of input data'''
    for i in range(12):
        users = int(users + (users * 0.2))
        active_users = int(active_users + (active_users * 0.2))
        pageviews = int(pageviews + (pageviews * 0.2))

        # printing the projection data
        print("Month " + str(i+1))
        print("|")
        print("|___ users: " + str(users))
        print("|___ active users: " + str(active_users))
        print("|___ pageviews: " + str(pageviews))
        print("")


users = 5911
active_users = 1419
pageviews = 79402
twenty_percent_growth(users, active_users, pageviews)



"""
Growth Projections:

2021 (20% percent growth every month):

users = 76
active_users = 20
pageviews (Weekly) = 1000

Month 1
|
|___ users: 91
|___ active users: 24
|___ pageviews: 1200

Month 2
|
|___ users: 109
|___ active users: 28
|___ pageviews: 1440

Month 3
|
|___ users: 130
|___ active users: 33
|___ pageviews: 1728

Month 4
|
|___ users: 156
|___ active users: 39
|___ pageviews: 2073

Month 5
|
|___ users: 187
|___ active users: 46
|___ pageviews: 2487

Month 6
|
|___ users: 224
|___ active users: 55
|___ pageviews: 2984

Month 7
|
|___ users: 268
|___ active users: 66
|___ pageviews: 3580

Month 8
|
|___ users: 321
|___ active users: 79
|___ pageviews: 4296

Month 9
|
|___ users: 385
|___ active users: 94
|___ pageviews: 5155

Month 10
|
|___ users: 462
|___ active users: 112
|___ pageviews: 6186

Month 11
|
|___ users: 554
|___ active users: 134
|___ pageviews: 7423

Month 12
|
|___ users: 664
|___ active users: 160
|___ pageviews: 8907

"""


"""
2022 (20% percent growth every month):

users = 664
active_users = 160
pageviews (Weekly) = 8907

Month 1
|
|___ users: 796
|___ active users: 192
|___ pageviews: 10688

Month 2
|
|___ users: 955
|___ active users: 230
|___ pageviews: 12825

Month 3
|
|___ users: 1146
|___ active users: 276
|___ pageviews: 15390

Month 4
|
|___ users: 1375
|___ active users: 331
|___ pageviews: 18468

Month 5
|
|___ users: 1650
|___ active users: 397
|___ pageviews: 22161

Month 6
|
|___ users: 1980
|___ active users: 476
|___ pageviews: 26593

Month 7
|
|___ users: 2376
|___ active users: 571
|___ pageviews: 31911

Month 8
|
|___ users: 2851
|___ active users: 685
|___ pageviews: 38293

Month 9
|
|___ users: 3421
|___ active users: 822
|___ pageviews: 45951

Month 10
|
|___ users: 4105
|___ active users: 986
|___ pageviews: 55141

Month 11
|
|___ users: 4926
|___ active users: 1183
|___ pageviews: 66169

Month 12
|
|___ users: 5911
|___ active users: 1419
|___ pageviews: 79402

"""

"""
2023: (20% percent growth every month):

users = 5911
active_users = 1419
pageviews (Weekly) = 79402

Month 1
|
|___ users: 7093
|___ active users: 1702
|___ pageviews: 95282

Month 2
|
|___ users: 8511
|___ active users: 2042
|___ pageviews: 114338

Month 3
|
|___ users: 10213
|___ active users: 2450
|___ pageviews: 137205

Month 4
|
|___ users: 12255
|___ active users: 2940
|___ pageviews: 164646

Month 5
|
|___ users: 14706
|___ active users: 3528
|___ pageviews: 197575

Month 6
|
|___ users: 17647
|___ active users: 4233
|___ pageviews: 237090

Month 7
|
|___ users: 21176
|___ active users: 5079
|___ pageviews: 284508

Month 8
|
|___ users: 25411
|___ active users: 6094
|___ pageviews: 341409

Month 9
|
|___ users: 30493
|___ active users: 7312
|___ pageviews: 409690

Month 10
|
|___ users: 36591
|___ active users: 8774
|___ pageviews: 491628

Month 11
|
|___ users: 43909
|___ active users: 10528
|___ pageviews: 589953

Month 12
|
|___ users: 52690
|___ active users: 12633
|___ pageviews: 707943

"""
