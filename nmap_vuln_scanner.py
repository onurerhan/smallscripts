import nmap
import os


def main(target, output_file):
    output = open(output_file, 'w')
    nm = nmap.PortScanner()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    result = nm.scan(target, arguments="-sV --script=" + dir_path + "/tools/nmap_vuln_scanner/vulners.nse")['scan']
    for host in result:
        if 'tcp' in result[host]:
            for port in result[host]['tcp']:
                if 'script' in result[host]['tcp'][port]:
                    if 'vulners' in result[host]['tcp'][port]['script']:
                        output.write("\n" + host + ":" + str(port))
                        output.write(result[host]['tcp'][port]['script']['vulners'])
        if 'udp' in result[host]:
            for port in result[host]['udp']:
                if 'script' in result[host]['udp'][port]:
                    if 'vulners' in result[host]['udp'][port]['script']:
                        output.write("\n" + host + ":" + str(port))
                        output.write(result[host]['udp'][port]['script']['vulners'])


if __name__ == '__main__':
    main('192.168.1.100/24', 'output.txt')
