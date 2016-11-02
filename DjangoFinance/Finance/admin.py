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

class EquityPosition_Admin(admin.ModelAdmin):
    readonly_fields = ('Amount',)
    list_display=('InvestType','Equity','Amount','AvgPrice','Quantity','UpdateDate','Comment')
admin.site.register(EquityPosition,EquityPosition_Admin)

class EquityReg_Admin(admin.ModelAdmin):
    readonly_fields = ('Amount',)
    list_display=('Agency','Account','EquityPosition','Amount','Price','Quantity','TradeDate','Comment')
admin.site.register(EquityReg,EquityReg_Admin)


