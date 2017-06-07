#!/usr/bin/env bash

vi ~/.bash_profile
source ~/.bash_profile

# Get the aliases and functions
if [ -f ~/.bashrc ]; then
        . ~/.bashrc
fi

# User specific environment and startup programs

export PATH=/usr/local/share/man/man1/python2.7.1:$PATH

PATH=$PATH:$HOME/bin

export PATH

# Youtube project, all default arguments, can still change by overwriting

alias producer_kafka="/usr/iop/current/kafka-broker/bin/kafka-console-producer.sh --broker-list $HOSTNAME:6667 --topic view"

alias consumer_kafka="/usr/iop/current/kafka-broker/bin/kafka-console-consumer.sh --bootstrap-server $HOSTNAME:6667 --topic view"

export GIT_HOME="/root/GameofYouTube"

export YOUTUBE_HOME="$GIT_HOME/webapp/backend"

alias vi_producer="echo '' > $YOUTUBE_HOME/producer.py ; vi $YOUTUBE_HOME/producer.py"

alias producer_py="python $YOUTUBE_HOME/producer.py --producer=kafka --source_mode=video --videos=1,2,3,4,5 --bootstrap_servers=$HOSTNAME:6667 --max_block_ms=1000 --activity=view --tempo=1"

alias spark_test="spark-shell --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.1.0"