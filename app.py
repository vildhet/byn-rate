#!/usr/bin/env python3

import argparse


def run_server():
    from web import server
    server.run()


def update_data():
    from data import daily
    all_data = daily.get_all()
    for d in all_data:
        print('Updating %s...' % d.data_type)
        d.update()


parser = argparse.ArgumentParser()
parser.add_argument('--update', action='store_true')
args = parser.parse_args()


if args.update:
    update_data()
else:
    run_server()