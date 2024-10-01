import argparse
import sys
import os

from netrc import netrc
from urllib.parse import urlparse

from . import AUTHENTICATION_URL


def env_credentials():
    creds = {}
    if "ETNA_USER" in os.environ:
        creds["username"] = os.environ["ETNA_USER"]
    if "ETNA_PASSWORD" in os.environ:
        creds["password"] = os.environ["ETNA_PASSWORD"]
    return creds


def netrc_credentials():
    creds = None
    try:
        url = urlparse(AUTHENTICATION_URL)
        creds = netrc().authenticators(url.netloc)
    except FileNotFoundError:
        pass
    if creds:
        return dict(username=creds[0], password=creds[2])
    else:
        return {}


def credentials():
    creds = netrc_credentials()
    creds.update(env_credentials())
    if creds.get("username") and creds.get("password"):
        return creds
    return None


class CommandLineHandler:
    def setup_subparsers(self, parser):
        subparsers = parser.add_subparsers(title="actions")
        commands = list(name[8:] for name in dir(self) if name.startswith("command_"))
        for name in commands:
            handler = getattr(self, "command_" + name)
            options = getattr(self, "options_for_" + name, None)
            aliases = getattr(self, "aliases_for_" + name, [])
            p = subparsers.add_parser(name, aliases=aliases, help=handler.__doc__)
            if callable(options):
                options(p)
            if isinstance(handler, CommandLineHandler):
                handler.setup_subparsers(p)
            elif callable(handler):
                p.set_defaults(handler=handler)
            else:
                raise ValueError(
                    f"type mismatch for {self.__class__.__name__}.command_{name}: "
                    f"should be callable or instance of CommandLineHandler"
                )

    def common_options(self, p):
        pass

    def run(self):
        parser = argparse.ArgumentParser(description=self.__doc__)
        parser.set_defaults(handler=None)
        self.common_options(parser)
        self.setup_subparsers(parser)
        opts = parser.parse_args()
        if opts.handler is None:
            parser.print_usage()
            sys.exit(1)
        return self.dispatch(opts.handler, opts)

    def dispatch(self, handler, opts):
        "Override this if you want to pass extra args to handlers or do exception handling, etc..."
        return handler(opts)
