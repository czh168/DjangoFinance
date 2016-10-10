from django.contrib import admin
from Finance.models import *
# Register your models here.
#base**************************************************************************
class Agency_Admin(admin.ModelAdmin):
    list_display=('name','comment')
admin.site.register(Agency,Agency_Admin)

class Account_Admin(admin.ModelAdmin):
    list_display=('name','comment')
admin.site.register(Account,Account_Admin)

class InvestType_Admin(admin.ModelAdmin):
    list_display=('name','subname','risk','liquidity','comment')
admin.site.register(InvestType,InvestType_Admin)

class IntrestType_Admin(admin.ModelAdmin):
    list_display=('name','comment')
admin.site.register(IntrestType,IntrestType_Admin)

class StockFundInfo_Admin(admin.ModelAdmin):
    list_display=('name','code','price','type')
    actions=['setprice',]
    
    def setprice(self,request,queryset):
        for sf in queryset:
            sf.setprice()
    setprice.short_description="从互联网更新价格"
admin.site.register(StockFundInfo,StockFundInfo_Admin)

#main****************************************************************************
class FixedIcome_Admin(admin.ModelAdmin):
    list_display=('name','agency','account','spend','investtype','buydate','maturity','intrestype','annualizedyield','discount','comment','completed')
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
    list_display=('happenddate','amount','relatefixedincome')
admin.site.register(FixedIncomeCashFlow,FixedIncomeCashFlow_Admin)