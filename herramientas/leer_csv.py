# Modulo realizado por Jhon Monrroy
# jrmr100@gmail
# OBJETIVO: Agregar numero de cuenta a la 
# descripcion de las interfaces
# ALGORTIMO:
# Recibe la ubicacion del archivo y lista con 
# los campos a buscar, retorna lista (separada con "|")
#  con los datos encontrados 

import csv

def leer_lineas(archivo_csv, lista_campos):
    with open(archivo_csv, 'r') as archivo_read:
        encontrados_dict = csv.DictReader(archivo_read)
        lista_salida =[]
        for linea_csv in encontrados_dict:
            almacen_linea =""
            for campo in lista_campos:
                almacen_linea = almacen_linea + str(linea_csv[campo]) + "|"
            almacen_linea = almacen_linea[:-1]    # elimino la ultima comma
            lista_salida.append(almacen_linea)
    return lista_salida
