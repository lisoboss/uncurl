import sys
import argparse
from pprint import pprint
import requests

from .parse import parse


def print_code(params, kwargs):
    io = sys.stdout
    print("import requests\n", file=io)

    print("# params\nparams = ", end='', file=io)
    pprint(params, indent=2, sort_dicts=False, stream=io)
    print("", file=io)

    print("response = requests.request(**", end='', file=io)
    pprint(kwargs, indent=2, sort_dicts=False, stream=io)
    print(")\n", file=io)
    print("print(response)", file=io)
    print("print(response.text)", file=io)


def cmd_parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('-b', '--cookie', default=None)
    parser.add_argument('-d', '--data', '--data-binary', '--data-raw', default=None)
    parser.add_argument('-X', default='')
    parser.add_argument('-H', '--header', action='append', default=[])
    parser.add_argument('--compressed', action='store_true')
    parser.add_argument('-k','--insecure', action='store_true')
    parser.add_argument('--user', '-u', default=())
    parser.add_argument('-i','--include', action='store_true')
    parser.add_argument('-s','--silent', action='store_true')
    parser.add_argument('-x', '--proxy', default={})
    parser.add_argument('-U', '--proxy-user', default='')

    return parser.parse_args()


def main_request():
    args = cmd_parse_args()
    _, kwargs = parse(args)
    print("\n\n--------")

    # 发起请求
    try:
        response = requests.request(**kwargs)
    except Exception as e:
        if not args.silent:
            print(f"Request failed: {e}", file=sys.stderr)
        sys.exit(1)

    print(response)
    print("--------")

    # 输出响应
    if not args.silent:
        if args.include:
            print("--------")
            print(f"HTTP/1.1 {response.status_code} {response.reason}")
            for k, v in response.headers.items():
                print(f"{k}: {v}")
            print("--------")

        # try:
        #     pprint(response.json())
        # except:
        #     print(response.text)

        print(response.text)
        print("--------")


def main():
    args = cmd_parse_args()
    params, kwargs = parse(args)
    print_code(params, kwargs)
