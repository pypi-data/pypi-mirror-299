# MIT License
#
# Modifications Copyright (c) klaytn authors
# Copyright (c) 2018 Evgeny Medvedev, evge.medvedev@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import pytest

import tests.resources
from klaytnetl.web3_utils import build_web3
from klaytnetl.jobs.export_contracts_job import ExportContractsJob
from klaytnetl.jobs.exporters.contracts_item_exporter import contracts_item_exporter
from klaytnetl.thread_local_proxy import ThreadLocalProxy
from tests.klaytnetl.job.helpers import get_web3_provider
from tests.helpers import (
    compare_lines_ignore_order,
    read_file,
    skip_if_slow_tests_disabled,
)

RESOURCE_GROUP = "test_export_contracts_job"


def read_resource(resource_group, file_name):
    return tests.resources.read_resource([RESOURCE_GROUP, resource_group], file_name)


ERC721_CONTRACT_ADDRESSES_UNDER_TEST = [
    {
        "contract_address": "0x29032e52f4d83661b4f51f90034d4411cea890f7",
        "block_number": 84412451,
    },
]

ERC1155_CONTRACT_ADDRESSES_UNDER_TEST = [
    {
        "contract_address": "0x4e16e2567dd332d4c44474f8b8d3130b5c311cf7",
        "block_number": 81331002,
    },
]


@pytest.mark.parametrize(
    "batch_size,contract_addresses,output_format,resource_group,web3_provider_type",
    [
        skip_if_slow_tests_disabled(
            (1, ERC721_CONTRACT_ADDRESSES_UNDER_TEST, "json", "erc721_contract", "fantrie")
        ),
        skip_if_slow_tests_disabled(
            (1, ERC1155_CONTRACT_ADDRESSES_UNDER_TEST, "json", "erc1155_contract", "fantrie")
        ),
    ],
)
def test_export_contracts_job(
    tmpdir,
    batch_size,
    contract_addresses,
    output_format,
    resource_group,
    web3_provider_type,
):
    contracts_output_file = str(tmpdir.join("actual_contracts." + output_format))

    job = ExportContractsJob(
        contracts_iterable=contract_addresses,
        batch_size=batch_size,
        batch_web3_provider=ThreadLocalProxy(
            lambda: get_web3_provider(
                web3_provider_type,
                lambda file: read_resource(resource_group, file),
                batch=True,
            )
        ),
        web3=ThreadLocalProxy(
            lambda: build_web3(
                get_web3_provider(
                    web3_provider_type, lambda file: read_resource(resource_group, file)
                )
            )
        ),
        max_workers=5,
        item_exporter=contracts_item_exporter(contracts_output_file),
    )
    job.run()

    compare_lines_ignore_order(
        read_resource(resource_group, "expected_contracts." + output_format),
        read_file(contracts_output_file),
    )
