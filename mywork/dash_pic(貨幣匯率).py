from django.shortcuts import render
from django.http import JsonResponse
from ..mywork.currency_scrape import *
import datetime


def callback(request):
    currencies = list(RateScrape.currencies.keys())
    init_cur = '美金'
    return render(request, "new_currency.html", locals())


def currency_ajax(request, currency):
    select = currency.split('&')  # 將網址split 得到個參數 []
    print(select)
    choice = RateScrape.currencies[select[0]]
    currency = RateScrape(choice, int(select[2]))
    x_data = list(map(lambda x: x[0], currency.all_rate))
    if select[3] == '現金匯率':
        y1_data = list(map(lambda x: x[1], currency.all_rate))
        y2_data = list(map(lambda x: x[2], currency.all_rate))
    else:
        y1_data = list(map(lambda x: x[3], currency.all_rate))
        y2_data = list(map(lambda x: x[4], currency.all_rate))
    x_axis_range_min = str(get_startDate(x_data[-1]))
    x_axis_range_max = str(get_endDate(x_data[0]))

    if select[1] != 'None':
        compare = RateScrape.currencies[select[1]]
        compare_currency = RateScrape(compare, int(select[2]))
        if select[3] == '現金匯率':
            y1com_data = list(map(lambda x: x[1], compare_currency.all_rate))
            y2com_data = list(map(lambda x: x[2], compare_currency.all_rate))
        else:
            y1com_data = list(map(lambda x: x[3], compare_currency.all_rate))
            y2com_data = list(map(lambda x: x[4], compare_currency.all_rate))
        return JsonResponse(
            [x_data, [y1_data, y2_data, y1com_data, y2com_data], [choice, compare], x_axis_range_min, x_axis_range_max,
             select[3]],
            safe=False)

    return JsonResponse([x_data, [y1_data, y2_data], select, x_axis_range_min, x_axis_range_max, select[3]], safe=False)


def get_startDate(date):
    """圖表資料起始日期"""
    date = date.split('-')
    date = datetime.datetime(year=int(date[0]), month=int(date[1]), day=int(date[2])).date()
    delta = datetime.timedelta(days=4)
    date -= delta
    return date


def get_endDate(date):
    """圖表資料結束日期"""
    date = date.split('-')
    date = datetime.datetime(year=int(date[0]), month=int(date[1]), day=int(date[2])).date()
    delta = datetime.timedelta(days=4)
    date += delta
    return date
