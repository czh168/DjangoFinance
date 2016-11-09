from django.contrib import admin
from Finance.models import *
# Register your models here.
#base**************************************************************************
class AgencyType_Admin(admin.ModelAdmin):
    list_display=('Name',)
admin.site.register(AgencyType,AgencyType_Admin)

class Agency_Admin(admin.ModelAdmin):
    list_display=('Type','Name','Comment')
admin.site.register(Agency,Agency_Admin)

class Account_Admin(admin.ModelAdmin):
    list_display=('Name','Comment')
admin.site.register(Account,Account_Admin)

class InvestType_Admin(admin.ModelAdmin):
    list_display=('Name','SubName','Risk','Liquidity','Comment')
admin.site.register(InvestType,InvestType_Admin)

class IntrestType_Admin(admin.ModelAdmin):
    list_display=('Name','Comment')
admin.site.register(IntrestType,IntrestType_Admin)

class Equity_Admin(admin.ModelAdmin):
    list_display=('Name','Code','Price','Type')
    actions=['setprice',]
    
    def setprice(self,request,queryset):
        for sf in queryset:
            sf.SetPrice()
    setprice.short_description="从互联网更新价格"
admin.site.register(Equity,Equity_Admin)

class BatchImport_Admin(admin.ModelAdmin):

    list_display=('ModelName','UploadFile','UploadTime')
admin.site.register(BatchImport,BatchImport_Admin)
#main****************************************************************************
class FixedIcome_Admin(admin.ModelAdmin):
    list_display=('Name','Agency','Account','Spend','Investtype','Buydate','Maturity','IntresType','AnnualizedYield','Discount','Comment','Completed')
    list_filter=('Completed',)
    actions = ['make_completed','genCashFlowA']

    def make_completed(self, request, queryset):
        ur=queryset.update(completed=True)
        self.message_user(request, "完成%d条" %ur)
    make_completed.short_description = "结束"

    def genCashFlowA(self, request, queryset):
        for fi in queryset : 
            fi.genCashFlow()
        self.message_user(request, "生成现金流ok")
    genCashFlowA.short_description="生成现金流"
admin.site.register(FixedIncome,FixedIcome_Admin)

class FixedIncomeCashFlow_Admin(admin.ModelAdmin):
    list_display=('HappendDate','Amount','RelateFixedIncome')
admin.site.register(FixedIncomeCashFlow,FixedIncomeCashFlow_Admin)

class EquityPositionFilter(admin.SimpleListFilter):
    title = '是否持仓'
    parameter_name = 'Quantity'
    def lookups(self, request, model_admin):
        return (
            ('y', '是'),
            ('n', '否'),
        )
    def queryset(self, request, queryset):
        if self.value() == 'y':
            return queryset.filter(Quantity__gt=0)
        if self.value() == 'n':
            return queryset.filter(Quantity__lte=0)
        return queryset
class EquityPosition_Admin(admin.ModelAdmin):
    #重新保存
    def batch_update(self,request,queryset):
        for e in queryset:
            e.save()
    batch_update.short_description="重新保存"
    #从权益类登记更新
    def UpdateFromEquityReg(self,request,queryset):
        for e in queryset:
            e.UpdateFromEquityReg()
    UpdateFromEquityReg.short_description="从权益类登记更新"
    #从权益类行情中更新
    def UpdateFromEquity(self,request,queryset):
        for e in queryset:
            e.UpdateFromEquity()
    UpdateFromEquity.short_description="从权益类行情更新"
    readonly_fields = ('Cost','CurrentPrice','MarketValue','AllGain','ReturnRate')
    list_display=('InvestType','Equity','Cost','AvgPrice','Quantity','CurrentPrice','MarketValue','ReturnRate','AllGain','Comment')
    actions = ['batch_update','UpdateFromEquityReg','UpdateFromEquity',]
    list_filter = (EquityPositionFilter,)
admin.site.register(EquityPosition,EquityPosition_Admin)

class EquityReg_Admin(admin.ModelAdmin):
    def batch_update(self,request,queryset):
        for e in queryset:
            e.save()
    batch_update.short_description="重新保存"
    readonly_fields = ('Rate',)
    list_display=('Agency','Account','EquityPosition','Amount','Rate','Price','Quantity','TradeDate','Comment')
    actions = ['batch_update',]
    #list_editable = ('Amount', )
admin.site.register(EquityReg,EquityReg_Admin)

class EquityRegStatu_Admin(admin.ModelAdmin):
    list_display=('EquityReg','EquityPositionSaved','CashFlowSaved')
admin.site.register(EquityRegStatu,EquityRegStatu_Admin)

class EquityCashFlow_Admin(admin.ModelAdmin):
    list_display=('HappendDate','Amount','RelateEquityReg')
admin.site.register(EquityCashFlow,EquityCashFlow_Admin)