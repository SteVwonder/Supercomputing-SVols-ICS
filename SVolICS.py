import csv
import argparse
import re
from datetime import datetime

from pytz import timezone
import ics

central_tz = timezone('US/Central')
bad_time_re = re.compile(r'^([0-9]+)(AM|PM)')

def fix_bad_times(time_str):
    match = bad_time_re.match(time_str)
    if match:
        time_str = "{}:00{}".format(match.group(1), match.group(2))
    return time_str

def convert_vol_time(vol_time, date):
    begin_str, end_str = vol_time.split('-')
    begin_str = fix_bad_times(begin_str.lstrip().upper())
    end_str = fix_bad_times(end_str.lstrip().upper())

    begin_str = "{}T{}".format(date, begin_str).upper()
    begin_datetime = datetime.strptime(begin_str, "%Y-%m-%dT%I:%M%p")
    begin_datetime = central_tz.localize(begin_datetime)
    begin_time = begin_datetime.isoformat()

    end_str = "{}T{}".format(date, end_str).upper()
    end_datetime = datetime.strptime(end_str, "%Y-%m-%dT%I:%M%p")
    end_datetime = central_tz.localize(end_datetime)
    end_time = end_datetime.isoformat()

    return begin_time, end_time

def save_calendar(filename, calendar):
    with open(filename, 'w') as outfile:
        outfile.writelines(calendar)

def create_calendar(schedule):
    calendar = ics.Calendar()
    for event in schedule:
        date = event['Day']
        description = "{} - {}".format(event['Type'], event['Tag'])
        for volunteer_time in event['Volunteer'].split(','):
            begin_time, end_time = convert_vol_time(volunteer_time, date)
            ics_event = ics.Event(name=event['Event'],
                                  begin=begin_time,
                                  end=end_time,
                                  description=description,
                                  location=event['Location'])
            calendar.events.append(ics_event)
    return calendar

def read_schedule(filename):
    with open(filename, 'r') as infile:
        reader = csv.DictReader(infile, delimiter='\t')
        reader.next()
        return list(reader)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("schedule_file", help="Exported tab-delimited file from Linklings")
    parser.add_argument("calendar_file", help="File to save ics calendar to")
    args = parser.parse_args()

    if args.calendar_file[-4:] != '.ics':
        print "Warning: we recommend that the output calendar file extension be .ics"

    schedule = read_schedule(args.schedule_file)
    calendar = create_calendar(schedule)
    save_calendar(args.calendar_file, calendar)

if __name__ == "__main__":
    main()
