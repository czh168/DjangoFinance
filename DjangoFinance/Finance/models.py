# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.fields import *
from django.core.urlresolvers import reverse
from django.apps import apps
import datetime
import urllib.request
import csv
# Create your models here.

#*******************************************************************************************************************
#************                                         base                                              ************
#*******************************************************************************************************************
#机构
class Agency(models.Model):
    Name= models.CharField('名称', max_length=30,blank=True, null=True)
    Type=models.CharField('机构类型', choices=(('1', "银行"),('2', "证券公司"),('3', "理财平台"),('4',"p2p平台"),('5',"基金公司")),max_length=1,blank=True, null=True)
    Comment= models.CharField('说明', max_length=100,blank=True, null=True)
    def __str__(self):
        return self.Name

    class Meta:
        verbose_name = '机构'
        verbose_name_plural = '机构'
        ordering = ['Type','Name']  # 按照哪个栏目排序
#户头
class Account(models.Model):
    Name= models.CharField('名称', max_length=30,blank=True, null=True)
    Comment= models.CharField('说明', max_length=100,blank=True, null=True)
    def __str__(self):
        return self.Name
    class Meta:
        verbose_name = '户头'
        verbose_name_plural = '户头'
        ordering = ['Name']  # 按照哪个栏目排序
#投资类别
class InvestType(models.Model):
    Name= models.CharField('类名', max_length=30,blank=True, null=True)
    SubName= models.CharField('子类名', max_length=30,blank=True, null=True)
    Comment= models.CharField('说明', max_length=100,blank=True, null=True)
    Risk= models.CharField('风险', choices=(('1', "低"),('2', "中"),('3', "高")),max_length=1,blank=True, null=True)
    Liquidity=models.CharField('流动性', choices=(('1', "高"),('2', "中"),('3', "低")),max_length=1,blank=True, null=True)
    def __str__(self):
        return self.Name+"/"+self.SubName
    class Meta:
        verbose_name = '投资类别'
        verbose_name_plural = '投资类别'
        ordering = ['Name','SubName']  # 按照哪个栏目排序

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
    Name= models.CharField('类名', max_length=30,blank=True, null=True)
    Comment= models.CharField('说明', max_length=100,blank=True, null=True)
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
        return gcf[self.Name]

    def __str__(self):
        return self.Name
    class Meta:
        verbose_name = '利息类型'
        verbose_name_plural = '利息类型'
        ordering = ['Name']  # 按照哪个栏目排序
#现金流
class CashFlow(models.Model):
    HappendDate=models.DateField('日期',editable=True)
    Amount=models.FloatField('金额' ,blank=True, null=True)
    class Meta:
        abstract = True
        
#*******************************************************************************************************************
#权益类信息
class Equity(models.Model):
    Name= models.CharField('股票名称', max_length=50,blank=True, null=True)
    Code=models.CharField('股票代码', max_length=20,blank=True, null=True)
    Price=models.FloatField('股票价格' ,blank=True, null=True,default=0)
    Type=models.CharField('类型', choices=(('1', "上海"),('2', "深圳"),('3', "基金"),('4',"自定义")),max_length=1,blank=True, null=True)
    def GetInternetPrice(self,code,type):
            t={'基金':'f_','上海':'sh','深圳':'sz'}
            p={'基金':1,'上海':3,'深圳':3}
            response = urllib.request.urlopen("http://hq.sinajs.cn/list="+t[type]+code)
            html = response.read()
            htmld=html.decode("gb2312")
            s=htmld.split(",")[p[type]]
            return float(s)
    def SetPrice(self):
        if self.get_Type_display()!='自定义' :
            self.Price=self.GetInternetPrice(self.Code,self.get_Type_display())
            self.save()
    def __str__(self):
        return self.Code+ self.Name
    class Meta:
        verbose_name = '权益类信息'
        verbose_name_plural = '权益类信息'
        ordering = ['Type','Code']  # 按照哪个栏目排序
#**********************************************************************************************************************
#数据导入
class BatchImport(models.Model):
    ModelName= models.CharField('模型名称', max_length=50,blank=True, null=True)
    UploadFile= models.FileField('上传文件',upload_to='./upload/%Y-%m-%d/')
    UploadTime=models.DateTimeField('上传时间',auto_now=True, null=True,blank=True)
 
    def save(self, *args, **kwargs):        
        super(BatchImport, self).save(*args, **kwargs)
        self.ImportData('Finance',self.ModelName,self.UploadFile.path)
#字符串布尔值
    def StrBoolValue(self, value):       
        if value in ("0", "false", "False","F","f"):            
            return False        
        elif value in ("1", "true", "True","T","t"):           
           return True       
        else:
            return False            
