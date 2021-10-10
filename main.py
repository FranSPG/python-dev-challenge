import argparse

from rich.console import Console
from pcapng_reader import PCAPNGReader


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str, help='Pcap file path')
    parser.add_argument('--comment', type=str, help='Comment to add', required=False)
    parser.add_argument('number', type=int, help='Packet number')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    pcapng = PCAPNGReader(args.file)
    console = Console()

    if args.comment:
        try:
            console.print(pcapng.insert_comment_in_i_packet(args.number, args.comment), style='bold green')
        except ValueError as v:
            console.log(v, style='bold red')
        except Exception as e:
            console.log(e, style='bold red')
    else:
        try:
            console.log(pcapng.display_i_packet(args.number))
        except ValueError as v:
            console.log(v, style='bold red')
        except Exception as e:
            console.log(e, style='bold red')
