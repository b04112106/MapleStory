import random
global Rec
Rec = -1
RecommendBook = []
def star_mapleCoin(equipLevel,nowStar):
    if(nowStar<=9):
        return 1000 + pow(equipLevel,3)*(nowStar+1)/25
    if(nowStar==10):
        return 1000 + pow(equipLevel,3)*pow(nowStar+1,2.7)/200
    if(nowStar<=14):
        return 1000 + pow(equipLevel,3)*pow(nowStar+1,2.7)/66.66
    if(nowStar<=19):
        return 1000 + pow(equipLevel,3)*pow(nowStar+1,2.7)/50
    if(nowStar<=24):
        return 1000 + pow(equipLevel,3)*pow(nowStar+1,2.7)/40
def Price(From,To):
    if(To==From):
        return 0
    if(To>=10 and To <= 20):
        if(RecommendBook[To-10]):
            global Rec
            Rec = To - 10
            return PriceStarBook_c[To-10]
    return FromToCost[To-1]+Price(From,To-1)
    
#############INPUT################
# The market price of StarBook, the unit is 10K maple coin
PriceStarBook_m = [1565,1888,2111,3333,6000,37777,43777,162222,279999,600000,1720000]
# The market price of StarBook, the unit is NTD
PriceStarBook_c = [4,5,5,8,15,100,117,431,744,1900,3700]
ER_mp = 10000 / (34) # Exchange Rate of maple point versus maple coin
ER_ch = 400          # Exchange Rate of NTD versus maple coin
equipLevel = 160     # The level limitation of your equipment
FromStar = 0         # The number of stars that your equipment has now.
ToStar = 22          # The number of stars that you want of your equipment
###INFLUENT THE ACCURACY########
SampleCount = 300
##################################
PriceDirect_mp = []
Prob_success = [0.95,0.9,0.85,0.85,0.8,0.75,0.7,0.65,0.6,0.55,0.5,0.45,0.4,0.35,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.03,0.02,0.01]
Prob_fail =    [0.05,0.1,0.15,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.7,0.7,0.7,0.7,0.7,0.7,0.7,0.97,0.98,0.99]
### Calculate NTD needed in each stage
for i in range(ToStar):
    cost = 0
    if(i >= 12):
        cost = min(star_mapleCoin(equipLevel,i)/ER_mp / 10000,50)
    else:
        cost = min(star_mapleCoin(equipLevel,i)/ER_mp / 10000,9)
    PriceDirect_mp.append(cost*ER_mp/0.94/ER_ch)

for i in range(len(PriceStarBook_m)):
    PriceStarBook_c[i] = min(PriceStarBook_m[i]/(ER_ch*0.94),PriceStarBook_c[i])

FromToCost = []
for i in range(ToStar):
    TTC = 0
    for sample in range(SampleCount):
        TotalCost = 0
        nowStar = i
        while nowStar != i+1 :
            dice = random.random()
            TotalCost = TotalCost + PriceDirect_mp[nowStar]
            if(dice <= Prob_success[nowStar]):
                nowStar = nowStar + 1
            else:
                if(nowStar >= 11 and nowStar != 20):
                    nowStar = nowStar - 1
        TTC = TTC + TotalCost
    FromToCost.append(TTC/SampleCount)
    
###Calculate the accumlate price of directly reinforcing your equipment###
PriceAcc = []
temp = 0
for i in range(ToStar):    
    if(i >= FromStar):
        temp = temp + FromToCost[i]
    PriceAcc.append(temp)
    if(i >= 9 and i <= 19):
        RecommendBook.append(temp > PriceStarBook_c[i-9])
##############OUTPUT###########
p = Price(FromStar,ToStar)
if(Rec >= 0):
    print("We recommend you to buy StarBook"+str(Rec+10)+", and the price would be " + str(p))
else:
    print("We recommend you to reinforce directly and the price would be "+str(p))
