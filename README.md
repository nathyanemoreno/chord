# Chord Algorithm

### A simple implementation of the Chord Distributed Hash Table in Python

Use `test.py` to test the code.

#### Command examples

- Create a DHT:
`d = DHT(n)`
- Create a node and make node join the DHT:
`d.join(Node(m))`
- Add data to the node:
`d.store(d._startNode, key, value)`
-Look up a key in the DHT
`d.lookup(d._startNode, key)`
