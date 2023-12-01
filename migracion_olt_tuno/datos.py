vlan_nueva = "1860"
vlan_vieja = "3313"
nombre_vlan = "TUNO-LASER-LAS-MERCE"
interface_vieja = """interface TenGigabitEthernet0/3/0.3313
 description LASER-LAS-MERCE;ID:26533
 bandwidth 153600
 encapsulation dot1Q 3313
 ip address 172.23.238.77 255.255.255.252
 service-policy input 150M
 service-policy output 150M"""
rutas_ip = """ip route 190.94.224.72 255.255.255.252 172.23.238.78 name GPON-V3313-TUNO-LASER-LAS-MERCE"""