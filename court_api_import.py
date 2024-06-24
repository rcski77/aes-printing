import requests
from datetime import datetime, timedelta
from termcolor import colored


class Match:
    def __init__(self, timestamp, result=False, team1="null", team2="null"):
        self.timestamp = timestamp
        self.result = result
        self.team1 = team1
        self.team2 = team2
    def __str__(self):
        return str(self.timestamp) + " / " + str(self.result)
        
class Court:
    def __init__(self, name, matches):
        self.name = name
        self.matches = matches
    def __str__(self):
        return self.name
        
        
url = "https://results.advancedeventsystems.com/api/event/PTAwMDAwMzY0NDE90/courts/2024-06-24/300"
time_offset = 3600000
new_grid = []
needed = [
    Court("OCCC North 74", Match(datetime.strptime('2024-06-24 10:30:00', '%Y-%m-%d %H:%M:%S'))),
    Court("OCCC North 50", Match(datetime.strptime('2024-06-24 10:30:00', '%Y-%m-%d %H:%M:%S'))),
    Court("OCCC North 17", Match(datetime.strptime('2024-06-24 11:00:00', '%Y-%m-%d %H:%M:%S'))),
    Court("OCCC North 17", Match(datetime.strptime('2024-06-24 12:00:00', '%Y-%m-%d %H:%M:%S'))),
    Court("OCCC North 12", Match(datetime.strptime('2024-06-24 11:00:00', '%Y-%m-%d %H:%M:%S'))),
    Court("OCCC North 23", Match(datetime.strptime('2024-06-24 11:00:00', '%Y-%m-%d %H:%M:%S'))),
    Court("OCCC North 2", Match(datetime.strptime('2024-06-24 11:00:00', '%Y-%m-%d %H:%M:%S'))),
    ]

courtgrid = requests.get(url).json()

for court in courtgrid.get('CourtSchedules'):
    court_object = Court(court.get('Name'), [])
    new_grid.append(court_object)

    for match in court.get('CourtMatches'):
        team1 = match.get('FirstTeamText')
        team2 = match.get('SecondTeamText')
        time = datetime.fromtimestamp((match.get('ScheduledStartDateTime') - time_offset) / 1e3)
        match_object = Match(time, match.get('HasOutcome'), team1, team2)
        court_object.matches.append(match_object)
        
print()
for scoresheet in needed:
    print("Looking for match:")
    print(scoresheet)
    print(scoresheet.matches)

    for each in new_grid:
        if each.name == scoresheet.name:
            for match in each.matches:
                if scoresheet.matches.timestamp == match.timestamp:
                    if "Winner" in match.team1 or "Winner" in match.team2 or "Loser" in match.team1 or "Loser" in match.team2:
                        print(colored("Match NOT ready", 'red'))
                    else:
                        print(colored("Scoresheet ready, PRINT!", 'green'))
                        break         
    print()