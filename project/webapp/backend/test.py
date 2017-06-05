from kafka import KafkaProducer
import time

def test1():
    # need to specify the ip instead of host name kunliu1.fyre.ibm.com:6667
    broker_list = ['kunliu1.fyre.ibm.com:6667','kunliu2.fyre.ibm.com:6667','kunliu8.fyre.ibm.com:6667']
    producer = KafkaProducer(bootstrap_servers="kunliu1.fyre.ibm.com:6667", api_version=(0,10), max_block_ms=1000)
    for _ in range(100):
        producer.send('video', 'message100')
        time.sleep(0.01)

arguments = "producer.py --producer=kafka --source_mode=video --videos=1,2,3,4,5 --bootstrap_servers=kunliu1.fyre.ibm.com:6667 --max_block_ms=1000"

test1()
print "-----Done"
