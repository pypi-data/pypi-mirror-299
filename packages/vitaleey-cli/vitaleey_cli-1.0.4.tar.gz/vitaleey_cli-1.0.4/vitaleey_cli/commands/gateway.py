import click

from vitaleey_cli.api.gateway import Gateway
from vitaleey_cli.config import api_gateway_config


@click.group(help="API Gateway helper commands")
def group() -> click.Command:
    pass


@group.command(name="services", help="List all API Gateway resources")
@click.option("--config_path", help="Config file path")
@click.argument("environment")
def show_services(environment, config_path):
    config = api_gateway_config(environment)

    gateway = Gateway(environment, config_path or config.config_path)
    services = gateway.get_services()

    click.secho("Listing API Gateway services\n", bold=True)

    for service in services:
        click.echo(f"Service: {service['name']}")
        for key, value in service["data"]["settings"].items():
            click.echo(f"{key.title()}: {value}")
        click.echo(f"Endpoints: {len(service['data']['endpoints'])}\n")


@group.command(name="settings", help="Show API Gateway settings")
@click.argument("environment")
def show_settings(environment):
    config = api_gateway_config(environment)

    gateway = Gateway(environment, config.config_path)
    settings = gateway.get_settings()

    click.secho("Show API Gateway settings\n", bold=True)

    for key, value in settings.items():
        click.echo(f"{click.style(f"{key}: ", fg="blue")}{value}")


@group.command(name="endpoints", help="Show API Gateway endpoints")
@click.option("--service", "-s", help="Filter by service")
@click.option("--config_path", help="Config file path")
@click.argument("environment")
def show_endpoints(environment, service, config_path):
    config = api_gateway_config(environment)

    gateway = Gateway(environment, config_path or config.config_path)
    endpoints = gateway.get_endpoints()

    click.secho("Show API Gateway endpoints\n", bold=True)

    if service:
        endpoints = gateway.get_service_endpoints(service)

    for endpoint in endpoints:
        click.echo(f"* Endpoint: {endpoint.endpoint}")
        click.echo(f"  Method: {endpoint.method}")
        click.echo(f"  Extra Config: {endpoint.extra_config}")
        click.echo("  Backends:")
        for backend in endpoint.backends:
            click.echo(f"  * Service: {backend.service}")
            click.echo(f"  * URL Pattern: {backend.url_pattern}")
            click.echo(f"  * Extra Config: {backend.extra_config}\n")


@group.command()
@click.option("--config_path", help="Config file path")
@click.argument("environment")
def audit(environment, config_path):
    """
    Audit the Kraken API Gateway file
    """

    config = api_gateway_config(environment)

    click.secho("Audit the Kraken API Gateway file \n", bold=True)

    gateway = Gateway(environment, config_path or config.config_path)

    gateway.audit()


@group.command()
@click.option("--debug", is_flag=True, help="Enable debugging endpoints")
@click.option("--export", is_flag=True, help="Export the gateway file")
@click.option("--config_path", help="Config file path")
@click.argument("environment")
def run(environment, config_path, debug, export):
    """
    Run the Kraken API Gateway file
    """

    config = api_gateway_config(environment)

    click.secho("Run the Kraken API Gateway file \n", bold=True)

    click.secho(
        "By default plugins set at service level will be set at service_endpoint level if they have none\n",
        bold=True,
    )
    click.secho(
        "!IMPORTANT!: \
        \n  - Plugins set at backend level will override the plugins set at service_endpoint level \
        \n  - Plugins set at service_endpoint level will override the plugins set at service level",
        fg="yellow",
    )

    gateway = Gateway(environment, config_path or config.config_path)
    gateway.run(debug=debug, export_file=export)
