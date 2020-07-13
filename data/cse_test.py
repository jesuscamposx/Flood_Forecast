from googleapiclient.discovery import build
import csv

API_KEY = "AIzaSyB-1e2lUaoS4Bnr4sG1iNMR810OozBfy3s"
CSE_ID = "001823884054433059105:80uptpizvb8"


def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().siterestrict().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res





result = google_search("lluvias inundacion cdmx", API_KEY, CSE_ID,
                               sort="date:r:20190101:20191201",
                               filter=1,
                               orTerms="GAM+Gustavo A. Madero lluvias Distrito Federal DF D.F. encharcamiento inundacion"
                               )

#print(result["queries"]["previousPage"])
print(result["queries"]["request"])
print(result["queries"]["nextPage"])

for item in result["items"]:
    print(item["title"] + "    " + item["snippet"] + "    " + item["link"])