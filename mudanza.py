import csv

csv_vlan = "vlan.csv"
csv_netinfo = "netinfo.csv"
csv_resultado = "resultado.csv"

with open(csv_resultado, 'w') as resultado_file:
    datos_resultados = "NOMBRE_EQUIPO," + "NOMBRE_VLAN,"\
                       + "COMANDO_DEL," + "COMANDO_ADD," + "COMANDO_IP\n"
    resultado_file.writelines(datos_resultados)


with open(csv_vlan, 'r') as vlan_file:
    vlan_dict = csv.DictReader(vlan_file)
    for vlan_line in vlan_dict:
        vlan_nodo = vlan_line["Nodo"]
        vlan_nombre = vlan_line["Vlan Name"]
        vlan_actual = vlan_line["Current Vlan"]
        vlan_nueva = vlan_line["New Vlan"]
        vlan_servicio = vlan_line["Servicio"]
        with open(csv_netinfo, 'r') as netinfo_file:
            netinfo_dict = csv.DictReader(netinfo_file)
            for netinfo_line in netinfo_dict:
                netinfo_nombre = netinfo_line["NOMBRE_CLIENTE"]
                netinfo_equipo = netinfo_line["NOMBRE_EQUIPO"]
                netinfo_interface = netinfo_line["INTERFACE"]
                netinfo_vlan_num = netinfo_line["NRO_VLAN"]
                netinfo_ip = netinfo_line["DIRECCION_IP"]
                if vlan_nombre != "" and vlan_nombre == netinfo_nombre:
                    if "J" in netinfo_equipo:
                        juniper_final = netinfo_equipo + "," + vlan_nombre + ",del interfaces "\
                                        + netinfo_interface + "unit " + netinfo_vlan_num\
                                        + ",interface Te0/3/0." + str(vlan_nueva)\
                                        + ",ip address " + netinfo_ip + "\n"
                        with open(csv_resultado, 'a') as resultado_file:
                            resultado_file.writelines(juniper_final)
                    else:
                        cisco_final = netinfo_equipo + "," + vlan_nombre + ",no interface "\
                                      + netinfo_interface + ","\
                                      + "interface Te0/3/0." + str(vlan_nueva)\
                                      + ",ip address " + netinfo_ip + "\n"
                        with open(csv_resultado, 'a') as resultado_file:
                            resultado_file.writelines(cisco_final)
                