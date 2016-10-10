# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
import datetime
import urllib.request
# Create your models here.

#*********************************************************************************************************************
#************                                         base                                                ************
#*********************************************************************************************************************
#机构
class Agency(models.Model):
    name= models.CharField('名称', max_length=30,blank=True, null=True)
    comment= models.CharField('说明', max_length=100,blank=True, null=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '机构'
        verbose_name_plural = '机构'
        ordering = ['name']  # 按照哪个栏目排序
#户头
class Account(models.Model):
    name= models.CharField('名称', max_length=30,blank=True, null=True)
    comment= models.CharField('说明', max_length=100,blank=True, null=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '户头'
        verbose_name_plural = '户头'
        ordering = ['name']  # 按照哪个栏目排序
#投资类别
class InvestType(models.Model):
    name= models.CharField('类名', max_length=30,blank=True, null=True)
    subname= models.CharField('子类名', max_length=30,blank=True, null=True)
    comment= models.CharField('说明', max_length=100,blank=True, null=True)
    risk= models.CharField('风险', choices=(('1', "低"),('2', "中"),('3', "高")),max_length=1,blank=True, null=True)
    liquidity=models.CharField('流动性', choices=(('1', "高"),('2', "中"),('3', "低")),max_length=1,blank=True, null=True)
    def __str__(self):
        return self.name+"/"+self.subname
    class Meta:
        verbose_name = '投资类别'
        verbose_name_plural = '投资类别'
        ordering = ['name','subname']  # 按照哪个栏目排序

#相差月数
def diff_by_month(starttime,endtime):
    months=(endtime.year-starttime.year)*12+endtime.month-starttime.month
    if add_by_month(starttime,months)>endtime:
        months-=1
    return months
#按月加
def add_by_month(datetime1, n = 1):
    # create a shortcut object for one day
    one_day = datetime.timedelta(days = 1)
 
    # first use div and mod to determine year cycle
    q,r = divmod(datetime1.month + n, 12)
 
    # create a datetime2
    # to be the last day of the target month
    datetime2 = datetime.date(
        datetime1.year + q, r + 1, 1) - one_day
    if datetime1.month != (datetime1 + one_day).month:
        return datetime2
    if datetime1.day >= datetime2.day:
        return datetime2
    return datetime2.replace(day = datetime1.day)
#利息类型
class IntrestType(models.Model):
    name= models.CharField('类名', max_length=30,blank=True, null=True)
    comment= models.CharField('说明', max_length=100,blank=True, null=True)
    #一次性还本付息
    class OneTimeDebt(object):
        def __init__(self,money,rate,starttime,endtime,discount):
            self.money=money
            self.rate=rate
            self.starttime=starttime
            self.endtime=endtime
            self.discount=discount
            self.step=0
        def __next__(self):
            self.step+=1  
            if self.step==1:
                return [self.starttime,self.money*-1+self.discount]
            elif self.step==2:
                return [self.endtime,self.money*(1+self.rate/12*diff_by_month(self.starttime,self.endtime))]
            else:
                raise StopIteration 
        def __iter__(self):  
            return self
    #按月付息到期还本
    class MonthlyInterest(object):
        def __init__(self,money,rate,starttime,endtime,discount):
            self.money=money
            self.rate=rate
            self.starttime=starttime
            self.endtime=endtime  
            self.step=0
            self.months=diff_by_month(starttime,endtime)
            self.discount=discount
            self.step=0
            self.money_everymonth=money*rate/12
        def __next__(self):
            self.step+=1  
            if self.step==1:
                return [self.starttime,self.money*-1+self.discount]
            elif self.step-1<=self.months:
                return [add_by_month(self.starttime,self.step-1),self.money_everymonth]
            elif self.step-1<=self.months+1:
                return [self.endtime,self.money]
            else:
                raise StopIteration 
        def __iter__(self):  
            return self
    #按月等额本息
    class EqualCorpusInt(object):
        def __init__(self,money,rate,starttime,endtime,discount):
            self.money=money
            self.rate=rate
            self.starttime=starttime
            self.endtime=endtime  
            self.step=0
            self.months=diff_by_month(starttime,endtime)
            print(self.months)
            self.discount=discount
            self.step=0
            self.money_everymonth=(self.money*(self.rate/12)*(1+self.rate/12)**self.months)/((1+self.rate/12)**self.months-1) 
        def __next__(self):
            self.step+=1
            if self.step==1:
                return [self.starttime,self.money*-1+self.discount]
            elif self.step-1<=self.months:
                return [add_by_month(self.starttime,self.step-1),self.money_everymonth]
            else:
                raise StopIteration
        def __iter__(self):  
            return self
    #生成现金流
    def genCashFlow(self,money,rate,starttime,endtime,discount):
        gcf={'一次性还本付息':self.OneTimeDebt(money,rate,starttime,endtime,discount),'按月付息到期还本':self.MonthlyInterest(money,rate,starttime,endtime,discount),'按月等额本息':self.EqualCorpusInt(money,rate,starttime,endtime,discount)}
        return gcf[self.name]

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '利息类型'
        verbose_name_plural = '利息类型'
        ordering = ['name']  # 按照哪个栏目排序
#现金流
class CashFlow(models.Model):
    happenddate=models.DateField('日期',editable=True)
    amount=models.FloatField('金额' ,blank=True, null=True)
    class Meta:
        abstract = True

#股票基金信息
class StockFundInfo(models.Model):
    name= models.CharField('股票名称', max_length=50,blank=True, null=True)
    code=models.CharField('股票代码', max_length=20,blank=True, null=True)
    price=models.FloatField('股票价格' ,blank=True, null=True,default=0)
    type=models.CharField('类型', choices=(('1', "股票"),('2', "基金"),('3',"自定义")),max_length=1,blank=True, null=True)
    def getprice(self,code,type):
            t={'基金':'f_','上海':'sh','深圳':'sz'}
            p={'基金':1,'上海':3,'深圳':3}
            response = urllib.request.urlopen("http://hq.sinajs.cn/list="+t[type]+code)
            html = response.read()
            htmld=html.decode("gb2312")
            s=htmld.split(",")[p[type]]
            return float(s)
    def setprice(self):
        if self.type!=3 :
            self.price=self.getprice(self.code,self.get_type_display())
            self.save()
    class Meta:
        verbose_name = '股票基金信息'
        verbose_name_plural = '股票基金信息'
        ordering = ['code']  # 按照哪个栏目排序
#******************************************************************************************************************
#*************                                      main                                           ****************
#******************************************************************************************************************
#固定收益类
class  FixedIncome(models.Model):
    name= models.CharField('名称', max_length=256,blank=True, null=True)
    agency=models.ForeignKey(Agency,blank=True, null=True,verbose_name='机构')
    account=models.ForeignKey(Account,blank=True, null=True,verbose_name='户头')
    spend=models.FloatField('投入' ,blank=True, null=True,default=0)
    investtype=models.ForeignKey(InvestType,blank=True, null=True,verbose_name='投资类别')
    buydate=models.DateField('购入时间',  editable=True, null=True)
    maturity=models.DateField('到期时间', editable=True, null=True)
    intrestype=models.ForeignKey(IntrestType,blank=True, null=True,verbose_name='利息类型')
    annualizedyield=models.FloatField('年化率',blank=True, null=True)
    discount=models.FloatField('优惠' ,blank=True, null=True,default=0)
    comment= models.CharField('说明', max_length=100,blank=True, null=True)
    completed=models.BooleanField("已完成",default=False)
    #生成现金流
    def genCashFlow(self):
        it=self.intrestype
        ficf=FixedIncomeCashFlow.objects.filter(relatefixedincome=self)
        ficf.delete()
        for i,j in it.genCashFlow(self.spend,self.annualizedyield,self.buydate,self.maturity,self.discount):
            cf=FixedIncomeCashFlow.objects.create(happenddate=i,amount=j,relatefixedincome=self)
        
    def __str__(self):
        return self.buydate.strftime('%Y-%m-%d')+"/"+ self.name
    class Meta:
        verbose_name = '固定收益类'
        verbose_name_plural = '固定收益类'
        
#固定收益类现金流
class FixedIncomeCashFlow(CashFlow):
    relatefixedincome=models.ForeignKey(FixedIncome,verbose_name='相关固定收益类')
    class Meta:
        verbose_name = '固定收益类现金流'
        verbose_name_plural = '固定收益类现金流'
        ordering = ['happenddate']  # 按照哪个栏目排序