import os
import csv
from icalendar import Calendar, Event, Timezone, TimezoneStandard
from datetime import datetime, timedelta
from pytz import timezone
import hashlib

# Read fixtures from CSV file
fixtures = []
with open('fixtures.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip header row
    for row in reader:
        fixtures.append(row)

# Create calendar
cal = Calendar()
cal.add('prodid', '-//Allestree Juniors Milan Fixtures//')
cal.add('version', '2.0')
cal.add('X-WR-CALNAME', 'Allestree Juniors Milan Fixtures 2024/25')
cal.add('LAST-MODIFIED', datetime.now(timezone('UTC')))
cal.add('REFRESH-INTERVAL;VALUE=DURATION', 'PT1H')  # Suggest refreshing every hour

# Add VTIMEZONE component
tz = Timezone()
tz.add('tzid', 'Europe/London')
tz.add('x-lic-location', 'Europe/London')

tzs = TimezoneStandard()
tzs.add('tzname', 'GMT/BST')
tzs.add('dtstart', datetime(1970, 1, 1, 0, 0, 0))
tzs.add('rrule', {'freq': 'yearly', 'bymonth': 3, 'byday': '-1su'})
tzs.add('tzoffsetfrom', timedelta(hours=0))
tzs.add('tzoffsetto', timedelta(hours=1))

tz.add_component(tzs)
cal.add_component(tz)

# Timezone
uk_tz = timezone('Europe/London')

# Create events
for fixture in fixtures:
    event = Event()
    start_dt = datetime.strptime(fixture[1], "%d/%m/%y %H:%M")
    end_dt = start_dt.replace(hour=12, minute=00)  # Set end time to 12:00

    # Create summary based on whether result is available
    if fixture[6]:  # If result is available
        summary = f"{fixture[2]} {fixture[6]} {fixture[3]}"
    else:
        summary = f"{fixture[2]} vs {fixture[3]}"

    # Append type if it's not 'League'
    if fixture[4] != 'League':
        summary += f" ({fixture[4]})"

    event.add('summary', summary)
    event.add('dtstart', uk_tz.localize(start_dt))
    event.add('dtend', uk_tz.localize(end_dt))
    event.add('dtstamp', datetime.now(timezone('UTC')))  # Add DTSTAMP
    event.add('location', fixture[5])
    event.add('description', f"Fixture between {fixture[2]} and {fixture[3]} at {fixture[5]}. Type: {fixture[4]}")
    event.add('last-modified', datetime.now(timezone('UTC')))
    
    # Generate a consistent UID for the event
    uid_string = f"2024-2025_{fixture[0]}"  # Use season and match ID
    uid = hashlib.md5(uid_string.encode()).hexdigest()
    event['uid'] = f"{uid}@allestree-juniors-milan.github.io"
    
    cal.add_component(event)

# Create 'ical' folder if it doesn't exist
os.makedirs('ical', exist_ok=True)

# Save to file in the 'ical' folder
file_path = os.path.join('ical', 'allestree_juniors_milan_fixtures_2024_2025.ics')
with open(file_path, 'wb') as f:
    f.write(cal.to_ical())

print(f"iCal file created: {file_path}")