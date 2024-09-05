import os
from icalendar import Calendar, Event
from datetime import datetime, timedelta
from pytz import timezone

# Data from the table
fixtures = [
    ("08/09/24 10:30", "Melbourne Dynamo Pistons", "Allestree Juniors Milan TEST UPDATE", "Melbourne Sports Park Pitch 2 ANOTHER TEST"),
    ("15/09/24 10:30", "Allestree Juniors Milan", "Ripley Town", "DCC 2023 Darley Playing Fields Pitch 3"),
    ("22/09/24 10:30", "Mickleover C P Ajax", "Allestree Juniors Milan", "Mickleover Country Park S.C. Pitch 1"),
    ("29/09/24 10:30", "Allestree Juniors Milan", "Mickleover C P Ajax", "DCC 2023 Darley Playing Fields Pitch 4"),
    ("06/10/24 10:30", "Erewash Eagles", "Allestree Juniors Milan", "DCC 2023 Chaddesden Park Pitch 5"),
    ("13/10/24 10:30", "Allestree Juniors Milan", "Melbourne Dynamo Pistons", "DCC 2023 Darley Playing Fields Pitch 2"),
    ("20/10/24 10:30", "Shelton FC Bisons", "Allestree Juniors Milan", "Hippo Park Pitch 1 (Cup)"),
    ("27/10/24 10:30", "Codnor Sports Legends", "Allestree Juniors Milan", "Aldercar College Pitch 1"),
    ("10/11/24 10:30", "Allestree Juniors Milan", "Codnor Sports Legends", "DCC 2023 Darley Playing Fields Pitch 5"),
    ("17/11/24 10:30", "Springwood United Tornadoes", "Allestree Juniors Milan", "DCC 2023 Alvaston Park Pitch 4"),
    ("24/11/24 10:30", "Field Lane Raiders", "Allestree Juniors Milan", "Field Lane Community Centre Pitch 2"),
    ("01/12/24 10:30", "Allestree Juniors Milan", "Field Lane Raiders", "DCC 2023 Darley Playing Fields Pitch 5"),
    ("15/12/24 10:30", "Allestree Juniors Milan", "Erewash Eagles", "DCC 2023 Darley Playing Fields Pitch 6"),
    ("05/01/25 10:30", "Allestree Juniors Milan", "Springwood United Tornadoes", "DCC 2023 Darley Playing Fields Pitch 5"),
    ("12/01/25 10:30", "West Hallam Dynamos", "Allestree Juniors Milan", "Beech Lane Recreation Ground"),
    ("19/01/25 10:30", "Allestree Juniors Milan", "West Hallam Dynamos", "DCC 2023 Darley Playing Fields Pitch 3"),
    ("26/01/25 10:30", "Ripley Town", "Allestree Juniors Milan", "Greenwich Park Pitch 2")
]

# Create calendar
cal = Calendar()
cal.add('prodid', '-//Allestree Juniors Milan Fixtures//')
cal.add('version', '2.0')
cal.add('X-WR-CALNAME', 'Allestree Juniors Milan Fixtures 2024/25')

# Timezone
uk_tz = timezone('Europe/London')

# Create events
for fixture in fixtures:
    event = Event()
    start_dt = datetime.strptime(fixture[0], "%d/%m/%y %H:%M")
    end_dt = start_dt.replace(hour=12, minute=30)  # Set end time to 12:30

    event.add('summary', f"{fixture[1]} vs {fixture[2]}")
    event.add('dtstart', uk_tz.localize(start_dt))
    event.add('dtend', uk_tz.localize(end_dt))
    event.add('location', fixture[3])
    event.add('description', f"Fixture between {fixture[1]} and {fixture[2]} at {fixture[3]}.")
    
    cal.add_component(event)

# Create 'ical' folder if it doesn't exist
os.makedirs('ical', exist_ok=True)

# Save to file in the 'ical' folder
file_path = os.path.join('ical', 'allestree_juniors_milan_fixtures_2024_2025.ics')
with open(file_path, 'wb') as f:
    f.write(cal.to_ical())

print(f"iCal file created: {file_path}")