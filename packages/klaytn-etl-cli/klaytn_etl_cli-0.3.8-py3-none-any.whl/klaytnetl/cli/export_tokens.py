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


import click

from web3 import Web3
from web3.middleware import geth_poa_middleware

from blockchainetl.file_utils import smart_open
from klaytnetl.jobs.export_tokens_job import ExportTokensJob
from klaytnetl.jobs.exporters.tokens_item_exporter import tokens_item_exporter
from blockchainetl.logging_utils import logging_basic_config
from klaytnetl.thread_local_proxy import ThreadLocalProxy
from klaytnetl.utils import return_provider
from klaytnetl.providers.auto import get_provider_from_uri

logging_basic_config()


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option(
    "-t",
    "--token-addresses",
    required=True,
    type=str,
    help="The file containing token addresses, one per line.",
)
@click.option(
    "-o",
    "--output",
    default="-",
    type=str,
    help="The output file. If not specified stdout is used.",
)
@click.option(
    "-w",
    "--max-workers",
    default=5,
    show_default=True,
    type=int,
    help="The maximum number of workers.",
)
@click.option(
    "-p",
    "--provider-uri",
    default="https://cypress.fandom.finance/archive",
    show_default=True,
    type=str,
    help="The URI of the web3 provider e.g. "
    "file://$HOME/var/kend/data/klay.ipc or https://cypress.fandom.finance/archive",
)
@click.option(
    "--network",
    default=None,
    type=str,
    help="Input either baobab or cypress to obtain public provider"
    "If not provided, the option will be disabled.",
)
def export_tokens(token_addresses, output, max_workers, provider_uri, network):
    """Exports ERC20/ERC721/ERC1155 tokens."""
    if network:
        provider_uri = return_provider(network)

    web3 = Web3(get_provider_from_uri(provider_uri))
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)

    with smart_open(token_addresses, "r") as token_addresses_file:
        job = ExportTokensJob(
            token_addresses_iterable=(
                token_address.strip() for token_address in token_addresses_file
            ),
            web3=ThreadLocalProxy(lambda: web3),
            item_exporter=tokens_item_exporter(output),
            max_workers=max_workers,
        )

        job.run()
