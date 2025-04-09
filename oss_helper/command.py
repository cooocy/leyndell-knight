import os
import sys

from oss_helper import mine_logger, logger_filename, kits, oss


def get_handler(command: str):
    if 'help' == command:
        return help_
    if 'list' == command:
        return list_
    if 'download' == command:
        return download
    if 'put' == command:
        return put
    if 'delete' == command:
        return delete
    if 'gc' == command:
        return gc
    print('Args Error. Exec `./interface.py help` for help.')
    sys.exit(1)


def help_(args: list):
    print('')
    print('This is oss helper.')
    print('')
    print('Command: help/list/download/put/delete')
    print('')

    print('* help')
    print('Show this help.')
    print('')

    print('* list')
    print('Usage: ./interface.py list [--marker <key>] [—-limit <limit>]')
    print('       key    Only key name in oss, not the full https url.')
    print('       limit  The objects count to list, must be int.')
    print('e.g.')
    print('./interface.py list')
    print('./interface.py list --marker x.png')
    print('./interface.py list --marker x.png --limit 20')
    print('')

    print('* download')
    print('Usage: ./interface.py download <key> [path]')
    print('       key   Only key name in oss, not the full https url.')
    print('       path  The local path to storage downloaded file, must be a filename.')
    print('e.g.')
    print('./interface.py download x.png')
    print('./interface.py download x.png ~/tmp/x.png')
    print('')

    print('* put')
    print('Usage: ./interface.py put <file>')
    print('       path  The local file path to uploaded, must be a file.')
    print('e.g.')
    print('./interface.py put x.png')
    print('./interface.py put /root/x.png')
    print('')

    print('* delete')
    print('Usage: ./interface.py delete <key>')
    print('       key   Only key name in oss, not the full https url.')
    print('e.g.')
    print('./interface.py delete x.png')
    print('')

    print('* gc')
    print('Usage: ./interface.py gc')
    print('Delete log file defined in `config.yaml`.')
    print('')


def list_(args: list):
    marker = ''
    limit = 20
    args_len = len(args)
    if args_len != 0 and args_len != 2 and args_len != 4:
        print('Args Error. Exec `./interface.py help` for help.')
        sys.exit(1)
    if args_len == 2:
        if args[0] == '--marker':
            marker = args[1]
        elif args[0] == '--limit':
            limit = args[1]
        else:
            print('Args Error. Exec `./interface.py help` for help.')
            sys.exit(1)
    if args_len == 4:
        if args[0] == '--marker':
            marker = args[1]
        elif args[0] == '--limit':
            limit = args[1]
        else:
            print('Args Error. Exec `./interface.py help` for help.')
            sys.exit(1)
        if args[2] == '--marker':
            marker = args[3]
        elif args[2] == '--limit':
            limit = args[3]
        else:
            print('Args Error. Exec `./interface.py help` for help.')
            sys.exit(1)
    if not str(limit).isdigit():
        print('Args Error. <limit> must be int. Exec `./interface.py help` for help.')
        sys.exit(1)
    limit = int(limit)
    bucket = oss.get_bucket()
    r = bucket.list_objects(marker=marker, max_keys=limit)
    for obj in r.object_list:
        print(obj.key)


def download(args: list):
    args_len = len(args)
    if args_len != 1 and args_len != 2:
        print('Args Error. Exec `./interface.py help` for help.')
        sys.exit(1)
    key = args[0]
    path = key
    if args_len == 2:
        path = args[1]

    # The path is not absolute path.
    if not os.path.isabs(path):
        path = os.path.abspath(path)
    print(f'Download {key} to {path}')
    if os.path.isdir(path):
        print('Args Error. <path> must be a filename. Exec `./interface.py help` for help.')
        sys.exit(1)
    oss.get_bucket().get_object_to_file(key, path)


def put(args: list):
    if len(args) != 1:
        print('Args Error. Exec `./interface.py help` for help.')
        sys.exit(1)
    file = args[0]
    if not os.path.isfile(file):
        print('Args Error. <file> must exist and must be file. Exec `./interface.py help` for help.')
        sys.exit(1)
    bucket = oss.get_bucket()
    res = bucket.put_object_from_file(kits.gen_oss_file_name(file), file)
    url = res.resp.response.url.replace('http://', 'https://')
    key = url[url.rindex('/') + 1:]
    print(url)
    mine_logger.log('put', file, key)


def delete(args: list):
    if len(args) != 1:
        print('Args Error. Exec `./interface.py help` for help.')
        sys.exit(1)
    key = args[0]
    res = oss.get_bucket().delete_object(key)
    print(res.resp.response.ok)
    mine_logger.log('delete', key)


def gc(args: list):
    if len(args) > 0:
        print('Args Error. Exec `./interface.py help` for help.')
        sys.exit(1)
    if os.path.exists(logger_filename):
        os.remove(logger_filename)
