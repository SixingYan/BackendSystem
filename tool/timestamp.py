#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import arrow


parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('start', type=str)
parser.add_argument('-d', '--days', type=int)
parser.add_argument('-H', '--hours', type=int)
parser.add_argument('-m', '--minutes', type=int)
args = parser.parse_args()

start = args.start
shift_args = {
    "days": args.days if args.days else 0,
    "hours": args.hours if args.hours else 0,
    "minutes": args.minutes if args.minutes else 0
}

start_ts = arrow.get(start).timestamp
end_ts = arrow.get(start_ts).shift(**shift_args).timestamp

print("{:10s} {:15s} {:20d}".format("start_ts", arrow.get(start_ts).format("YYYY-MM-DD HH:mm:ss"), start_ts))
print("{:10s} {:15s} {:20d}".format("end_ts", arrow.get(end_ts).format("YYYY-MM-DD HH:mm:ss"), end_ts))