#类型转换
    def TypeChange(self,field,str):
        ftype=type(field)
        if ftype in (models.DateField,):
            return datetime.datetime.strptime(str, "%Y/%m/%d").date()
        elif ftype in ( models.DateTimeField,):
            return datetime.datetime.strptime(str, "%Y/%m/%d %H:%M:%S")
        elif ftype in (models.BooleanField,models.NullBooleanField):
            return  self.StrBoolValue(str)
        elif ftype in (models.ForeignKey,):
            return self.GetForeignObj(str,field)
        elif ftype in (models.FloatField,models,):
            return float(str)
        else:
            if len(field.choices):
                return self.GetChoiceValue(str,field.choices)
            else:
                print(str)
                return str
#返回choice值
    def GetChoiceValue(self,name,choices):
        for i in choices:
            if i[1]==name:
                return i[0]
    def GetForeignObj(self,str,field):
        m=field.related_model
        for r in m.objects.all():
            if "%s"%r==str:
                return r
         
#导入数据
    def ImportData(self,appname,modelname,path):
        csvrows=csv.DictReader(open(path, 'r'))
#获取model
        m = apps.get_app_config(appname).get_model(modelname)
#获取字段verbose_name
        fverbose_names=[f.verbose_name for f in m._meta.get_fields() if not f.auto_created]
#获取字段
        fields=[f for f in m._meta.get_fields() if not f.auto_created]
#生成verbose_name与field的字典
        v_f=dict(zip( fverbose_names, fields))
#导入数据
        for csvrow in csvrows:
            e=m()
            for name in csvrow:
                f=v_f[name]
                setattr(e,f.name,self.TypeChange(f,csvrow[name]))
            e.save()       
    def __str__(self):
        return self.ModelName
    class Meta:
        verbose_name = '数据导入'
        verbose_name_plural = '数据导入'
        ordering = ['UploadTime']  # 按照哪个栏目排序
#******************************************************************************************************************
#*************                                      main                                           ****************
#******************************************************************************************************************
#固定收益类
class  FixedIncome(models.Model):
    Name= models.CharField('名称', max_length=256,blank=True, null=True)
    Agency=models.ForeignKey(Agency,blank=True, null=True,verbose_name='机构')
    Account=models.ForeignKey(Account,blank=True, null=True,verbose_name='户头')
    Spend=models.FloatField('投入' ,blank=True, null=True,default=0)
    Investtype=models.ForeignKey(InvestType,blank=True, null=True,verbose_name='投资类别')
    Buydate=models.DateField('购入时间',  editable=True, null=True)
    Maturity=models.DateField('到期时间', editable=True, null=True)
    IntresType=models.ForeignKey(IntrestType,blank=True, null=True,verbose_name='利息类型')
    AnnualizedYield=models.FloatField('年化率',blank=True, null=True)
    Discount=models.FloatField('优惠' ,blank=True, null=True,default=0)
    Comment= models.CharField('说明', max_length=100,blank=True, null=True)
    Completed=models.BooleanField("已完成",default=False)
    #生成现金流
    def genCashFlow(self):
        it=self.intrestype
        ficf=FixedIncomeCashFlow.objects.filter(relatefixedincome=self)
        ficf.delete()
        for i,j in it.genCashFlow(self.Spend,self.AnnualizedYield,self.Buydate,self.Maturity,self.Discount):
            cf=FixedIncomeCashFlow.objects.create(happenddate=i,amount=j,relatefixedincome=self)
        
    def __str__(self):
        return self.Buydate.strftime('%Y-%m-%d')+"/"+ self.Name
    class Meta:
        verbose_name = '固定收益类'
        verbose_name_plural = '固定收益类'
        ordering = ['Buydate','Account','Agency']  # 按照哪个栏目排序        
#固定收益类现金流
class FixedIncomeCashFlow(CashFlow):
    RelateFixedIncome=models.ForeignKey(FixedIncome,verbose_name='相关固定收益类')
    class Meta:
        verbose_name = '固定收益类现金流'
        verbose_name_plural = '固定收益类现金流'
        ordering = ['HappendDate']  # 按照哪个栏目排序
        
#*******************************************************************************************************************
#权益类登记
class EquityReg(models.Model):
    Agency=models.ForeignKey(Agency,blank=True, null=True,verbose_name='机构')
    Account=models.ForeignKey(Account,blank=True, null=True,verbose_name='户头')
    InvestType=models.ForeignKey(InvestType,blank=True, null=True,verbose_name='投资类别')
    Equity=models.ForeignKey(Equity,blank=True, null=True,verbose_name='权益类信息')
    Amount=models.FloatField('成交金额' ,blank=True, null=True,default=0)
    Price=models.FloatField('成交单价' ,blank=True, null=True,default=0)
    Quantity=models.FloatField('成交数量' ,blank=True, null=True,default=0)
    TradeDate=models.DateField('成交日期',  editable=True, null=True)
    Comment= models.CharField('说明', max_length=100,blank=True, null=True)
    class Meta:
        verbose_name = '权益类登记'
        verbose_name_plural = '权益类登记'
        ordering = ['TradeDate','Account','Agency']  # 按照哪个栏目排序