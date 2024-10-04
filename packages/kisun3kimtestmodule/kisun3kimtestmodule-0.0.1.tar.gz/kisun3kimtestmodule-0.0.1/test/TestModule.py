"""모듈을 테스트하기 위한 파일

This file is for testing the module.

Requirements:
    - pyspark
    - arrow

Example:
        $ python TestModule.py
"""
import sys
sys.path.append("../src")
sys.path.append("./src")

from pyspark.sql import SparkSession
from pyspark.sql import Row
from datetime import datetime, date
import MyLogging
import TagFilePath

def test_logging_func():
    """기본적인 실행 및 로그 모듈 테스트를 위한 함수"""
    #print("test_func")
    mylogger.stream().info('test log')
    mylogger.file().debug('test debug log..')

def test_spark_dataframe():
    """기본적인 Spark(pySpark) 테스트를 위한 함수"""
    spark = SparkSession.builder.appName("Testing PySpark Example").getOrCreate()
    df = spark.createDataFrame([
        Row(a=1, b=2., c='string1', d=date(2000, 1, 1), e=datetime(2000, 1, 1, 12, 0)),
        Row(a=2, b=3., c='string2', d=date(2000, 2, 1), e=datetime(2000, 1, 2, 12, 0)),
        Row(a=4, b=5., c='string3', d=date(2000, 3, 1), e=datetime(2000, 1, 3, 12, 0))
    ])
    print(df)
    spark.stop()

def test_tag_file_path():
    """태그 파일 경로 모듈 테스트를 위한 함수"""
    # input
    plant_name = 'hanam'
    tag_name = '11gtspeed'
    tag_sensor_name = 'HN.GTC.11RCAOG-D001_01'
    hdfs_path = 'hdfs://10.224.81.60:8020'
    base_path = f'/data0/plants/{plant_name}/'      # hdfs - data data0 
    file_extention = 'txt.gz'

    tag_file_path = TagFilePath.TagFilePath(plant_name, hdfs_path, base_path, tag_name, tag_sensor_name, file_extention)
    print(tag_file_path.get_file_path_from_date('2024-10-01'))
    print(tag_file_path.get_file_list_from_date_range('2021-01-01', '2021-01-03'))

# 로그 모듈 설정
mylogger = MyLogging.MyLogging('TestModule.log')
mylogger.check_configurations()
#print(mylogger.get_filename())

# 실행 및 로깅 테스트 함수 호출
test_logging_func()

# 태그 파일 경로 모듈 테스트
test_tag_file_path()
