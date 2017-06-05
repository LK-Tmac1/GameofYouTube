#!/usr/bin/env bash

# Start zookeeper and kafka manually
nohup bin/zookeeper-server-start.sh config/zookeeper.properties &
nohup bin/kafka-server-start.sh config/server.properties &

# Create a kafka topic
# Ensure replication factor no larger than available brokers
cd /usr/iop/current/kafka-broker/
bin/kafka-topics.sh --create --replication-factor 2  --partition 3 --topic video \
--zookeeper kunliu1.fyre.ibm.com:2181,kunliu10.fyre.ibm.com:2181,kunliu2.fyre.ibm.com:2181
# Successful message: Created topic "user-behavior-topic".

# Start producer/consumer console
bin/kafka-console-producer.sh --broker-list kunliu1.fyre.ibm.com:6667 --topic user-behavior-topic
# 9092 is the default port of listeners, in IOP it is 6667
bin/kafka-console-consumer.sh --zookeeper kunliu1.fyre.ibm.com:2181 --topic video --from-beginning
bin/kafka-console-consumer.sh --bootstrap-server kunliu1.fyre.ibm.com:6667 --topic video --from-beginning
# Using the ConsoleConsumer with old consumer is deprecated and will be removed in a future major release.
# Consider using the new consumer by passing [bootstrap-server] instead of [zookeeper].


producer.py --producer=kafka --source_mode=video --videos=1,2,3,4,5 --bootstrap_servers=kunliu1.fyre.ibm.com:6667 --max_block_ms=1000
