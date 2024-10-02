from pyspark.sql import SparkSession
from py4j.java_gateway import java_import
from easy_spark.easy_spark_instance import EasySparkInstance
from easy_utils.easy_singleton import easy_singleton


@easy_singleton
class EasyHadoopInstance:
    def __init__(self, spark: SparkSession = None, must_java_import=True):
        self.spark_instance = EasySparkInstance(spark)
        self.hadoop_conf = None
        self.fs = None

        if must_java_import:
            self.import_java()

        self.configure_fs()
        pass

    def import_java(self):
        spark = self.spark_instance.spark
        java_import(spark._jvm, 'org.apache.hadoop.fs.FileSystem')
        java_import(spark._jvm, 'org.apache.hadoop.conf.Configuration')
        java_import(spark._jvm, 'org.apache.hadoop.fs.Path')

    def configure_fs(self):
        spark = self.spark_instance.spark
        self.hadoop_conf = spark._jsc.hadoopConfiguration()
        self.fs = spark._jvm.FileSystem.get(self.hadoop_conf)
