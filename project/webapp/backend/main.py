from producer import ActivityProducer
from utility import parse_main_arguments
import sys


if __name__ == '__main__':
    arguments = sys.argv
    arguments.append("--config_path=")
    arguments.append("--channelId=kun")
    arguments.append("--mode=channel_video")
    arguments.append("--videos=1,2,3,4,5")
    arguments.append("--activity=like")
    # arguments.append("--tempo=0.01")
    config = parse_main_arguments(sys.argv)
    producer = ActivityProducer.build_producer(config=config)
    producer.produce()
