#coding:utf-8

# Common functions for all gstat tests

import pytest
import re

class Helpers:
    @staticmethod
    def get_metric(data: str, table: str, metric: str) -> int:
        pattern = re.compile(f'^{table}.*\\n(^\\s+.*\\n)*?\\s+(?:[\\s\\w\\d.:]+, )*?{metric}: (\\d+\.?\\d*)', flags=re.M)
        result = pattern.search(data)
        if result:
            return float(result.group(2))
        else:
            return

    @staticmethod
    def get_full_stat(data: str, start: str) -> str:
        pattern = re.compile(f'^{start}.*\\n((^.*\\n)*)^Gstat completion', flags=re.M)
        result = pattern.search(data)
        if result:
            return result.group(1)
        else:
            return

@pytest.fixture
def gstat_helpers():
    return Helpers