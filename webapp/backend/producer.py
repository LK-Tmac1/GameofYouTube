from kafka import KafkaProducer
from utility import parse_main_arguments, pop_argument, is_path_existed, get_current_time
from source import ActivitySource
import time, sys, os


class ActivityProducer(object):
    default_produce_tempo = 1

    def __init__(self, **kwargs):
        self.produce_tempo = float(pop_argument("tempo", kwargs, ActivityProducer.default_produce_tempo))
        self.source = pop_argument("source", kwargs, None)

    def __repr__(self):
        return "%s, tempo=%s, source=%s" % (self.__class__.__name__, self.produce_tempo, self.source)

    @staticmethod
    def build_producer(**kwargs):
        source = ActivitySource.build_source(**kwargs)
        producer = pop_argument("producer", kwargs, "file")
        if producer == "file":
            return ActivityFileProducer(source=source, **kwargs)
        elif producer == "kafka":
            return ActivityKafkaProducer(source=source, **kwargs)
        return None

    def produce(self):
        if self.source is None:
            print "Not able to build an activity source by parameters provided."
            sys.exit(-1)
        while True:
            self.new_message()
            if self.produce_tempo:
                time.sleep(self.produce_tempo)


class ActivityKafkaProducer(ActivityProducer):
    def __init__(self, **kwargs):
        ActivityProducer.__init__(self, **kwargs)
        pop_config_list = list([])
        for k in kwargs:
            if k not in KafkaProducer.DEFAULT_CONFIG:
                pop_config_list.append(k)
        for k in pop_config_list:
            kwargs.pop(k)
        kwargs['max_block_ms'] = float(kwargs.get('max_block_ms', 1))
        kwargs['bootstrap_servers'] = kwargs.get('bootstrap_servers').split(",")
        self.producer = KafkaProducer(api_version=(0, 10), **kwargs)

    def new_message(self):
        message = self.source.new_activity()
        print message
        self.producer.send(topic=self.source.activity, value=message)


class ActivityFileProducer(ActivityProducer):
    def __init__(self, **kwargs):
        ActivityProducer.__init__(self, **kwargs)
        self.output_path = pop_argument("output_path", kwargs, "./test-output")
        self.write_mode = pop_argument("write_mode", kwargs, "w")
        self.output_mode = pop_argument("output_mode", kwargs, "d")

    @staticmethod
    def write_local_file(output_path, content, write_mode):
        parent_dir = output_path[0:output_path.rfind("/")]
        # If output parent dir does not exist, create it
        if not is_path_existed(parent_dir):
            os.makedirs(parent_dir)
        with open(output_path, write_mode) as output:
            output.write(content+"\n")
            output.close()

    @staticmethod
    def write_local_path(output_dir, content, file_name, write_mode):
        if output_dir[-1] != "/":
            output_dir += "/"
        output_path = output_dir + file_name
        ActivityFileProducer.write_local_file(output_path, content, write_mode)

    def new_message(self):
        message = self.source.new_activity()
        if self.output_mode == "d":
            file_name = get_current_time()
            ActivityFileProducer.write_local_path(self.output_path, message, file_name, self.write_mode)
        else:
            ActivityFileProducer.write_local_file(self.output_path, message, self.write_mode)


if __name__ == '__main__':
    config = parse_main_arguments(sys.argv)
    producer = ActivityProducer.build_producer(**config)
    producer.produce()
