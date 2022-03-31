import json
from typing import Optional
import pandas as pd
from cwr_parser.pack.models import Error
import utils.array_utils as utils

"""
    4.5.5. Transaction Level Validation
"""


def record_type_must_be_valid(transaction_rows: list) -> Optional[Error]:
    """
    1. Only one NWR or REV or ISW or EXC is allowed per transaction. (TR)
    """
    # print(json.dumps(transaction_rows, indent=2))

    transaction_rows_pd = pd.DataFrame(transaction_rows)
    record_type = list(transaction_rows_pd["record_type"].unique())
    common = utils.intersection(["NWR", "REV", "ISW", "EXC"], record_type)
    if len(common) > 1:
        return Error(
            "Only one NWR or REV or ISW or EXC is allowed per transaction.", "TR"
        )


def ins_should_present_if_musical_work_distribution_is_ser(
    transaction_rows: list,
) -> Optional[Error]:
    """
    3. If Musical Work Distribution Category is equal to "SER", the transaction must include an INS (Instrumentation Summary) record. (TR)
    """

    transaction_rows_pd = pd.DataFrame(transaction_rows)
    target_row = transaction_rows_pd[
        (transaction_rows_pd["record_type"] == "NWR")
        | (transaction_rows_pd["record_type"] == "REV")
    ]
    ins_row = transaction_rows_pd[(transaction_rows_pd["record_type"] == "INS")]
    musical_work_distribution = target_row["musical_work_distribution"]

    if musical_work_distribution.unique() == ["SEG"] and ins_row.empty:
        return Error(
            "the transaction must include an INS if the musical_work_distribution is SER.",
            "TR",
        )


def pr_shares_must_be_valid(transaction_rows: list) -> Optional[Error]:
    """
    4a. Total Ownership shares across all SPU and OPU records must be less than or equal to 05000 (50%) for PR
    Shares and must be less than or equal to 10000 (100%) for MR Shares and SR Shares. Note that a
    tolerance of plus or minus 00006 (.06%) is allowed. (TR)
    """
    transaction_rows_pd = pd.DataFrame(transaction_rows)
    target_row = transaction_rows_pd[
        (transaction_rows_pd["record_type"] == "SPU")
        | (transaction_rows_pd["record_type"] == "OPU")
    ]
    pr_shares_sum = target_row["pr_ownership_share"].sum() / 100 / 100

    print("pr_shares_sum", pr_shares_sum)

    if pr_shares_sum >= 0.5 + 0.0006:
        return Error(
            f"Total Ownership shares across all SPU and OPU records must be less than or equal to 50% for PR Shares",
            "TR",
        )


def mr_shares_must_be_valid(transaction_rows: list) -> Optional[Error]:
    """
    4b. Total Ownership shares across all SPU and OPU records must be less than or equal to 05000 (50%) for PR
    Shares and must be less than or equal to 10000 (100%) for MR Shares and SR Shares. Note that a
    tolerance of plus or minus 00006 (.06%) is allowed. (TR)
    """
    transaction_rows_pd = pd.DataFrame(transaction_rows)
    target_row = transaction_rows_pd[
        (transaction_rows_pd["record_type"] == "SPU")
        | (transaction_rows_pd["record_type"] == "OPU")
    ]
    mr_shares_sum = target_row["mr_ownership_share"].sum() / 100 / 100

    if mr_shares_sum >= 1 + 0.0006:
        return Error(
            f"Total Ownership shares across all SPU and OPU records must be less than or equal to 100% for MR Shares",
            "TR",
        )


def sr_shares_must_be_valid(transaction_rows: list) -> Optional[Error]:
    """
    4c. Total Ownership shares across all SPU and OPU records must be less than or equal to 05000 (50%) for PR
    Shares and must be less than or equal to 10000 (100%) for MR Shares and SR Shares. Note that a
    tolerance of plus or minus 00006 (.06%) is allowed. (TR)
    """
    transaction_rows_pd = pd.DataFrame(transaction_rows)
    target_row = transaction_rows_pd[
        (transaction_rows_pd["record_type"] == "SPU")
        | (transaction_rows_pd["record_type"] == "OPU")
    ]
    sr_shares_sum = target_row["sr_ownership_share"].sum() / 100 / 100

    if sr_shares_sum >= 1 + 0.0006:
        return Error(
            f"Total Ownership shares across all SPU and OPU records must be less than or equal to 100% for SR Shares",
            "TR",
        )
