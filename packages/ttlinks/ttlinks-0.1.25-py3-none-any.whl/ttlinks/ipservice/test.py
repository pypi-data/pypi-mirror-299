from ttlinks.ipservice.ip_address import IPv4Addr, IPv6Addr
from ttlinks.ipservice.ip_converters import DecimalIPv4ConverterHandler, DecimalIPv6ConverterHandler
import ipaddress

from ttlinks.ipservice.ip_factory import IPv4Factory

if __name__ == '__main__':
    ipv4factory = IPv4Factory()
    subnet = ipv4factory.subnet('129.119.69.64/26')
    print(subnet.subnet_range)