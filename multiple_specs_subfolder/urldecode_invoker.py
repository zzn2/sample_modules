import sys
from urllib import parse

from invoker import execute


INVOKER_VERSION = '0.0.1'


if __name__ == '__main__':
    args = sys.argv[1:]
    print(f"Invoking module by urldecode_invoker {INVOKER_VERSION}.")
    print("")

    decoded_args = [parse.unquote_plus(arg) for arg in args]
    print(f"args: ({len(args)} items)")
    print("-" * 20)
    for arg, decoded_arg in zip(args, decoded_args):
        print(f"{arg}  =>  {decoded_arg}")
    print("-" * 20)

    execute(decoded_args)
