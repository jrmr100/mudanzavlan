#!venv/bin/python

# Script realizado por JHON MONRROY jrmr100@gmail.com
# OBJETIVO: Migrar clientes desde un router / nterface a otro, incluyendo
# cambio de VLAN
# ALGORITMO:
# - Leo csv enviado por operaciones y obtengo:
#   - Nombre y Nro Vlan actual
#   - Nombre y Nro Vlan propuesto
# - Leo archivo netinfo
# - Busco con Nro de vlan actual en netinfo.csv equipo e interface actual
# - Creo archivo de salida.txt con comando adaptado al nuevo equipo / interface
# USO:
# - Preparar previamente los comandos de la ruta en un algoritmo
# - Agrego los datos de los INSUMOS requeridos
# - configuro las funciones que genera los comandos segun el equipo
# - Busco manualmente las rutas estaticas para cambiarles el nombre

from herramientas.leer_csv import leer_lineas

# INSUMOS:
csv_oper = "fuente-operaciones.csv"  # Archivo enviado por operaciones
lista_campos_oper = ["Vlan Name", "Nombre a Cambiar", "Current Vlan",
                     "New Vlan"]  # Campos a leer del csv enviado
lista_campos_netinfo = ["NOMBRE_EQUIPO", "INTERFACE", "NOMBRE_CLIENTE",
                        "NRO_VLAN", "DIRECCION_IP", "VELOCIDAD_ENTRADA",
                        "VELOCIDAD_SALIDA"]  # Campos a leer del csv netinfo
csv_netinfo = "netinfo.csv"  # Ultima version del netinfo.csv
comandos = "Comandos_generados.txt"  # archivo de salida con los comandos
conexion1 = "ssh soporte2@181.225.41.18"
interface_router_recibe = "TenGigabitEthernet1/0/3"
nombre_sw_jun = "CCSJ4500CREX2"
conex_sw1 = "ssh soporte2@172.23.253.59"
int_red_sw1 = "ae6"
int_router_sw1 = "xe-0/0/9"
nombre_sw_cisco = "CCS3064GALIX1"
conex_sw2 = "ssh soporte2@172.23.253.46"
int_red_sw2 = "Eth1/8"

# Leo y creo lista de campos de los archivos de operaciones y netinfo
lineas_oper = leer_lineas(csv_oper, lista_campos_oper)
lineas_netinfo = leer_lineas(csv_netinfo, lista_campos_netinfo)

# Creo archivo de salida
with open(comandos, 'w') as comandos_file:
    comandos_file.writelines("")


def router_cisco(nombre_cliente, equipo_actual, conexion1, delete_interface,
                 interface_recibe, description, bandwidth, vlan_new,
                 ip_address, policy, nombre_cliente_oper):
    encabezado = "################" + nombre_cliente + "###############\n"
    eq_actual = "----------" + equipo_actual + "-----------\n"
    conex1 = conexion1 + "\n\n"
    del_int = "no interface " + delete_interface + "\n"
    int_rec = "interface " + interface_recibe + "\n"
    descr = "description " + description + "\n"
    bw = "bandwidth " + str(bandwidth) + "\n"
    encap = "encapsulation dot1Q " + vlan_new + "\n"
    ip = "ip address " + ip_address + "\n"
    speed = "service-policy input " + policy + "\n" +\
        "service-policy output " + policy + "\n\n"

    # Creo la ip wan remota para buscar la estatica
    # valido q sea una IP valida y formato cisco
    if "." in ip_address and "/" not in ip_address:
        ip_wan = ip_address.split(" ")
        octeto = ip_wan[0].split(".")
        octeto_remoto = int(octeto[3]) + 1
        ruta_estatica = "sh run | in " + octeto[0] + "." + octeto[1] + "." +\
            octeto[2] + "." + str(octeto_remoto) + "\n\n"
    else:
        ruta_estatica = "FORMATO IP NO VALIDO!!!\n" + ip_address
    name_static = "GPON-VL" + vlan_new + "-" + nombre_cliente_oper + "\n\n"

    comando_final_cisco = encabezado + eq_actual + conex1 + del_int + int_rec\
        + descr + bw + encap + ip + speed + ruta_estatica + name_static
    with open(comandos, 'a') as comandos_file:
        comandos_file.writelines(comando_final_cisco)


def sw_juniper(nombre_sw1, conex_sw1, nombre_cliente_oper, vlan_new,
               int_red_sw1, int_router_sw1):
    eq_actual = "----------" + nombre_sw1 + "-----------\n"
    conex1 = conex_sw1 + "\n\n"
    crear_vlan = "set vlan " + nombre_cliente_oper + " vlan-id " + vlan_new + "\n"
    permiso1 = "set interfaces " + int_red_sw1 +\
        " unit 0 family ethernet-switching vlan members " +\
        nombre_cliente_oper + "\n"
    permiso2 = "set interfaces " + int_router_sw1 +\
        " unit 0 family ethernet-switching vlan members " +\
        nombre_cliente_oper + "\n\n"

    comando_final_juniper = eq_actual + conex1 + crear_vlan +\
        permiso1 + permiso2
    with open(comandos, 'a') as comandos_file:
        comandos_file.writelines(comando_final_juniper)


def sw_cisco(nombre_sw_cisco, conex_sw2, nombre_cliente_oper,
             vlan_new, int_red_sw2):
    eq_actual = "----------" + nombre_sw_cisco + "-----------\n"
    conex1 = conex_sw2 + "\n\n"
    crear_vlan = "vlan " + vlan_new + "\n" + "name " + nombre_cliente_oper + "\n"
    permiso1 = "interface " + int_red_sw2 + "\n" +\
        "switchport trunk allowed vlan add " + vlan_new + "\n\n"

    comando_final_juniper = eq_actual + conex1 + crear_vlan + permiso1
    with open(comandos, 'a') as comandos_file:
        comandos_file.writelines(comando_final_juniper)


for linea_oper in lineas_oper:
    lista_linea_oper = linea_oper.split("|")
    for linea_netinfo in lineas_netinfo:
        lista_linea_netinfo = linea_netinfo.split("|")
        if lista_linea_oper[2] in lista_linea_netinfo[3]:
            # Valido si piden cambio de nombre de vlan
            if lista_linea_oper[1] != "":
                lista_linea_oper[0] = lista_linea_oper[1]
            # lleno las variables con los datos obtenidos
            nombre_cliente_netinfo = lista_linea_netinfo[2]
            nombre_cliente_oper = lista_linea_oper[0]
            equipo_actual = lista_linea_netinfo[0]
            delete_interface = lista_linea_netinfo[1]
            interface_recibe = interface_router_recibe + "."\
                + str(lista_linea_oper[3])
            description = lista_linea_netinfo[2]
            if lista_linea_netinfo[5][:-1] != "":
                bandwidth = int(lista_linea_netinfo[5][:-1]) * 1024
            vlan_new = str(lista_linea_oper[3])
            ip_address = lista_linea_netinfo[4]
            policy = lista_linea_netinfo[5]

            # paso los parametros a la funcion q crea comandos
            router_cisco(nombre_cliente_netinfo, equipo_actual, conexion1,
                         delete_interface, interface_recibe, description,
                         bandwidth, vlan_new, ip_address, policy,
                         nombre_cliente_oper)
            sw_juniper(nombre_sw_jun, conex_sw1, nombre_cliente_oper, vlan_new,
                       int_red_sw1, int_router_sw1)
            sw_cisco(nombre_sw_cisco, conex_sw2, nombre_cliente_oper,
                     vlan_new, int_red_sw2)

print("\nComandos generados en " + comandos + "\n")
