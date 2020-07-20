import googlemaps
import csv

FILE_NAME_FROM = "./data/files/atlas-de-riesgo-inundaciones_gam.csv"
FILE_NAME_TO = "./data/files/atlas-de-riesgo-inundaciones_gam_nombres.csv"
KEY = 'AIzaSyB-1e2lUaoS4Bnr4sG1iNMR810OozBfy3s'

i = 0
gmaps = googlemaps.Client(key=KEY)
with open(FILE_NAME_FROM, 'r', newline='', encoding="utf-8") as f_f:
    reader_f = csv.reader(f_f)
    with open(FILE_NAME_TO, 'w', newline='', encoding="utf-8") as f_t:
        writer_t = csv.writer(f_t)
        for r in reader_f:
            i += 1
            print('Procesando registro numero ' + str(i))
            if r[10] == 'Alcaldía':
                r.append('ID Lugar')
                r.append('Dirección')
                r.append('Número')
                r.append('Calle')
                r.append('Colonia')
                r.append('Alcaldia')
                r.append('Ciudad')
                r.append('País')
                r.append('Código postal')
            else:
                result = gmaps.reverse_geocode((r[0]))
                result = result[0]
                r.append(result['place_id'])
                r.append(result['formatted_address'])
                for element in result['address_components']:
                    if 'locality' in element['types']:
                        r.append(r[10])
                    else:
                        r.append(element['long_name'])
            writer_t.writerow(r)
