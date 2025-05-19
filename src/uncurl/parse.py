import re
import os
import sys
from urllib.parse import parse_qs, urlparse


unescape_compile = re.compile(r'\\(.)')


def unescape_json(s):
    # Handle all escaped characters \X -> X where X is any character
    return unescape_compile.sub(r'\1', s)


def extract_query_params(url: str):
    query = urlparse(url).query
    parsed = parse_qs(query)
    return {k: v[0] if len(v) == 1 else v for k, v in parsed.items()}


def parse_headers(args):
    headers = {}
    for h in args.header:
        if ':' in h:
            k, v = h.split(':', 1)
            headers[k.strip()] = v.strip()

    if args.compressed:
        headers.setdefault('Accept-Encoding', 'gzip, deflate, br')

    return headers


def parse_auth(args):
    if not args.user:
        return None

    if ':' in args.user:
        user, pwd = args.user.split(':', 1)
        return (user, pwd)
    else:
        print("Error: --user must be in 'username:password' format", file=sys.stderr)
        sys.exit(1)


def parse_proxies(args):
    if not args.proxy:
        return {}

    proxies = {
        'http': args.proxy,
        'https': args.proxy
    }

    if args.proxy_user and ':' in args.proxy_user:
        pu, pp = args.proxy_user.split(':', 1)
        proxy_auth = f"{pu}:{pp}@"
        for proto in proxies:
            if '://' in proxies[proto]:
                proto_scheme, rest = proxies[proto].split('://', 1)
                proxies[proto] = f"{proto_scheme}://{proxy_auth}{rest}"
            else:
                proxies[proto] = f"http://{proxy_auth}{proxies[proto]}"

    return proxies


def add_cookie(headers, args):
    if not args.cookie:
        return

    cookie_header = None
    if '=' in args.cookie:
        cookie_header = args.cookie
    elif args.cookie == '-':
        cookie_header = sys.stdin.read().strip()
    elif os.path.isfile(args.cookie):
        with open(args.cookie, 'r') as f:
            lines = f.readlines()
        cookies = []
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if line.lower().startswith('set-cookie:'):
                line = line[len('set-cookie:'):].strip()
            cookies.append(line)
        cookie_header = '; '.join(cookies)
    elif args.cookie == '':
        # 启动 cookie 引擎但不传 cookie：requests 无等价行为，可忽略
        pass
    else:
        print(f"无法识别 --cookie 参数格式: {args.cookie}", file=sys.stderr)

    if cookie_header:
        headers.setdefault('Cookie', cookie_header)


def parse(args):
    url = unescape_json(args.url)
    params = extract_query_params(url)
    method = args.X or ('POST' if args.data else 'GET')

    headers = parse_headers(args)
    auth = parse_auth(args)
    proxies = parse_proxies(args)
    verify = not args.insecure
    data = args.data
    add_cookie(headers, args)

    return params, dict(
        method=method,
        url=url,
        headers=headers,
        data=data,
        auth=auth,
        proxies=proxies,
        verify=verify
    )
