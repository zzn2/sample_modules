import subprocess
import sys


def run(command: list, timeout=60000):
    if not command:
        return

    return subprocess.Popen(command, stdout=sys.stdout, stderr=sys.stderr).wait(timeout=timeout)


INVOKER_VERSION = '0.0.6'


def is_invoking_official_module(args):
    return len(args) >= 3 and args[0] == 'python' and args[1] == '-m' and args[2].startswith('azureml.studio.')


def generate_run_command(args):
    return [arg for arg in args]


def execute(args):
    is_custom_module = not is_invoking_official_module(args)
    module_type = 'custom module' if is_custom_module else 'official module'
    print('Invoking {} by invoker {}.'.format(module_type, INVOKER_VERSION))

    ret = run(generate_run_command(args))

    # set the subprocess run result as exit value
    exit(ret)


if __name__ == '__main__':
    args = sys.argv[1:]
    execute(args)
