
from pyvis.network import Network
from scapy.all import ARP, Ether, srp, conf
import csv
import pandas as pd
import mac_details
import time

def arp_scan():

    global gw_mac

    gw = conf.route.route("0.0.0.0")[2]

    arp = ARP(pdst=gw+"/24")

    ether = Ether(dst="ff:ff:ff:ff:ff:ff")

    packet = ether/arp
    packet.show()


    result = srp(packet, timeout=3)[0]


    clients = []


        
    for sent, received in result:
        vendor = mac_details.get_mac_details(received.hwsrc).split()
        vendor = str(vendor[0])
        if gw == received.psrc:
            gw_mac = received.hwsrc
            clients.append({'ip': received.psrc, 'mac': received.hwsrc, 'vendor': vendor, 'gateway': 'y'})
        # for each response, append ip and mac address to 'clients' list
        else:
            clients.append({'ip': received.psrc, 'mac': received.hwsrc, 'vendor': vendor, 'gateway': 'n' })
        #print({'ip': received.psrc, 'mac': received.hwsrc})
        

    print("Available devices in the network:")
    print("IP" + " "*18+"MAC"+" "*18+"VENDOR")
    with open("local_network.csv", "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["IP", "MAC", "VENDOR", "GATEWAY"])
        for client in clients:
            writer.writerow([client['ip'], client['mac'], client['vendor'], client['gateway']])
            print("{:16}    {}".format(client['ip'], client['mac'], client["vendor"], client["gateway"]))

ask = input("Wanna re-scan? (y/n) : ")
if(ask == 'y'):
    arp_scan()
    gw = conf.route.route("0.0.0.0")[2]
    gw_vendor = mac_details.get_mac_details(gw_mac).split()
    gw_vendor = str(gw_vendor[0])
else:
    pass

got_data = pd.read_csv("local_network.csv")

net = Network()

print("NOW DISPLAYING GOT DATA")
print(got_data)
gw = conf.route.route("0.0.0.0")[2]
i = 1

time.sleep(1)


for i in range(len(got_data)):
    print(got_data['IP'][i])
    #print(vendor)
    if got_data["GATEWAY"][i] == 'y':
        net.add_node(got_data["VENDOR"][i]+"\n"+got_data["IP"][i], title=f"MAC: {got_data['MAC'][i]}", color="green")
    else:
        net.add_node(got_data["VENDOR"][i]+"\n"+got_data["IP"][i], title=f"MAC: {got_data['MAC'][i]}")
    if got_data["GATEWAY"][i] != 'y':
        for k in range(len(got_data)):
            if got_data["GATEWAY"][k] == 'y':
                net.add_edge(got_data["VENDOR"][k]+"\n"+got_data["IP"][k],got_data["VENDOR"][i]+"\n"+got_data['IP'][i])
            else:
                pass
    else:
        pass




#net.add_edges([(gw,got_data['IP'][1])])



net.show('basic.html', notebook=False)
