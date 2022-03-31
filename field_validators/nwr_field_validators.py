from cwr_parser.pack.models import Error, Nwr
from constants import language_code_table


def work_title_is_required(obj: Nwr) -> Error:
    """
    1. Work Title must be entered. (TR)
    """
    print("work_title", obj.work_title)
    if not obj.work_title:
        return Error("work_title is missing.", "TR")


"""
Revised in Version 1.2
"""


def language_code_must_exist_if_entered(obj: Nwr) -> Error:
    """
    2. Language Code, if entered, must match an entry in the Language Code Table. (TR)
    """
    if obj.language_code not in language_code_table.keys():
        return Error(
            f"{obj.language_code} does not exist in the Language Code Table.", "TR"
        )
