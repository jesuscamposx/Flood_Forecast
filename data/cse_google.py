from googleapiclient.discovery import build
from datetime import date
from calendar import monthrange
import csv


API_KEY = "AIzaSyB-1e2lUaoS4Bnr4sG1iNMR810OozBfy3s"
CSE_ID = "001823884054433059105:80uptpizvb8"
START_YEAR = 2010
END_YEAR = 2020
orTerms = "GAM Gustavo A. Madero lluvias Distrito Federal DF D.F. encharcamiento inundacion"
FILE_NAME = "./data/files/urls_inundacion.csv"
NUM=10

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().siterestrict().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res


def last_day_of_month(date_value):
    return date_value.replace(day=monthrange(date_value.year, date_value.month)[1])


def initiliaze_file(file):
    f = open(file, "w", newline='')
    w = csv.writer(f)
    w.writerow(["[URL]", "[Titulo]", "[Fecha]", "[Snippet]"])
    f.close()

def add_or_terms(year):
    return year >= 2012

initiliaze_file(FILE_NAME)
for year in range(START_YEAR, END_YEAR + 1):
    year_file = "./data/files/urls_" + str(year) + ".csv"
    initiliaze_file(year_file)
    e_month = 7 if year == 2020 else 13
    q = "lluvias inundacion distrito federal mexico" if year <= 2016 else "lluvias inundacion cdmx"  # noqa
    f = open(FILE_NAME, "a+", newline='', encoding="utf-8")
    f_y = open(year_file, "a+", newline='', encoding="utf-8")
    w_y = csv.writer(f_y)
    w = csv.writer(f)
    for month in range(1, e_month):
        f_day = date(year, month, 1)
        l_day = last_day_of_month(f_day)
        sort = "date:r:" + f_day.strftime("%Y%m%d") + ":" + l_day.strftime("%Y%m%d")
        print(sort)
        start = 1
        while 1:
            try:
                print(start)
                result = google_search(q, API_KEY, CSE_ID,
                                       sort=sort,
                                       filter=1,
                                       orTerms=orTerms if add_or_terms(year) else None,
                                       num=NUM,
                                       start=start
                                       )
                items = result.get("items")
                nextPage = result["queries"].get("nextPage")
                #print(result["queries"])
                #print("____________________________________")
                if items is not None:
                    for item in items:
                        lk = item["link"]
                        tt = item["title"]
                        dt = item["snippet"].split(" ... ")[0]
                        sp = item["snippet"]
                        #print([lk, tt, dt])
                        w.writerow([lk, tt, dt, sp])
                        w_y.writerow([lk, tt, dt, sp])

                if nextPage is None or start >= 91:
                    break
            except Exception as e:
                print(str(e))
            finally:
                start += 10
    f.close()
    f_y.close()
