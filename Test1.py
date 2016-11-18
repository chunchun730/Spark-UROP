from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
import time
from datetime import datetime

conf = SparkConf().setAppName("Use pre-aggregated data").setMaster("local").set("spark.eventLog.enabled", "true")
sc = SparkContext(conf=conf)

global files
global mapping

mapping = {}
files = sc.textFile("/home/chunchun/Documents/ICEWS/preagg/*.csv")


def print_f(line):
    print line


def sum_events(fromdate=None, todate=None):
    """
    Use spark to run through tab files and return sum_events.
    Input:
    fromadte: YYYYMM OR YYYY
    todate: YYYYMM OR YYYY

    Output:
    mapping: dictionary
            {(source country, to country, CAMEO code): sum of events}}
    """
    t0 = time.time()
    start_date = datetime.strptime(fromdate, "%Y-%m")
    end_date = datetime.strptime(todate, "%Y-%m")

    def read_line(line):
        row = line.split(",")
        if time_range(row[0]):
            return (tuple(row[:-1]), row[-1])
        return ("None", 0)

    def time_range(date):
        try:
            date = datetime.strptime(date, "%Y-%m")
            return start_date <= date <= end_date
        except Exception:
            return False

    extracted_files = files.map(read_line).coalesce(8)
    mapping = extracted_files.collectAsMap()

    t1 = time.time()

    #print mapping
    print "finished in ",t1-t0,' seconds.'
    #Event ID   Event Date  Source Name Source Sectors  Source Country  Event Text  CAMEO Code  Intensity   Target Name Target Sectors  Target Country  Story ID    Sentence Number Publisher   City    District    Province    Country Latitude    Longitude

sum_events("1995-01", "2013-01")

