import pandas as pd
import matplotlib.pyplot as plt
from pylab import mpl
from datetime import date
import numpy as np
df=pd.read_csv('D:\\hotel\\hotel_bookings.csv')
df.info() #有32欄119390列，有缺失值children country agent company
a=df.nunique() #dataframe可以用nunique找出每項不重複的值有多少
df['children'].fillna(0,inplace=True)#children的缺失值代表無小孩，改0
df['total guest']=df['children']+df['babies']+df['adults']#所有客人數
explode = (0,0.05) #分隔2個圓餅圖
df['hotel'].value_counts().plot(kind='pie',explode=explode, autopct ='%1.1f%%')#畫hotel的比率的圓餅圖
plt.savefig('D:\\hotel\\percentage of Hotels.jpg')
r_adult=df.loc[(df['hotel']=='Resort Hotel')&(df['is_canceled']==0),'adults'].sum()
r_chil=df.loc[(df['hotel']=='Resort Hotel')&(df['is_canceled']==0),'children'].sum()
r_baby=df.loc[(df['hotel']=='Resort Hotel')&(df['is_canceled']==0),'babies'].sum()
labels=['adults','children','babies',]
size=r_adult,r_chil,r_baby
plt.pie(size , labels = labels,autopct ='%1.1f%%')#Resort飯店未取消的總人數中小孩跟成人跟寶寶的占比
plt.axis('equal')
plt.savefig('D:\\hotel\\Guest type percentage in the Resort Hotel.jpg')
c_adult=df.loc[(df['hotel']=='City Hotel')&(df['is_canceled']==0),'adults'].sum()
c_chil=df.loc[(df['hotel']=='City Hotel')&(df['is_canceled']==0),'children'].sum()
c_baby=df.loc[(df['hotel']=='City Hotel')&(df['is_canceled']==0),'babies'].sum()
labels=['adults','children','babies',]
size=c_adult,c_chil,c_baby
plt.pie(size , labels = labels,autopct ='%1.1f%%')#City飯店未取消的總人數中小孩跟成人跟寶寶的占比
plt.axis('equal')
plt.savefig('D:\\hotel\\Guest type percentage in the City Hotel.jpg')
#只有children跟只有大人的高峰月份
data=df.loc[(df['is_canceled']==0)].copy()
data['kids']=df['children']+df['babies']
data['total guest']=df['children']+df['babies']+df['adults']
#用Categorical排序1月-12月，categories是要排序的類別，ordered=True才會排序
df['arrival_date_month']=pd.Categorical(df['arrival_date_month'], categories=['January', 'February', 'March', 'April','May','June', 'July', 'August','September', 'October', 'November', 'December'],ordered=True)
#用樞紐分析算出各月的人數，aggfunc=函數，values=需計算的欄位
pd=data.pivot_table(index=['hotel','arrival_date_month'],values=['kids','adults'],aggfunc=[np.sum]).reset_index()#有小孩和成人每個月份的總人數
pd.columns=['hotel','month','count_a','count_k']
c_month=pd.query('hotel==["City Hotel"]')#查询某一项数据
pd.sort_values(by=['month'],inplace=True)#month會按照前面設置好的categorical排序(若無設置才照字母排)，並替換原數據(inplace=True)
plt.xlabel('month')
plt.ylabel('amount')
plt.plot(c_month['month'],c_month['count_a'],'b-*',label='adults')
plt.plot(c_month['month'],c_month['count_k'],'r--o',label='kids')
plt.xticks(rotation=90)#设置x轴标签旋转角度
plt.legend()#顯示xy的label
fig=plt.gcf()#plt.gcf()用來获取当前图片
fig.set_size_inches(14,10)#設圖片大小
fig.savefig('D:\\hotel\\Kid v.s Adult in the City Hotel.png')
r_month=pd.query('hotel==["Resort Hotel"]')
plt.xlabel('month')
plt.ylabel('amount')
plt.plot(r_month['month'],r_month['count_a'],'g-*',label='adults')
plt.plot(r_month['month'],r_month['count_k'],'y--o',label='kids')
plt.xticks(rotation=90)#设置x轴标签旋转角度
plt.legend()#顯示xy的label
fig=plt.gcf()#plt.gcf()用來获取当前图片
fig.set_size_inches(14,10)#設圖片大小
fig.savefig('D:\\hotel\\Kid v.s Adult in the Resort Hotel.png')
#每間飯店的市場區隔
ps=data.pivot_table(index=['hotel','market_segment'],values=['total guest'],aggfunc=[np.sum]).reset_index()
ps.columns=['hotel','market_segment','guests']
ps=ps.append({'hotel':'Resort Hotel','market_segment':'Aviation','guests':0}, ignore_index=True)#加一筆數據
ps.sort_values(by=['market_segment'],inplace=True)
c_market=ps.query('hotel==["City Hotel"]')
r_market=ps.query('hotel==["Resort Hotel"]')
x=np.arange(len(ps['market_segment'].unique()))#用np.arange生成list來列出market segment[0 1 2 3 4 5 6]來代表x軸的位置
plt.ylabel('people amount')
plt.xlabel('market segment')
labels=ps['market_segment'].unique()#x軸標籤名稱
plt.xticks(x,labels)#設定x軸刻度標籤，ticks=標籤位置, labels=標籤名稱
plt.bar(x,c_market['guests'],width=0.35,label='City Hotel')
plt.bar(x+ 0.35,r_market['guests'],width=0.35,label='Resort Hotel')
plt.legend()
fig=plt.gcf()#plt.gcf()用來获取当前图片
fig.set_size_inches(14,10)#設圖片大小
fig.savefig('D:\\hotel\\market segment.png')
#兩個飯店每月的取消人數的比例
d=df.groupby(by=['hotel','arrival_date_month']).agg({'total guest':sum}).reset_index().rename(columns={'total guest':'total booked'})
e=df[(df['is_canceled']==1)].groupby(by=['hotel','arrival_date_month']).agg({'total guest':sum}).reset_index().rename(columns={'total guest':'canceled'})
d['canceled']=e['canceled']
d['percentage']=round((d['canceled']/d['total booked'])*100,2)
plt.xlabel('month')
plt.ylabel('%')
city=d.query('hotel==["City Hotel"]')
resort=d.query('hotel==["Resort Hotel"]')
plt.plot(city['arrival_date_month'],city['percentage'],'c-*',label='City Hotel')
plt.plot(resort['arrival_date_month'],resort['percentage'],'y--o',label='Resort Hotel ')
plt.xticks(rotation=90)#设置x轴标签旋转角度
plt.legend()#顯示xy的label
fig=plt.gcf()#plt.gcf()用來获取当前图片
fig.set_size_inches(14,10)
fig.savefig('D:\\hotel\\The cancal persantage for City Hotal vs Resort Hotel.png')
