import matplotlib.pyplot as plt
import numpy as np

# x=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# y=[24, 44, 66, 8, 100, 17982, 14, 1600, 18, 2800]
# z=[11890, 22, 37890, 430, 540, 6090, 790,]
# plt.figure(figsize=(66, 5))
#
#
# plt.grid(True, axis='both', color='gray', alpha=0.3, ls=':', lw=1)
# #plt.xticks(x)
#plt.xlabel("day")
#plt.ylabel('temperature')
#plt.title('')
#plt.legend(loc=0, shadow=True, fontsize="small")
#plt.show()
#
# place =['village', 'city']
# temperature = [13 ,150]
# ypos = np.arange(len(place))
#
# plt.bar(place, temperature)
# company=['GOOGL','AMZN','MSFT','FB']
# revenue=[90,136,89,27]
# profit=[40,2,34,12]
#
# xpos = np.arange(len(company))
# plt.subplot(2,1,1)
# plt.barh(xpos+0.2,revenue, height=0.4, label="Revenue")
# plt.barh(xpos-0.2,profit, height=0.4,label="Profit", color="green")
#
# # plt.xticks(xpos,company)
# plt.yticks(xpos,company)
# plt.ylabel("Revenue(Bln)")
# plt.title('US Technology Stocks')
# plt.legend()

#blood_sugar = [113, 85, 90, 150, 149, 88, 93, 115, 135, 80, 77, 82, 129]
# plt.hist(blood_sugar, rwidth=0.5) # by default number of bins is set to 10
#plt.hist(blood_sugar,rwidth=0.5,bins=4, histtype='stepfilled')
exp_vals = [1400,600,300,410,250]
exp_labels = ["Home Rent","Food","Phone/Internet Bill","Car ","Other Utilities"]
plt.axis('equal') # to make pie chart look circular
plt.pie(exp_vals,labels=exp_labels, explode=(0,0,0,0.5,0), shadow=True, autopct='%1.2f%%', startangle=30, radius=0.90,counterclock=True )
plt.savefig("piechart.jpg", bbox_inches="tight", pad_inches=1, transparent=True)

plt.show()
