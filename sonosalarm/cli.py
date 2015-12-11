from argparse import ArgumentParser
import logging
import sonosalarm.discovery
import sonosalarm.alarm
import sys

def discovery(options):
    d = sonosalarm.discovery.Discover()
    d.printZones()

def play(options):
    p = sonosalarm.alarm.Alarm(options.config)
    p.play()

def run():
    p = ArgumentParser()
    p.add_argument('--verbose', action="store_true")

    s = p.add_subparsers(dest="action")

    p_d = s.add_parser('discovery')
    p_p = s.add_parser('play')
    p_p.add_argument('--config')

    options = p.parse_args()

    if options.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    globals()[options.action](options)


if __name__ == "__main__":
    run()
