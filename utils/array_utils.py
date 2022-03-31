from typing import List


def intersection(list1: List, list2: List) -> List:
    """the intersection of two lists"""
    list3 = [value for value in list1 if value in list2]
    return list3
