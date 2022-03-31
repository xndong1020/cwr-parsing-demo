import json
from cwr_parser.pack.generator import json_generator
import cwr_parser.pack.models as models
from processors.nwr_processor import nwr_processor


json_generator("cw210020ccp_008_short.v21")


def record_parser(record) -> models.EntityBase:
    record_type = record["record_type"]
    # print("record_type", record_type)
    if record_type == "NWR":
        return nwr_processor(record)


with open("json_data.json") as json_file:
    data = json.load(json_file)
    for record in data:
        obj = record_parser(record)
