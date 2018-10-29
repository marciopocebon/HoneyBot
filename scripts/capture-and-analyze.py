import sys
import argparse
from time import sleep


from snappycap import utils
from snappycap import const
from snappycap import interfaces


def parse_commandline():
    args = argparse.ArgumentParser(description=const.DESCRIPTION)
    args.add_argument(
        "--seconds",
        help="The number of seconds to capture traffic for.",
        type=int,
        required='--analyze' in sys.argv
    )
    args.add_argument(
        "--interface",
        help="The name of the interface (--list-interfaces to show available)",
        type=str,
        required='--analyze' in sys.argv
    )
    args.add_argument(
        '--analyze',
        help="If included, capture will be uploaded for analysis to PacketTotal.com.",
        action="store_true"
    )
    args.add_argument(
        "--list-interfaces",
        help="Lists the available interfaces.",
        action="store_true"
    )
    args.add_argument(
        "--list-pcaps",
        help="Lists pcaps submitted to PacketTotal.com for analysis.",
        action="store_true"
    )
    args.add_argument(
        '--export-pcaps',
        help="Writes pcaps submitted to PacketTotal.com for analysis to a csv file.",
        action="store_true"
    )
    return args.parse_args()


if __name__ == '__main__':
    args = parse_commandline()
    if len(sys.argv) == 1:
        utils.print_pt_ascii_logo()
    if args.list_interfaces:
        utils.print_network_interaces()
    elif args.list_pcaps:
        interfaces.print_submission_status()
    elif args.export_pcaps:
        interfaces.export_submissions_status()
    elif args.analyze:
        interfaces.Database().initialize_database()
        pcap = interfaces.Capture(args.interface, timeout=args.seconds)
        print("Beginning packet capture for {} seconds. Max PacketTotal upload size is 50MB; "
              "will terminate if this is reached.".format(args.seconds))
        sleep(2)
        pcap.capture()
        print("Beginning upload...")
        pcap.upload()
        print("Upload complete!")
        pcap.save()