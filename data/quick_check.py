import csv


f = open("./data/files/metricas.csv", 'r')
r = csv.reader(f)
data = []
for row in r:
    data.append(row)
data = data[3:-1]
f.close()

r_in_cdmx = 0
r_in_cdmx_lluvia = 0
r_in_gam = 0
r_in_gam_ll = 0
r_w_colonia = 0
for d in data:
    cdmx = int(d[2])
    inundacion = int(d[3])
    lluvia = int(d[4])
    gam = int(d[5])
    colonia = d[7]

    cdin = cdmx > 0 and inundacion > 0
    cdinll = cdin and lluvia > 0
    cdingam = cdin and gam > 0
    cdingamll = cdingam and lluvia > 0
    cdingamcol = cdingam and colonia

    if cdin:
        r_in_cdmx += 1
    if cdinll:
        r_in_cdmx_lluvia += 1
    if cdingam:
        r_in_gam += 1
    if cdingamll:
        r_in_gam_ll += 1
    if cdingamcol:
        r_w_colonia += 1

print("Total de registros: " + str(len(data)-1))
print("Registros en cdmx: " + str(r_in_cdmx))
print("Registros en cdmx con lluvia: " + str(r_in_cdmx_lluvia))
print("Registros en cdmx en GAM: " + str(r_in_gam))
print("Registros en cdmx en GAM con lluvia: " + str(r_in_gam_ll))
print("Registros en GAM con colonias: " + str(r_w_colonia))