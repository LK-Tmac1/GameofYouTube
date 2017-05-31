import subprocess, os


class Service(object):
    cwd = os.path.dirname(os.path.realpath(__file__))

    def __init__(self, program_path=None, **kwargs):
        self.service_name = self.__class__.__name__
        self.PID = None
        self.cmd_list = list([])
        self.program_path = program_path
        for p in program_path.split():
            self.cmd_list.append(p)
        for k, v in kwargs.items():
            self.cmd_list.append("--%s=%s" % (k, v))

    def __repr__(self):
        return "%s Program path=%s PID=%s CWD=%s" % (self.service_name, self.program_path, self.PID, Service.cwd)

    def add_argument_pair(self, **kwargs):
        for k, v in kwargs.items():
            self.add_argument("--%s=%s" % (k, v))

    def add_argument(self, v):
        self.cmd_list.append(str(v))

    def start(self):
        if not self.PID:
            self.PID = subprocess.Popen(self.cmd_list, shell=False, cwd=self.cwd).pid
        return self.PID

    def stop(self):
        return self.PID


class ProducerService(Service):
    def __init__(self, **kwargs):
        Service.__init__(self, program_path="python ./producer.py", **kwargs)
        pass


class SparkService(Service):
    def __init__(self, **kwargs):
        Service.__init__(self, program_path="spark-submit", **kwargs)
        pass
