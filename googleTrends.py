from pytrends.request import TrendReq

pytrends = TrendReq(hl='en-US', tz=360)

kw_list = ["Tesla"]

interest = (pytrends.get_historical_interest(kw_list, year_start=2010, month_start=1, day_start=1, hour_start=0, year_end=2019, month_end=1, day_end=1, hour_end=0, cat=0, geo='', gprop='', sleep=0))


text_file = open("TSLA_trends.txt", "w")
text_file.write(interest)
text_file.close()

exit()
pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='', gprop='')
