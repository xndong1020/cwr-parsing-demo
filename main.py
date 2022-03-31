from inspect import getmembers, isfunction
import json
import os
from app import record_parser
import luigi
from luigi import Task, LocalTarget
from cwr_parser.pack.generator import json_generator
import transaction_validators.nwr_transaction_validators as nwr_transaction_validators


class DownloadParsedJson(Task):
    def output(self):
        return LocalTarget("data.json")

    def run(self):
        json_generator("cw210020ccp_008_short.v21")
        with open("json_data.json") as file:
            lines = file.readlines()
            for line in lines:
                with self.output().open("w") as f:
                    f.write(line)


class ValidateJsonFile(Task):
    def requires(self):
        return DownloadParsedJson()

    def output(self):
        return LocalTarget("errors.json")

    def run(self):
        with self.input().open() as json_file:
            data = json.load(json_file)

            transaction_errors = []
            transaction_errors = list(
                filter(
                    lambda x: x != None,
                    [
                        validator[1](data)
                        for validator in getmembers(
                            nwr_transaction_validators, isfunction
                        )
                    ],
                )
            )
            transaction_sequence_number = data[0]["transaction_sequence_number"]
            print(
                "transaction_errors",
                {
                    f"transaction_sequence_number-{transaction_sequence_number}": [
                        item.toJson() for item in transaction_errors
                    ]
                },
            )
            all_fields_errors = []
            for record in data:
                fields_errors = record_parser(record)
                print("fields_errors", fields_errors)
                if fields_errors is not None:
                    all_fields_errors = fields_errors

            with self.output().open("w") as f:
                for k, v in all_fields_errors.items():
                    for err in v:
                        print(err.toJson())
                        f.write(err.toJson())


if __name__ == "__main__":
    luigi.run(["ValidateJsonFile"])
