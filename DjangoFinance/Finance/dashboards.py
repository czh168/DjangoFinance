from controlcenter import Dashboard, widgets
from Finance.models import *

class FixedIncomeItemList(widgets.ItemList):
    title='固定资产列表'
    model = FixedIncome
    list_display = ('name', 'spend')

class FixedIncomeSinglePieChart(widgets.SinglePieChart):
    # label and series
    title='固定资产饼图'
    values_list = ('name', 'spend')
    # Data source
    queryset = FixedIncome.objects

class MyDashboard(Dashboard):
    title = "理财统计"
    widgets = (
         widgets.Group([FixedIncomeItemList,FixedIncomeSinglePieChart], width=widgets.LARGER, height=300), widgets.Group([FixedIncomeItemList,FixedIncomeSinglePieChart], width=widgets.LARGER, height=300),
    )


