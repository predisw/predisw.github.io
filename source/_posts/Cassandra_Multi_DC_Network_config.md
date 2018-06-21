---
title: Cassandra_Multi_DC_Network_config
date: 2018-06-21 18:57:06
categories:
- db
tags:
- cassandra
---
### Multi Network Interfaces Using in Multi DC 


#### cassandra.yaml 

1. In the cassandra.yaml, set the `listen_address`(for communication within the local datacenter) to the private IP address of the node, and the `broadcast_address` (for communication between datacenters)to the public address of the node.


2. Set the addresses of the seed nodes in the `cassandra.yaml` file to that of the public IP. Private IP are not routable between networks.

    > Be sure to enable encryption and authentication when using public IPs. See [Node-to-node](https://docs.datastax.com/en/cassandra/3.0/cassandra/configuration/secureSSLNodeToNode.html) encryption. Another option is to use a custom VPN to have local, inter-region/ datacenter IPs.


3. `listen_on_broadcast_address: true`  The public address to private address routing is not automatically enabled. Enabling `listen_on_broadcast_address` allows Cassandra to listen on both `listen_address` and `broadcast_address` with two network interfaces

#### cassandra-rackdc.properties

1. Define the datacenter and Rack that include this node. The default settings:
```
dc=DC1
rack=RAC1
```
Note: datacenter and rack names are case-sensitive.

2. `prefer_local=true` Enable the option `prefer_local` to ensure that traffic to broadcast_address will re-route to listen_address. And This option tells Cassandra to use the local IP address when communication is not across different datacenters


#### Case:

- **env:**
    - dc1
    - cassandra1-1
        - eth1:10.175.188.47
        - eth2:192.168.0.6
        - eth3:10.175.189.7

    - dc2
    - cassandra2-1
        - eth1:10.175.187.79
        - eth2:192.168.0.6
        - eth3:10.175.189.4



- **requirement**
    - eth1 receive traffic from application client
    - eth0 sync data between cassandra nodes in local data center
    - eth2 sync data between data center 


- **here is the configuration for cassandra2-1 in dc2 **

    - **for cassandra.yaml**
    ```
    - seeds: 10.175.189.4,10.175.189.5,10.175.189.7,10.175.189.8
    listen_address: 192.168.0.6
    broadcast_address: 10.175.189.4
    listen_on_broadcast_address: true

    rpc_address: 0.0.0.0                  # for sake of eth1 receive traffic from application client
    broadcast_rpc_address: 10.175.187.79  # for sake of eth1 receive traffic from application client

    endpoint_snitch: GossipingPropertyFileSnitch
    ```

    - ** for cassandra-rackdc.properties**
    ```
    dc=dc2
    rack=cassandra_rack

    prefer_local=true

    ```

