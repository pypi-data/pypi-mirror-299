"""Implementation for 'client' command"""

from argparse import _SubParsersAction
from .config import get_target_config, to_omada_connection
from .util import get_client_mac, get_target_argument


async def command_reconnect_client(args) -> int:
    """Executes 'reconnect-client' command"""
    controller = get_target_argument(args)
    config = get_target_config(controller)

    async with to_omada_connection(config) as client:
        site_client = await client.get_site_client(config.site)
        mac = await get_client_mac(site_client, args["mac"])
        await site_client.reconnect_client(mac)
    return 0


def arg_parser(subparsers: _SubParsersAction) -> None:
    """Configures arguments parser for 'reconnect-client' command"""
    reconnect_parser = subparsers.add_parser("reconnect-client", help="Reconnects a client")

    reconnect_parser.add_argument(
        "mac",
        help="The MAC address or name of the client",
    )

    reconnect_parser.set_defaults(func=command_reconnect_client)
