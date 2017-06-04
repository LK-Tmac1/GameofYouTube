from kafka import KafkaProducer
import time

def test1():
    # need to specify the ip instead of host name kunliu1.fyre.ibm.com:6667
    broker_list = ['kunliu1.fyre.ibm.com:6667','kunliu2.fyre.ibm.com:6667','kunliu8.fyre.ibm.com:6667']
    producer = KafkaProducer(bootstrap_servers="kunliu1.fyre.ibm.com:6667", api_version=(0,10), max_block_ms=1000, ssl_password="password", sasl_plain_username="root", sasl_plain_password="password")
    for _ in range(100):
        producer.send('user-behavior-topic', 'message%s' % _)
        time.sleep(0.01)

arguments = "producer.py --producer=kafka --source_mode=video --videos=1,2,3,4,5 --bootstrap_servers=kunliu1.fyre.ibm.com:6667 --max_block_ms=1000"

test1()
print "-----Done"
