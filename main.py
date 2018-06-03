import argparse

from selfcar.common import Vehicle, Driver
from selfcar.manual import ManualDriver

parser = argparse.ArgumentParser(description='Some description.')

parser.add_argument('--vehicle', dest='vehicle', default='default')
parser.add_argument('--driver', dest='driver', default='default')
args = parser.parse_args()

if args.vehicle == 'default':
    vehicle = Vehicle()
else:
    raise ValueError('Unknown vehicle type: {}'.format(args.vehicle))

if args.driver == 'manual':
    driver = ManualDriver()
elif args.driver == 'default':
    driver = Driver()
else:
    raise ValueError('Unknown driver type: {}'.format(args.driver))

driver.drive(vehicle)
