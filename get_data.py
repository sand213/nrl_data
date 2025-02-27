import requests as re
import urllib.request
import urllib.parse
import json

url = "https://www.footystatistics.com/includes/get_players.php"

json_data = {}

# Data to be sent in the POST request
team_data = [('action', 'get_teams')]

# Encode the data
mydata = urllib.parse.urlencode(team_data).encode('utf-8')

# Create the request
req = urllib.request.Request(url, data=mydata)

# Add headers to the request
req.add_header("Content-type", "application/x-www-form-urlencoded")

# Send the request and read the response
with urllib.request.urlopen(req) as response:
    page = response.read()

# Print the response
teams = json.loads(page.decode('utf-8'))

idx = 0

for team in enumerate(teams):
    
    team_name = team['full_name']
    squad_id = team['squad_id']
    
    players_data = [('action', 'get_players'), ('squad_id', squad_id)]

    mydata = urllib.parse.urlencode(players_data).encode('utf-8')

    req = urllib.request.Request(url, data=mydata)

    req.add_header("Content-type", "application/x-www-form-urlencoded")

    # Send the request and read the response
    with urllib.request.urlopen(req) as response:
        page = response.read()
    
    players = json.loads(page.decode('utf-8'))

    for player in players:

        player_info =  [('action', 'get_player'), ('player_id', player['id'])]

        mydata = urllib.parse.urlencode(player_info).encode('utf-8')

        req = urllib.request.Request(url, data=mydata)

        req.add_header("Content-type", "application/x-www-form-urlencoded")

        # Send the request and read the response
        with urllib.request.urlopen(req) as response:
            page = response.read()

        player_data = json.loads(page.decode('utf-8'))

        data = player_data["year_2018"][0]

        # Select the fields to be added to the dictionary
        selected_fields = {
            "cost": data.get("cost"),
            "status": data.get("status"),
            "positions": data.get("positions"),
            "cost": data.get("cost"),
            "selections": data.get("selections"),
            "selections_c": data.get("selections_c"),
            "selections_vc": data.get("selections_vc"),
            "owned_by": data.get("owned_by"),
            "avg_points": data.get("avg_points"),
            "high_score": data.get("high_score"),
            "low_score": data.get("low_score"),
            "last_3_avg": data.get("last_3_avg"),
            "last_5_avg": data.get("last_5_avg"),
            "last_5_avg": data.get("last_5_avg"),
            "ppm": data.get("ppm"),
            "match_stats" : data.get("match_stats")
            }
        
        if float(selected_fields["selections"]) > 1.0:
            # Create a key using player's full name and add the selected fields to json_data
            player_key = f"{data['first_name']} {data['last_name']} {data['full_name']}"
            json_data[player_key] = selected_fields

        idx += 1

        if idx == 50:
            
            with open(f'response{idx}.json', 'w') as json_file:
                json.dump(json_data, json_file, indent=4)  

