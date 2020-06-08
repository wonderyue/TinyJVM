# TinyJVM
A Java virtual machine implemented in python

# How to run

`pip install -r requirement.txt`

`python ./ your_class_path/your_class.class`

or

`python ./ -jar your_jar_path/your_jar.jar`

help:

`python ./ -h`

## help

usage: [-h] [-v] [-cp [CLASSPATH [CLASSPATH ...]]] [-jh JAVAHOME] [-jar JAR] [main_class]

positional arguments:

- main_class             java class to execute



optional arguments:

- -h, --help            show this help message and exit

- -v, -version          print product version and exit

- -cp [CLASSPATH [CLASSPATH ...]], -classpath [CLASSPATH [CLASSPATH ...]]
                          <class search path of directories and zip/jar files>, default: [current directory]

- -jh JAVAHOME, -javahome JAVAHOME
                          java home path, default: $JAVA_HOME

- -jar JAR              jar to execute

## turn on/off debug output

modify debug.py: 

`DEBUG = True`

# Feature

- [x] class loader(.class/.jar)
- [x] instructions: 160+/202
- [x] interpreter
- [x] array
- [ ] verify
- [ ] native method
- [ ] exceptions
- [ ] multithreading
- [ ] gc