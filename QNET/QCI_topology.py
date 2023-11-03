import os
from qcompute_qnet.core.des import DESEnv
from qcompute_qnet.topology.network import Network


# Create an environment for simulation
env = DESEnv("QKD Network Architecture", default=True)
# Create the network for Beijing quantum metropolitan area network
network = Network("QCI")

# Set path of the JSON file for network topology configuration
#change path 
filename = "/home/ubuntuvm//Desktop/qnet/QCI.json"
filename = os.path.abspath(filename)

# Load the network topology from the file
network.load_topology_from(filename)

# Print the quantum network topology by the geographical locations of the nodes
network.print_quantum_topology(geo=True)

# Get end nodes by their names
irb = env.get_node("FPZ")
osijek = env.get_node("FER")

# IRB -> Osijek
irb.key_request(dst=osijek, key_num=20, key_length=512)

# Initialize and run the simulation
env.init()
env.run(logging=True)
