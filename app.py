#!/usr/bin/env python3

import argparse


def run_server():
    from backend import server
    server.run()


def update_data():
    from backend import data
    all_data = data.get_all()
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