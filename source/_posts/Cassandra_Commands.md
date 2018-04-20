---
title: Cassandra_Commands
date: 2018-04-20 23:49:40
categories:
- db
tags:
- cassandra
---
### Cassandra Commands

- remove cluster node when running
    nodetool decommission


- add cluster node when running

Fatal configuration error; unable to start server.  See log for stacktrace.
ERROR [main] 2018-04-18 16:34:04,674 CassandraDaemon.java:706 - Fatal configuration error
org.apache.cassandra.exceptions.ConfigurationException: This node was decommissioned and will not rejoin the ring unless cassandra.override_decommission=true has been set, or all existing data is removed and the node is bootstrapped again
