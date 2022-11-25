# Tests for dht
from dht import *
from random import randint

d = DHT(10)

# Adding nodes
for i in range(0, 50):
    r = randint(0, 10240)
    d.join(Node(r))

d.fix_all_finger_tables()

# Saving data on nodes
for i in range(5, 50):
    d.store(d._startNode, i, "Data: " + str(i))


#for i in range(0, 10):
#	temp = d.lookup(d._startNode, i)
#	if(temp!= None):
#		print(temp)

#for i in range(5, 200, 10):
#    print(d.distance(0, i))


#d.store(d._startNode, 20, "Data: " + str(5))

print(d.lookup(d._startNode, 5))
print(f"Total number of nodes: {d.get_num_node()}")