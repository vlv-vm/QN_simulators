from qcompute_qnet.core.des import DESEnv
from qcompute_qnet.topology.network import Network
from qcompute_qnet.models.qkd.node import QKDNode
from qcompute_qnet.topology.link import Link
from qcompute_qnet.devices.channel import ClassicalFiberChannel, QuantumFiberChannel
from qcompute_qnet.models.qkd.key_generation import PrepareAndMeasure

#Experimental devices configuration
#source_options = {"frequency": 2e6, "mean_photon_num": 0.1}
#detector_options = {"efficiency": 0.275, "dark_count": 0.7, "count_rate": 10e3, "resolution": 10}
source_options = {"frequency": 2e6, "mean_photon_num": 0.1}
detector_options = {"efficiency": 0.1, "dark_count": 800.0, "count_rate": 10e4, "resolution": 10}

# 1. Create the simulation environment and set as default
env = DESEnv("BB84", default=True)

# 2. Create a quantum network
network = Network("BB84 Network")

# 3. Create the QKD nodes and load protocol + add source and detector options to nodoes
alice = QKDNode("Alice")
alice.photon_source.set(**source_options)
bob = QKDNode("Bob")
bob.polar_detector.set_detectors(**detector_options)

# Set the protocols and build the protocol stacks
bb84_alice = alice.set_key_generation(bob)
alice.protocol_stack.build(bb84_alice)
bb84_bob = bob.set_key_generation(alice)
bob.protocol_stack.build(bb84_bob)

# 4. Create and connect the link
link_ab = Link("A_B", ends=(alice, bob))

# 4.1 Create the channels and connect the nodes
cchannel1 = ClassicalFiberChannel("c_A2B", sender=alice, receiver=bob, distance=7.8e3)
cchannel2 = ClassicalFiberChannel("c_B2A", sender=bob, receiver=alice, distance=7.8e3)
qchannel = QuantumFiberChannel("q_A2B", sender=alice, receiver=bob, distance=7.8e3)

# 4.2 Install the channels to the link
link_ab.install([cchannel1, cchannel2, qchannel])

# 5. Install the nodes and the link to the network
network.install([alice, bob, link_ab])

# 6. Set parameters (role, key number, key length) for the start of protocol stacks
alice.protocol_stack.start(role=PrepareAndMeasure.Role.TRANSMITTER, key_num=20, key_length=256)
bob.protocol_stack.start(role=PrepareAndMeasure.Role.RECEIVER, key_num=20, key_length=256)

# 7. Initialize the environment and run simulation with log records turned on
env.init()
env.run(logging=True)
