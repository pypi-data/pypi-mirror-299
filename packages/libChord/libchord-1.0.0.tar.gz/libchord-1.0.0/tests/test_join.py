from libChord import chord
import time

port=57429
ipaddr="192.168.56.1"

my_node = chord.join(port=port, ip_addr=ipaddr)
print(my_node.ip_addr)
print(my_node.port)
print("ID: ", my_node.id)

while True:
    time.sleep(15)
    print("SUCC ID: ", my_node.successor_id)
    print("PRED ID: ", my_node.predecessor_id)

    # command = int(input("Enter command: "))
    # if command == 0:
    #     pass
    # elif command == 1:
    #     pass
    # elif command == 2:
    #     pass
    # elif command == 3:
    #     print("SUCC ID: ", my_node.successor_id)
    # elif command == 4:
    #     print("PRED ID: ", my_node.predecessor_id)
    # elif command == 5:
    #     my_node.leave()
    # else:
    #    break


