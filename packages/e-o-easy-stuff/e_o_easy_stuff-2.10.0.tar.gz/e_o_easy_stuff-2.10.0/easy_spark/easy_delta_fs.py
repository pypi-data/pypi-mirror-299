from pyspark.sql import SparkSession
from datetime import datetime
from easy_spark.easy_hoop_instance import EasyHadoopInstance
from easy_spark.easy_spark_instance import EasySparkInstance


class EasyDeltaFS:
    def __init__(self, spark: SparkSession = None, path: str = None, must_java_import=False):
        self.spark_instance = EasySparkInstance(spark)
        self.easy_hadoop = EasyHadoopInstance(spark, must_java_import)
        self.file_path = None
        self.path: str = path

        if self.path and self.spark:
            self.from_path(self.path)

    @property
    def spark(self) -> SparkSession:
        return self.spark_instance.spark

    def from_path(self, path: str) -> 'EasyDeltaFS':
        self.path = path
        self.file_path = self.spark._jvm.Path(self.path)
        return self

    def file_exists(self) -> bool:
        return self.easy_hadoop.fs.exists(self.file_path)

    def get_file_status(self):
        return self.easy_hadoop.fs.getFileStatus(self.file_path)

    def get_modified_time(self):
        return self.get_file_status().getModificationTime()

    def get_readable_modified_time(self) -> datetime:
        modified_time = self.get_modified_time()
        return datetime.fromtimestamp(modified_time / 1000.0)

    def delete_file(self) -> bool:
        return self.easy_hadoop.fs.delete(self.file_path, True)

    def write_file_content(self, content: any, delete_if_exists: bool = False) -> bool:

        if delete_if_exists:
            if self.file_exists():
                self.delete_file()
        elif self.file_exists():
            return False

        output_stream = self.easy_hadoop.fs.create(self.file_path)
        try:
            output_stream.write(content)
        finally:
            output_stream.close()

        return True
