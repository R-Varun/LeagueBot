import requests
from config import Constants
ID_LOOKUP_CACHE = {}

URLS = {"sum_id":"https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/"
        ,"sum_stats": "https://na.api.pvp.net/api/lol/na/v2.5/league/by-summoner/"}


def format_sum_id(aString):
    retString = "";
    for char in aString:
        if char != " ":
            retString += char
    return retString.lower()


def lookup_summoner_id(sumID):
    data = {}
    raw_data = {}
    stats_url = URLS['sum_stats'] + sumID
    r = requests.get(stats_url, params={"api_key": Constants.getToken()})
    if r.status_code == 200:
        ranked_league = r.json()[sumID][0]
        data['tier'] = ranked_league['tier']
        for player in ranked_league['entries']:
            if player['playerOrTeamId'] == sumID:
                raw_data = player
                data['division'] = player['division']
                data['leaguePoints'] = player['leaguePoints']
                data['wins'] = player['wins']
                data['losses'] = player['losses']
                break

    return (r.status_code, data, raw_data)


def find_summoner_id(sumName):
    if sumName in ID_LOOKUP_CACHE:
        return ID_LOOKUP_CACHE[sumName]

    data = {}
    sumName = format_sum_id(sumName)
    request_url = URLS['sum_id'] + sumName
    r = requests.get(request_url, params={"api_key": Constants.getToken()})
    if r.status_code == 200:
        data['id'] = str(r.json()[sumName]['id'])
        data['name'] = r.json()[sumName]['name']
        ID_LOOKUP_CACHE[sumName] = data['id']

    return r.status_code, data


