import csv
import sys
sys.path.append('/home/pi/Desktop/SantaFridge/Modulos/sensors')
from rfid import admin_actions

def add_inventario(data):
    with open(r'/home/pi/Desktop/SantaFridge/Modulos/db/inventario.csv','a')as f:
        writer = csv.writer(f)
        writer.writerow(data)

def write_csv(data):
    with open(r'/home/pi/Desktop/SantaFridge/Modulos/db/inventario.csv','w')as f:
        writer = csv.writer(f)
        writer.writerows(data)


def query_product(id):
    if id == 184511698440:
        print("Hola Admin")
        admin_actions()
    else:
        with open('/home/pi/Desktop/SantaFridge/Modulos/db/inventario.csv','r')as f:
            reader = csv.reader(f)
            nombre = ""
            sku = ""
            changes = []
            for row in reader:
                if int(row[0]) == id:
                    nombre = row[2]
                    sku = row[1]

                    #CAMBIAR VALOR 'CANTIDAD' DEL INVENTARIO
                    temp = int(row[3])
                    temp -= 1
                    row[3] = str(temp)

                changes.append(row)
            write_csv(changes)
            data = [sku,nombre,id]
            return data