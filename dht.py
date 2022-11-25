# A Distributed Hash Table implementation

class Node:
    def __init__(self, id, next = None, prev = None):
        self.id = id
        self.data = dict()
        self.prev = prev
        self.fingerTable = [next]

    # Update the finger table of this node when necessary
    def fix_finger_table(self, dht, k):
        del self.fingerTable[1:]
        for i in range(1, k):
            self.fingerTable.append(dht.find_node(dht._startNode, self.id + 3 ** i))

        
class DHT:
    # The total number of IDs available in the DHT is 2 ** k
    def __init__(self, k):
        self._k = k
        self._size = 2 ** k    
        self._startNode = Node(0, k)
        self._startNode.fingerTable[0] = self._startNode
        self._startNode.prev = self._startNode
        self._startNode.fix_finger_table(self, k)

    def get_hash_id(self, key):
        return key % self._size

    # Get distance between to IDs
    def distance(self, n1, n2):
        if n1 == n2:
            return 0
        if n1 < n2:
            return n2 - n1
        return self._size - n1 + n2

    # Get number of nodes
    def get_num_node(self):
        if self._startNode == None:
            return 0
        node = self._startNode
        n = 1
        while node.fingerTable[0] != self._startNode:
            n = n + 1
            node = node.fingerTable[0]
        return n
    
    # Find the node which holds the key
    def find_node(self, start, key):
        hashId = self.get_hash_id(key)
        curr = start
        numJumps = 0
        while True:
            if curr.id == hashId:
                print("Node: ", curr.id)
                return curr
            if self.distance(curr.id, hashId) <= self.distance(curr.fingerTable[0].id, hashId):
                #print("number of jumps: ", numJumps)
                print("Hash id: ", hashId)
                return curr.fingerTable[0]
            tabSize = len(curr.fingerTable)
            i = 0;
            nextNode = curr.fingerTable[-1]
            while i < tabSize - 1:
                if self.distance(curr.fingerTable[i].id, hashId) < self.distance(curr.fingerTable[i + 1].id, hashId):
                    nextNode = curr.fingerTable[i]
                i = i + 1
            #if(curr.id != nextNode.id):
            #    print("Hash id: ", nextNode.id)
            #print("number of jumps: ", numJumps)
            curr = nextNode
            numJumps += 1
            

    # Look up a key in the DHT
    def lookup(self, start, key):
        nodeForKey = self.find_node(start, key)
        if key in nodeForKey.data:
            print("The key is in node: ", nodeForKey.id)
            return nodeForKey.data[key]
        return "Key not found"

    # Store a key-value pair in the DHT
    def store(self, start, key, value):
        nodeForKey = self.find_node(start, key)
        nodeForKey.data[key] = value

    # Routine for new node joining the system
    def join(self, newNode):
        # Find the node before which the new node should be inserted
        rootNode = self.find_node(self._startNode, newNode.id)

        # print(rootNode.id, "  ", newNode.id)
        # If there is a node with the same id, decline the join request for now
        if rootNode.id == newNode.id:
            print("Node with id already exists!")
            return
        
        # Copy the key-value pairs that will belong to the new node after
        # the node is inserted in the system
        for key in rootNode.data:
            hashId = self.get_hash_id(key)
            if self.distance(hashId, newNode.id) < self.distance(hashId, rootNode.id):
                newNode.data[key] = rootNode.data[key]

        # Update the prev and next pointers
        prevNode = rootNode.prev
        newNode.fingerTable[0] = rootNode
        newNode.prev = prevNode
        rootNode.prev = newNode
        prevNode.fingerTable[0] = newNode
    
        # Configure finger table for new node
        newNode.fix_finger_table(self, self._k)

        # Delete keys that have been moved to new node
        for key in list(rootNode.data.keys()):
            hashId = self.get_hash_id(key)
            if self.distance(hashId, newNode.id) < self.distance(hashId, rootNode.id):
                del rootNode.data[key]
                
    
    def leave(self, node):
        # Copy all its key-value pairs to its successor in the system
        for k, v in node.data.items():
            node.fingerTable[0].data[k] = v
        # If only node in the system
        if node.fingerTable[0] == node:
            self._startNode = None
        else:
            node.prev.fingerTable[0] = node.fingerTable[0]
            node.fingerTable[0] = prev = node.prev
            # If deleted node was an entry point to the system,
            # choose another entry point, in this case its successor
            if self._startNode == node:
                self._startNode = node.fingerTable[0]
    
    def fix_all_finger_tables(self):
        self._startNode.fix_finger_table(self, self._k)
        curr = self._startNode.fingerTable[0]
        while curr != self._startNode:
            curr.fix_finger_table(self, self._k)
            curr = curr.fingerTable[0]