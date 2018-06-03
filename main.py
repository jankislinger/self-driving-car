import argparse

from selfcar.common import Vehicle, Tank, Driver
from selfcar.manual import ManualDriver
from selfcar.simulator import Simulator

parser = argparse.ArgumentParser(description='Some description.')

parser.add_argument('--vehicle', dest='vehicle', default='vehicle')
parser.add_argument('--driver', dest='driver', default='driver')

parser.add_argument('--file_name', dest='file_name', default='misc/simulator.mp4')
args = parser.parse_args()

if args.vehicle == 'tank':
    vehicle = Tank()
elif args.vehicle == 'simulator':
    vehicle = Simulator(args.file_name)
elif args.vehicle == 'vehicle':
    vehicle = Vehicle()
else:
    raise ValueError('Unknown vehicle type: {}'.format(args.vehicle))

if args.driver == 'manual':
    driver = ManualDriver()
elif args.driver == 'driver':
    driver = Driver()
else:
    raise ValueError('Unknown driver type: {}'.format(args.driver))

driver.drive(vehicle)
