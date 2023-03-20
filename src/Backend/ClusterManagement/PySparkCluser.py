import findspark  
import os
import subprocess 
findspark.init('C:\Spark\spark-3.3.1-bin-hadoop3')

from pyspark import SparkConf  
from pyspark import SparkContext 

#Need to check if Java/Hadoop/Spark are installed properly

class ClusterManagement():

    def __init__(self, cpu, mem, masterURL):
        self.cpu = cpu
        self.mem = mem
        self.masterURL = masterURL

    def start_pyspark(self):
        x = os.system("cmd pyspark")
        print(x)

    def start_master(self):
      os.system('cmd cd %SPARK_HOME% && bin\spark-class2.cmd org.apache.spark.deploy.master.Master')


    def start_workers(self):
        if self.cpu is None or self.mem is None or self.masterURL is None:
            raise ValueError("To Start a Spark Worker Please Set the CPU, memory, and the location of the master node")

        command = f"cmd cd %SPARK_HOME% && bin\spark-class2.cmd org.apache.spark.deploy.worker.Worker -c {str(self.cpu)} -m {str(self.mem)}G {self.masterURL}"
        os.system(command)

if __name__ == '__main__':
    cpu = 1 
    mem = 1 
    masterUrl = 'spark://192.168.0.164:7077'
    x = ClusterManagement(cpu, mem, masterUrl).start_pyspark().start_master().start_workers()
