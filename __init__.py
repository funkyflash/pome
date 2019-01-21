import json
import logging
import signal
import sys
import time

import pytuya
import schedule
devices = {}


def set_desired(dev, state):
    devices[dev]['desired_state'] = state


def exit_gracefully():
    sys.exit(0)


def bool_to_power(ffs):
    if ffs:
        return "on"
    else:
        return "off"

# signal.signal(signal.SIGTERM, exit_gracefully())
# signal.signal(signal.SIGINT, exit_gracefully())


def main():
    with open('dev_config.json') as cf:
        config = json.load(cf)

    for dev in config['devices']:
        devices[dev['devId']] = {'dev': pytuya.OutletDevice(dev['devId'], dev['ip'], dev['localKey']), "name": dev['name'], "desired_state": True}

    for sched in config['schedules']:
        for sched_dev in sched['devices']:
            for day in sched['days']:
                # job = getattr(schedule.every, calendar.day_name[day].lower())()
                # job.do(set_desired(sched_dev, sched['state']))
                if day is 1:
                    schedule.every().monday.at(sched['time']).do(set_desired, sched_dev, sched['state'])
                elif day is 2:
                    schedule.every().tuesday.at(sched['time']).do(set_desired, sched_dev, sched['state'])
                elif day is 3:
                    schedule.every().wednesday.at(sched['time']).do(set_desired, sched_dev, sched['state'])
                elif day is 4:
                    schedule.every().thursday.at(sched['time']).do(set_desired, sched_dev, sched['state'])
                elif day is 5:
                    schedule.every().friday.at(sched['time']).do(set_desired, sched_dev, sched['state'])
                elif day is 6:
                    schedule.every().saturday.at(sched['time']).do(set_desired, sched_dev, sched['state'])
                elif day is 7:
                    schedule.every().sunday.at(sched['time']).do(set_desired, sched_dev, sched['state'])
    for job in schedule.jobs:
        print(job)

    try:
        while True:
            schedule.run_pending()
            for i, dev_handle in devices.items():
                try:
                    cur_state = dev_handle['dev'].status()['dps']['1']
                    print("Device {} is {}.".format(dev_handle['name'], bool_to_power(cur_state)))
                    if dev_handle['desired_state'] is not cur_state:
                        logging.warning("Device {} was supposed to be {}, but instead was {}.".format(dev_handle['name'],
                                                                                                   bool_to_power(dev_handle['desired_state']),
                                                                                                   bool_to_power(
                                                                                                       cur_state)))
                        dev_handle['dev'].set_status(dev_handle['desired_state'])
                except ConnectionResetError:
                    pass
            time.sleep(15)
    except KeyboardInterrupt:
        exit(0)


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    main()
