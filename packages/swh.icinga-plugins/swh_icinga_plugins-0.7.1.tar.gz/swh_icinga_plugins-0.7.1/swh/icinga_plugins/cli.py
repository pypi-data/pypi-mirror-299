# Copyright (C) 2019-2022  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

# WARNING: do not import unnecessary things here to keep cli startup time under
# control
import sys

import click

from swh.core.cli import CONTEXT_SETTINGS
from swh.core.cli import swh as swh_cli_group


@swh_cli_group.group(name="icinga_plugins", context_settings=CONTEXT_SETTINGS)
@click.option("-w", "--warning", type=int, help="Warning threshold.")
@click.option("-c", "--critical", type=int, help="Critical threshold.")
@click.option("--prometheus-exporter/--no-prometheus-exporter", default=False)
@click.option(
    "--prometheus-exporter-directory",
    type=str,
    default="/var/lib/prometheus/node-exporter",
)
@click.option("--environment", type=str, help="The tested environment")
@click.pass_context
def icinga_cli_group(
    ctx,
    warning,
    critical,
    prometheus_exporter: bool,
    prometheus_exporter_directory: str,
    environment: str,
):
    """Main command for Icinga plugins"""
    ctx.ensure_object(dict)
    if warning:
        ctx.obj["warning_threshold"] = int(warning)
    if critical:
        ctx.obj["critical_threshold"] = int(critical)

    ctx.obj["prometheus_enabled"] = prometheus_exporter
    ctx.obj["prometheus_exporter_directory"] = prometheus_exporter_directory
    ctx.obj["environment"] = environment


@icinga_cli_group.group(name="check-vault")
@click.option(
    "--swh-storage-url", type=str, required=True, help="URL to an swh-storage HTTP API"
)
@click.option(
    "--swh-web-url", type=str, required=True, help="URL to an swh-web instance"
)
@click.option(
    "--poll-interval",
    type=int,
    default=10,
    help="Interval (in seconds) between two polls to the API, "
    "to check for cooking status.",
)
@click.pass_context
def check_vault(ctx, **kwargs):
    ctx.obj.update(kwargs)


@check_vault.command(name="directory")
@click.pass_context
def check_vault_directory(ctx):
    """Picks a random directory, requests its cooking via swh-web,
    and waits for completion."""
    from .vault import VaultCheck

    sys.exit(VaultCheck(ctx.obj).main())


@icinga_cli_group.group(name="check-savecodenow")
@click.option(
    "--swh-web-url", type=str, required=True, help="URL to an swh-web instance"
)
@click.option(
    "--poll-interval",
    type=int,
    default=10,
    help="Interval (in seconds) between two polls to the API, "
    "to check for save code now status.",
)
@click.pass_context
def check_scn(ctx, **kwargs):
    ctx.obj.update(kwargs)


@check_scn.command(name="origin")
@click.argument("origin", type=str, nargs=-1)
@click.option("--visit-type", type=str, required=True, help="Visit type for origin")
@click.pass_context
def check_scn_origin(ctx, origin, visit_type):
    """Requests a save code now via the api for a given origin with type visit_type, waits
    for its completion, report approximate time of completion (failed or succeeded) and
    warn if threshold exceeded.

    """
    from .save_code_now import SaveCodeNowCheck

    sys.exit(SaveCodeNowCheck(ctx.obj, list(origin), visit_type).main())


@icinga_cli_group.group(name="check-deposit")
@click.option(
    "--server",
    type=str,
    default="https://deposit.softwareheritage.org/1",
    help="URL to the SWORD server to test",
)
@click.option(
    "--provider-url",
    type=str,
    required=True,
    help=(
        "Root URL of the deposit client, as defined in the "
        "'deposit_client.provider_url' column in the deposit DB"
    ),
)
@click.option("--username", type=str, required=True, help="Login for the SWORD server")
@click.option(
    "--password", type=str, required=True, help="Password for the SWORD server"
)
@click.option(
    "--collection",
    type=str,
    required=True,
    help="Software collection to use on the SWORD server",
)
@click.option(
    "--poll-interval",
    type=int,
    default=10,
    help="Interval (in seconds) between two polls to the API, "
    "to check for ingestion status.",
)
@click.option(
    "--swh-web-url", type=str, required=True, help="URL to an swh-web instance"
)
@click.pass_context
def check_deposit(ctx, **kwargs):
    ctx.obj.update(kwargs)


@check_deposit.command(name="single")
@click.option(
    "--archive", type=click.Path(), required=True, help="Software artefact to upload"
)
@click.option(
    "--metadata",
    type=click.Path(),
    required=True,
    help="Metadata file for the software artefact.",
)
@click.pass_context
def check_deposit_single(ctx, **kwargs):
    """Checks the provided archive and metadata file and be deposited."""
    from .deposit import DepositCheck

    ctx.obj.update(kwargs)
    sys.exit(DepositCheck(ctx.obj).main())
