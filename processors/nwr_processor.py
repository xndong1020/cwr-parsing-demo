from inspect import getmembers, isfunction
from pprint import pprint
from cwr_parser.pack.models import Nwr
import field_validators.nwr_field_validators as nwr_validators


def nwr_processor(record):
    nwr = Nwr(record["record_prefix"])
    for k, v in record.items():
        setattr(nwr, k, v)

    # pprint(nwr.asdict())

    # field level validations
    field_errors = []
    field_errors = list(
        filter(
            lambda x: x != None,
            [validator[1](nwr) for validator in getmembers(nwr_validators, isfunction)],
        )
    )

    return {
        f"transaction_sequence_number-{nwr.transaction_sequence_number}-NWR": field_errors
    }
