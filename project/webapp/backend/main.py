from producer import ActivityProducer
from utility import parse_main_arguments
import sys


def test():
    sys.argv.append("--config_path=")
    sys.argv.append("--channelId=kun")
    sys.argv.append("--mode=channel_video")
    sys.argv.append("--videos=1,2,3,4,5")
    sys.argv.append("--activity=like")
    # arguments.append("--tempo=0.01")
    config = parse_main_arguments(sys.argv)
    producer = ActivityProducer.build_producer(config=config)
    producer.produce()


if __name__ == '__main__':
    config = parse_main_arguments(sys.argv)
    producer = ActivityProducer.build_producer(config=config)
    producer.produce()
