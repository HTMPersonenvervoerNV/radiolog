#!/usr/bin/env python2

import re
import sys

# 	'M129': re.compile('LogonMessage: Block (\d+) ReliefBlock (\d+) Journey (\d+) Line (\d+) Route (\d+)'),
#	'M152': re.compile('GPS Position \((\d+)(\w) (\d+),(\d+)\'\|(\d+)(\w) (\d+),(\d+)\) #Sat(\d+) (.+)'),
#       'M229': re.compile('LogonMessage: Block (\d+) ReliefBlock (\d+) Journey (\d+) Line (\d+) Route (\d+)'),
p = re.compile('(\d+-\d+-\d+ \d+:\d+:\d+).* -I- .*CENTRAL <-- # (\d+) : (M\d+) (.*)')
frag = {
    'M128': re.compile('(.*)'),
    'M129': re.compile('LogonMessage: Block (\d+) Journey (\d+) Line (\d+) Route (\d+) .*'),
    'M131': re.compile('(.+) (\d+)'),
    'M139': re.compile('Position, Stop (\d+) Dist (\d+).0 Trigger=\( (\w+ \w+) \)'),
    'M140': re.compile('(\w+) \((.+)\)'),
    'M141': re.compile('(.*)'),
    'M152': re.compile('GPS Position \((\d+)(\w) (\d+),(\d+)\'\|(\d+)(\w) (\d+),(\d+) .*\) #Sat(\d+) (.+)'),
    'M153': re.compile('TickerMessage: Request text \(ID (\d+)\)'),
    'M199': re.compile('curtailment order, Ack\?true, Reason: OK, ID: (\d+)'),
    'M228': re.compile('IMSIMessagePart@(\d+)'),
    'M229': re.compile('LogonMessage: Block (\d+) Journey (\d+) Line (\d+) Route (\d+) .*'),
    'M230': re.compile('DriverID (\d+)'),
    'M231': re.compile('LogonMessage: Line (\d+) Run (\d+) Dest (\d+)'),
    'M242': re.compile('StopDependentRequestMsg \((\d+).*\) = RequestMode: (.+), Block No: (\d+), JourneyIndex: (\d+), StopsIndex: (\d+), BlockOrLineCourseNoOfTaker: (\d+), IdOfMeasure: (\d+), NumberOfRequestedTrips: (\d+), NumberOfPeopleScheduledToBoard: (\d+), DiversionNo: (\d+)')
}

files = {}

for k in frag.keys():
    files[k] = open('/mnt/resource/radiolog-parsed/' + k + '.csv', 'w')

for line in sys.stdin:
    m = p.match(line)
    if m is not None:
        if m.group(3) in frag:
            m2 = frag[m.group(3)].split(m.group(4))
            if m2[0] == '':
		date = m.group(1).split(' ')[0]
                timestamp = m.group(1).replace(' ', 'T')
                vehicle = m.group(2)

                if m.group(3) == 'M152':
                    lon = str(int(m2[1]) + (int(m2[3]) + (float('0.' + m2[4]))) / 60.0)[0:9]
                    lat = str(int(m2[5]) + (int(m2[7]) + (float('0.' + m2[8]))) / 60.0)[0:9]
                    sat = m2[9]
                    open = str('open' in m2[10])

                    output = [timestamp, vehicle, lon, lat, sat, open]
                    files[m.group(3)].write('\t'.join(output) + '\n')

                else:
                    output = [timestamp, vehicle] + m2[1:-1]
                    files[m.group(3)].write('\t'.join(output) + '\n')


