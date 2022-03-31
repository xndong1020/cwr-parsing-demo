from inspect import getmembers, isfunction
from pprint import pprint
from cwr_parser.pack.models import Nwr
import field_validators.nwr_field_validators as nwr_validators
from config.validations_control import field_level_Validations


def nwr_processor(record):
    nwr = Nwr(record["record_prefix"])
    for k, v in record.items():
        setattr(nwr, k, v)

    # pprint(nwr.asdict())

    # to disable/enable validation rules by reading the settings from configuration
    validators = [
        validator
        for validator in getmembers(nwr_validators, isfunction)
        if field_level_Validations[validator[0]]
    ]

    # field level validations
    field_errors = []
    field_errors = list(
        filter(
            lambda x: x != None,
            [validator[1](nwr) for validator in validators],
        )
    )

    return {
        f"transaction_sequence_number-{nwr.transaction_sequence_number}-NWR": field_errors
    }
