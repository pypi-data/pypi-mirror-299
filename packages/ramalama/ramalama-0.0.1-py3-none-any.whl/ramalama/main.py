import argcomplete
import os
import errno
import subprocess
import sys
from ramalama.cli import init_cli, run_container, version
from ramalama.common import perror

def main_cli():
    sharedirs = ["/opt/homebrew/share/ramalama", "/usr/local/share/ramalama", "/usr/share/ramalama"]
    syspath = next((d for d in sharedirs if os.path.exists(d)), None)
    sys.path.insert(0, syspath)

    import ramalama

    parser, args = init_cli()
    argcomplete.autocomplete(parser)

    if args.version:
        return version(args)

    if run_container(args):
        return

    # Process CLI
    try:
        args.func(args)
    except HelpException:
        parser.print_help()
    except AttributeError:
        parser.print_usage()
        print("ramalama: requires a subcommand")
    except IndexError as e:
        perror("Error: " + str(e).strip("'"))
        sys.exit(errno.EINVAL)
    except KeyError as e:
        perror("Error: " + str(e).strip("'"))
        sys.exit(1)
    except NotImplementedError as e:
        perror("Error: " + str(e).strip("'"))
        sys.exit(errno.ENOTSUP)
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)
