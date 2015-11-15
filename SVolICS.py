'''
 Robert Searles
 Stephen Herbein
 Department of Computer and Information Sciences
 University of Delaware

 SVolCalendar.py
 A script for student volunteers at super computing.
 This script will take their exported volunteer schedules and create an .ics file for them to use in the calendar application of their choosing.
'''

#################################################################
###    Includes
#################################################################

# Needed for reading CSV files into a dictionary
import csv

# Needed to parse command line arguments
import argparse

# Regular Expressions
import re

# Needed for processing dates/times efficiently
from datetime import datetime

# Needed in order to account for timezone of events
from pytz import timezone

# ICS writing
import ics

import string

central_tz = timezone('US/Central')
bad_time_re = re.compile(r'^([0-9]+)(AM|PM)')

#################################################################
###    Function Declarations
#################################################################

def sanitize_string(in_str):
    return filter(lambda x: x in string.printable, in_str)

def fix_bad_times(time_str):
    '''
     fix_bad_times()
     Input: A time string
     Return: A better time string
     How it works: Takes a time string and uses a regex to make sure it is properly formatted. If not, it replaces the string with :00 appended. An example of this would be if you changed 4pm to 4:00PM.
    '''
    match = bad_time_re.match(time_str)
    if match:
        time_str = "{}:00{}".format(match.group(1), match.group(2))
    return time_str

def convert_vol_time(vol_time, date):
    '''
     convert_vol_time()
     Input: A time and a date
     Return: A beginning time and ending time
     How it works: Takes a time and date in from an event dictionary. This function will correct improperly formatted times (ex. 4pm instead of 4:00PM), and it will return a starting and ending datetime object to use in the .ics output.
    '''
    # Grab beginning and ending times
    begin_str, end_str = vol_time.split('-')

    # Fix times if they aren't properly formatted
    begin_str = fix_bad_times(begin_str.lstrip().upper())
    end_str = fix_bad_times(end_str.lstrip().upper())

    # Convert beginning time from a string into a datetime object
    begin_str = "{}T{}".format(date, begin_str).upper()
    begin_datetime = datetime.strptime(begin_str, "%Y-%m-%dT%I:%M%p")
    begin_datetime = central_tz.localize(begin_datetime)
    begin_time = begin_datetime.isoformat()

    # Convert ending time from a string into a datetime object
    end_str = "{}T{}".format(date, end_str).upper()
    end_datetime = datetime.strptime(end_str, "%Y-%m-%dT%I:%M%p")
    end_datetime = central_tz.localize(end_datetime)
    end_time = end_datetime.isoformat()

    return begin_time, end_time

def convert_attend_time(attend_time):
    '''
    convert_attend_time()
    Input: A time
    Return: A beginning time and ending time
    How it works: Takes an attend time in from an event
     dictionary. This function will correct improperly formatted times
     (ex. 4pm instead of 4:00PM), and it will return a starting and
     ending datetime object to use in the .ics output.
    '''

    # Split the date and times out by --
    date, times = attend_time.split("--")

    # Grab beginning and ending times
    begin_str, end_str = times.split('-')

    # Convert beginning time from a string into a datetime object
    begin_str = "{}T{}".format(date, begin_str).upper()
    begin_datetime = datetime.strptime(begin_str, "%Y-%m-%dT%H:%M")
    begin_datetime = central_tz.localize(begin_datetime)
    begin_time = begin_datetime.isoformat()

    # Convert ending time from a string into a datetime object
    end_str = "{}T{}".format(date, end_str).upper()
    end_datetime = datetime.strptime(end_str, "%Y-%m-%dT%H:%M")
    end_datetime = central_tz.localize(end_datetime)
    end_time = end_datetime.isoformat()

    return begin_time, end_time

def save_calendar(filename, calendar):
    '''
     save_calendar()
     Input: A filename and a calendar
     Return: Void
     How it works: Writes the ics calendar to a file.
    '''
    with open(filename, 'w') as outfile:
        outfile.writelines(calendar)

def create_calendar(schedule):
    '''
     create_calendar()
     Input: A schedule
     Return: A calendar
     How it works: Reads each event in the given schedule (list of events) and creates an ics event for each one.
    '''
    calendar = ics.Calendar()
    for event in schedule:
        date = event['Day']
        description = "{} - {}".format(event['Type'], event['Tag'])
        if 'Volunteer' in event:
            for volunteer_time in event['Volunteer'].split(','):
                begin_time, end_time = convert_vol_time(volunteer_time, date)
                ics_event = ics.Event(name=event['Event'],
                                      begin=begin_time,
                                      end=end_time,
                                      description=description,
                                      location=event['Location'])
                calendar.events.append(ics_event)
        elif 'Attend' in event:
            begin_time, end_time = convert_attend_time (event['Time'])
            ics_event = ics.Event(name=sanitize_string(event['Event']),
                                  begin=begin_time,
                                  end=end_time,
                                  description=description,
                                  location=event['Location'])
            calendar.events.append(ics_event)
        else:
            print "Warning: Event found that you are neither attending nor volunteering for: {}".format(event['Event'])
    return calendar

def read_schedule(filename):
    '''
     read_schedule()
     Input: A filename
     Return: A schedule (dictionary)
     How it works: Uses DictReader from the csv package to read in the tab-delimited file provided. It returns a list of dictionaries, where each entry is an event. The data within an event are in the form of a dictionary.
    '''
    with open(filename, 'r') as infile:
        reader = csv.DictReader(infile, delimiter='\t')
        reader.next()
        return list(reader)

#################################################################
###    Script Execution
#################################################################

def main():
    # Used to parse command line arguments
    parser = argparse.ArgumentParser()

    # Add arguments
    parser.add_argument("schedule_file", help="Exported tab-delimited file from Linklings")
    parser.add_argument("calendar_file", help="File to save ics calendar to")
    args = parser.parse_args()

    # Make sure output file extension is .ics
    if args.calendar_file[-4:] != '.ics':
        print "Warning: we recommend that the output calendar file extension be .ics"

    # Read in schedule
    schedule = read_schedule(args.schedule_file)

    # Create a calendar from events in the schedule
    calendar = create_calendar(schedule)

    # Write calendar events to .ics file
    save_calendar(args.calendar_file, calendar)

if __name__ == "__main__":
    main()
