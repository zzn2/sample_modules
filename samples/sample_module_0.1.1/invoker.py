import shlex
import subprocess
import sys
import re
import json
import os


def run(command: str, timeout=60000):
    if not command:
        return

    print("\n$ {}".format(command))
    return subprocess.Popen(shlex.split(command), stdout=sys.stdout, stderr=sys.stderr).wait(timeout=timeout)


INITIAL_COMMANDS = '''
pwd
'''.splitlines()

INVOKER_VERSION = '0.0.1'


def is_invoking_official_module(args):
    return len(args) >= 3 and args[0] == 'python' and args[1] == '-m' and args[2].startswith('azureml.studio.')


def first_or_none(iterable):
    try:
        return next(iterable)
    except StopIteration:
        return None


def remove_prefix(text, prefix=None):
    if not text or not prefix:
        return text

    if not text.startswith(prefix):
        return text

    return text[len(prefix):]


class CommandJsonParser:
    def __init__(self, path):
        try:
            with open(path) as f:
                self._dct = json.load(f)
        except Exception:
            self._dct = {}

    @property
    def module_statistics_folder(self):
        return self._dct.get('ModuleStatisticsFolder', None)


def save_custom_module_run_statistics(command_json_arg, is_run_succeed):
    path = remove_prefix(command_json_arg, prefix='--command-file=')
    parser = CommandJsonParser(path)
    output_path = parser.module_statistics_folder

    if not output_path:
        print("Warning: no valid path to write module run statistics.")
        return

    os.makedirs(output_path, exist_ok=True)

    error_info = {
        'ErrorId': 'CustomModuleRuntimeError',
        'ErrorCode': 1001,
        'ExceptionType': 'ModuleException',
        'Message': 'Failed while invoking custom module. Refer to error outputs for details.'
    } if not is_run_succeed else None

    try:
        with open(os.path.join(output_path, 'error_info.json'), 'w') as f:
            json.dump({'Exception': error_info}, f)
    except Exception as e:
        print("Error occurred while writing module run statistics: {}".format(e))


def execute(args):
    is_custom_module = not is_invoking_official_module(args)
    module_type = 'custom module' if is_custom_module else 'official module'
    print('Invoking {} by invoker {}.'.format(module_type, INVOKER_VERSION))
    print('')
    print('args: ({} items)'.format(len(args)))
    print('--------------------------------------------')
    for arg in args:
        print(arg)
    print('--------------------------------------------')

    for command in INITIAL_COMMANDS:
        run(command)

    command_json_arg = first_or_none(a for a in args if re.match(r'--command-file=.+/command.json', a))

    # Remove --command-file argument before invoking custom modules because it is only used inside AzureML.
    if is_custom_module:
        if command_json_arg in args:
            args.remove(command_json_arg)

    ret = run(' '.join(args))

    # Output module statistics for custom modules
    # No need to do for official modules, because official modules will do this inside module host.
    if is_custom_module:
        save_custom_module_run_statistics(command_json_arg, is_run_succeed=(ret == 0))

    # set the subprocess run result as exit value
    exit(ret)


if __name__ == '__main__':
    args = sys.argv[1:]
    execute(args)
