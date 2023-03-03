
from pyvis.network import Network
from scapy.all import ARP, Ether, srp, conf
import csv
import pandas as pd

def arp_scan():

    gw = conf.route.route("0.0.0.0")[2]

    arp = ARP(pdst=gw+"/24")

    ether = Ether(dst="ff:ff:ff:ff:ff:ff")

    packet = ether/arp
    packet.show()


    result = srp(packet, timeout=3)[0]


    clients = []


        
    for sent, received in result:

        # for each response, append ip and mac address to 'clients' list
        clients.append({'ip': received.psrc, 'mac': received.hwsrc})
        #print({'ip': received.psrc, 'mac': received.hwsrc})

    print("Available devices in the network:")
    print("IP" + " "*18+"MAC")
    with open("local_network.csv", "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["IP", "MAC"])
        for client in clients:
            writer.writerow([client['ip'], client['mac']])
            print("{:16}    {}".format(client['ip'], client['mac']))

arp_scan()

got_data = pd.read_csv("local_network.csv")

net = Network()

print("NOW DISPLAYING GOT DATA")
print(got_data)

i = 1
gw = conf.route.route("0.0.0.0")[2]

for i in range(len(got_data)):
    print(got_data['IP'][i])
    if got_data["IP"][i] == gw:
        net.add_node(got_data["IP"][i], title=f"MAC: {got_data['MAC'][i]}", color="green")
    else:
        net.add_node(got_data["IP"][i], title=f"MAC: {got_data['MAC'][i]}")
    if got_data["IP"][i] != gw:
        net.add_edge(gw,got_data['IP'][i])
    else:
        pass




#net.add_edges([(gw,got_data['IP'][1])])


#net.add_nodes([3, 4, 5, 6], 
#              label=['Michael', 'Ben', 'Oliver', 'Olivia'],
#              color=['#3da831', '#9a31a8', '#3155a8', '#eb4034'])

net.show('basic.html', notebook=False)