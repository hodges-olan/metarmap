#!/usr/bin/python3
#*/30 * * * * /root/metarmap/metar.py
import board
import neopixel
import time
import requests
import urllib3
import re
from xml.etree import ElementTree
vfr = (255,0,0)
mvfr = (0,0,255)
ifr = (0,255,0)
lifr = (0,255,255)
error = (192,192,192)
off = (0,0,0)
airports = {'OFF0': 0, 'OFF1': 1, 'KPPA': 2, 'KBGD': 3, 'KBPC': 4, 'OFF5': 5, 'KHHF': 6,
            'OFF7': 7, 'OFF8': 8, 'KPYX': 9, 'OFF10': 10, 'OFF11': 11, 'KGUY': 12,
			'OFF13': 13, 'KHQG': 14, 'OFF15': 15, 'KLBL': 16, 'OFF17': 17, 'KMEJ': 18,
			'OFF19': 19, 'OFF20': 20, 'OFF21': 21, 'KGAG': 22, 'KWWR': 23, 'OFF24': 24,
			'OFF25': 25, '3K8': 26, 'OFF27': 27, 'OFF28': 28, 'KAVK': 29, 'KEND': 30,
			'OFF31': 31, 'KGOK': 32, 'OFF33': 33, 'KWDG': 34, 'OFF35': 35, 'OFF36': 36,
			'OFF37': 37, 'KWLD': 38, 'OFF39': 39, 'KBKN': 40, 'KPNC': 41, 'OFF42': 42, 
			'KSWO': 43, 'KCUH': 44, 'KCQB': 45, 'OFF46': 46, 'OFF47': 47, 'KOKM': 48,
			'OFF49': 49, 'KRVS': 50, 'KOWP': 51, 'KTUL': 52, 'KGCM': 53, 'OFF54': 54,
			'KBVO': 55, 'OFF56': 56, 'KIDP': 57, 'KCFV': 58, 'KPPF': 59, 'OFF60': 60,
			'OFF61': 61, 'KGMJ': 62, 'KMIO': 63, 'OFF64': 64, 'KJLN': 65, 'OFF66': 66,
			'KEOS': 67, 'KHFJ': 68, 'OFF69': 69, 'KXNA': 70, 'KVBT': 71, 'KROG': 72,
			'KASG': 73, 'KFYV': 74, 'KSLG': 75, 'OFF76': 76, 'KTQH': 77, 'OFF78': 78,
			'KMKO': 79, 'OFF80': 80, 'KGZL': 81, 'KJSV': 82, 'OFF83': 83, 'KFSM': 84,
			'OFF85': 85, 'OFF86': 86, 'KMEZ': 87, 'OFF88': 88, 'KRKR': 89, 'OFF90': 90,
			'OFF91': 91, 'KMLC': 92, 'OFF93': 93, 'OFF94': 94, 'KHHW': 95, 'OFF96': 96,
			'KAQR': 97, 'OFF98': 98, 'KADH': 99, 'OFF100': 100, 'KSRE': 101, 'KSNL': 102,
			'OFF103': 103, 'KTIK': 104, 'KOUN': 105, 'KOKC': 106, 'KPWA': 107, 'KHSD': 108,
			'KRCE': 109, 'OFF110': 110, 'KCHK': 111, 'KRQO': 112, 'OFF113': 113, 'KOJA': 114,
			'KCLK': 115, 'OFF116': 116, 'KELK': 117, 'KCSM': 118, 'OFF119': 119, 'KHBR': 120,
			'OFF121': 121, 'KAXS': 122, 'KLTS': 123, 'OFF124': 124, 'OFF125': 125, 'KFSI': 126,
			'KLAW': 127, 'OFF128': 128, 'KDUC': 129, 'KPVJ': 130, 'OFF131': 131, 'KADM': 132,
			'1F0': 133, 'OFF134': 134, 'OFF135': 135, '0F2': 136, 'OFF137': 137, 'KGLE': 138,
			'OFF139': 139, 'KGYI': 140, 'KDUA': 141, 'OFF142': 142, 'F00': 143, 'OFF144': 144,
			'KPRX': 145, 'OFF146': 146, '4O4': 147, 'OFF148': 148, 'KDEQ': 149, 'OFF150': 150,
			'OFF151': 151, 'KTXK': 152, 'OFF153': 153, 'OFF154': 154, 'KOSA': 155, 'OFF156': 156,
			'KSLR': 157, 'OFF158': 158, 'KGVT': 159, 'OFF160': 160, 'KTKI': 161, 'KADS': 162,
			'OFF163': 163, 'KDTO': 164, 'KAFW': 165, 'KLUD': 166, 'KXBP': 167, 'OFF168': 168,
			'KRPH': 169, 'OFF170': 170, 'OFF171': 171, 'KCWC': 172, 'KSPS': 173, 'OFF174': 174,
			'KFDR': 175, 'F05': 176, 'OFF177': 177, 'OFF178': 178, 'KCDS': 179}
pixels = neopixel.NeoPixel(board.D18, 180, brightness=0.2, auto_write=False)

# Disable Unsecure request warning for Self-signed SSL Certificate on Palo
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def getMetar(airport):
    flight_category = 'ERROR'
    if re.match('^OFF\d*', airport):
        flight_category='OFF'
    else:
        apiCall = 'https://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&stationString={}&hoursBeforeNow=1'.format(
airport)
        resp = requests.get(apiCall, verify=False)
        root = ElementTree.fromstring(resp.content)
        for data in root.findall('data'):
            for metar in data.findall('METAR'):
                for fc in metar.findall('flight_category'):
                    flight_category = fc.text
    return flight_category


def main():
    for airport in airports:
        category = getMetar(airport)
        if category == 'VFR':
            pixels[airports[airport]] = vfr
        elif category == 'MVFR':
            pixels[airports[airport]] = mvfr
        elif category == 'IFR':
            pixels[airports[airport]] = ifr
        elif category == 'LIFR':
            pixels[airports[airport]] = lifr
        elif category == 'OFF':
            pixels[airports[airport]] = off
        else:
            pixels[airports[airport]] = error
        print(airport, category)
    pixels.show()


def test():
    pixels.fill(vfr)
    time.sleep(3)
    pixels.fill(mvfr)
    time.sleep(3)
    pixels.fill(ifr)
    time.sleep(3)
    pixels.fill(lifr)
    time.sleep(3)
    for x in range(0, 100):
        if x % 3 == 0:
            pixels[x] = (0, 255, 0)
        elif x % 3 == 1:
            pixels[x] = (255, 255, 255)
        else:
            pixels[x] = (255, 0, 0)
    time.sleep(3)
    pixels.deinit()


if __name__ == '__main__':
    main()

