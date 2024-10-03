# STDLIB
import sys


# main{{{
def main() -> None:
    """
    the main method, it does nothing at all

    >>> main()

    """
    # main}}}
    pass


if __name__ == "__main__":
    print(b'this is a library only, the executable is named "security_dependency_pinning_cli.py"', file=sys.stderr)
