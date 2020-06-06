import argparse
import os
from jvm import TinyJVM


class Cmd:
    parser = None

    def __init__(self):
        self.parser = argparse.ArgumentParser(description='jvm parameters')
        self.parser.add_argument('-v', '-version', dest='version', action='store_true',
                                 help='print product version and exit')
        self.parser.add_argument('-cp', '-classpath', dest='classpath', action='extend', nargs='*', default=[os.getcwd()],
                                 help='<class search path of directories and zip/jar files>')
        self.parser.add_argument('-jh', '-javahome', dest='javahome', action='store', default=os.environ.get('JAVA_HOME'),
                                 help='java home path')
        self.parser.add_argument(dest='mainClass', action='store', nargs='?', default=None,
                                 help='java class to execute')
        self.parser.add_argument('-jar', dest='jar', action='store',
                                 help='jar to execute')

    def parse(self):
        args = self.parser.parse_args()
        if args.version:
            print("version 0.1.0")
        else:
            if args.mainClass is None and args.jar is None:
                print("Main Class or jar is required")
                return
            jvm = TinyJVM(args.javahome, args.classpath,
                          args.jar if args.mainClass is None else args.mainClass)
            jvm.start()
