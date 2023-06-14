import time
import click

from pydantic import BaseModel, Field
from fabric import Connection


class TunnelPort(BaseModel):
    local: int
    remote: int


class LsofResult(BaseModel):
    command: str
    pid: int
    user: str
    fd: str
    type: str
    device: int
    size_off: str = Field(alias="size/off")
    node: str
    name: str


def lsof_port(conn, port):
    """
    **EXAMPLE**

    COMMAND  PID     USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
    sshd    8661 ecs-user    7u  IPv4 341300      0t0  TCP localhost:2222 (LISTEN)
    """
    sudo lsof -iTCP:2234 -sTCP:LISTEN
    result = conn.sudo(
        f"lsof -iTCP:{port} -sTCP:LISTEN",
        timeout=1,
        hide="both"
    )
    headers, line = [
        [part.strip() for part in line.split(maxsplit=8)]
        for line in result.stdout.splitlines()
    ]
    return LsofResult.parse_obj({k.lower(): v for k, v in zip(headers, line)})


@click.command
@click.argument("proxy-jump")
@click.argument("local-port", type=int)
@click.argument("remote-port", type=int)
@click.option("--check-interval", type=int, default=10)
def cli(proxy_jump, local_port, remote_port, check_interval):
    with Connection(proxy_jump) as conn:
        with conn.forward_remote(
            remote_port=remote_port,
            local_port=local_port,
        ):
            while True:
                proc = lsof_port(conn, remote_port)
                click.echo(f"alive! tunnel running on pid:{proc.pid}")
                time.sleep(check_interval)


if __name__ == "__main__":
    cli()
