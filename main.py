import logging
import botocore.config
import boto3

import typer
import urllib.parse

logging.basicConfig(format="[%(levelname)s] %(message)s", level=logging.WARNING)

app = typer.Typer(
    name="presign",
    help="Presign AWS requests.",
    context_settings={"help_option_names": ["-h", "--help"]},
    pretty_exceptions_enable=False,
)


@app.command(
    context_settings={
        "allow_extra_args": True,
        "ignore_unknown_options": True
    },
)
def presign(
        ctx: typer.Context,
        service: str = typer.Argument(..., help="AWS service to presign."),
        action: str = typer.Argument(..., help="AWS CLI action to presign."),
        profile: str = typer.Option(None),
        method: str = typer.Option('GET'),
        no_encoding: bool = typer.Option(False),
        endpoint: str = typer.Option(None),
        version: str = typer.Option('v4'),
):
    """Create pre-signed URL for the given service and action."""
    action = action.replace('-', '_')
    params = list_to_dict(ctx.args)
    params = {k.lstrip('--'): v for k, v in params.items()}

    sess: boto3.Session = boto3.Session(profile_name=profile)
    config = botocore.config.Config(
        signature_version=version,
    )
    client = sess.client(
        service,
        config=config,
        endpoint_url=endpoint,
    )

    resp = client.generate_presigned_url(action, Params=params, HttpMethod=method)

    if no_encoding:
        print(urllib.parse.unquote(resp))
    else:
        print(resp)


def list_to_dict(a):
    it = iter(a)
    res_dct = dict(zip(it, it))
    return res_dct


if __name__ == "__main__":
    app()
