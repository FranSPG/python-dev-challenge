import subprocess
import os
import json


class PCAPNGReader:
    def __init__(self, filename: str):
        self.filename = filename
        self.path = os.getcwd()

    def insert_comment_in_i_packet(self, i: int, comment: str):

        i_valid = self.validate_i(i)
        if i_valid:
            new_filename = f'{self.path}/pcapng_files/{self.filename.split(".")[0]}_comment_in_{i}_packet.pcapng'
            editcap_process = f'editcap -a "{i}:{comment}" {self.path}/{self.filename} {new_filename}'
            subprocess.call(editcap_process, shell=True)
            return f"New file {new_filename} created, with the comment [bold white]{comment}[/bold white] in the packet number {i}."

    def display_i_packet(self, i):
        i_valid = self.validate_i(i)
        if i_valid:
            tshark_process = f"tshark -T json -r {self.path}/{self.filename} -c {i}"
            result = subprocess.check_output(tshark_process, shell=True)
            result_json = json.loads(result.decode())[-1]
            return result_json

    def validate_i(self, i):
        number_of_packets_process = f'capinfos {self.path}/{self.filename} -c'
        n_packets = subprocess.Popen(number_of_packets_process, shell=True, stdout=subprocess.PIPE)
        n_packets = n_packets.stdout.readlines()[1]
        n_packets = n_packets.decode().split('  ')[1].strip()
        if 'k' in n_packets:
            n_packets = n_packets.split()[0]
            n_packets += '000'
            n_packets = int(n_packets)
        if n_packets < i:
            raise ValueError(
                f"The number of packet {i} is not in the file. There are {n_packets} in this file, try another number.")
        else:
            return True
