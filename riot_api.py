import requests
import time
import pandas as pd

name = 'hide on bush'
api_key = 'RGAPI-5b351140-1ef9-4538-b9db-fcc954e5b400'

def get_id(name):
    url = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/"+name+'?api_key='+api_key
    page = requests.get(url)
    return page.json()

def get_rank(id):
    url = "https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/"+id+'?api_key='+api_key
    page = requests.get(url)
    return page.json()

def get_grandmaster():
    url = grandmaster = 'https://kr.api.riotgames.com/lol/league/v4/grandmasterleagues/by-queue/RANKED_SOLO_5x5?api_key='+api_key
    page = requests.get(url)
    league_df = pd.DataFrame(page.json())
    league_df.reset_index(inplace=True)
    league_entries_df = pd.DataFrame(dict(league_df['entries'])).T
    league_df = pd.concat([league_df, league_entries_df], axis=1)
    league_df = league_df.drop(['index', 'queue', 'name', 'leagueId', 'entries', 'rank', 'tier', 'summonerId', 'leaguePoints', 'wins', 'losses', 'inactive', 'freshBlood', 'hotStreak'], axis=1)
    league_df['puuid'] = ['']*len(league_df)
    return league_df

def get_puuid_df(df):
    j=0
    k=0
    for i in range(len(df)):
        url = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/'+df['summonerName'][i] + '?api_key=' + api_key
        page = requests.get(url)
        j += 1
        k += 1
        df['puuid'][i] = page.json()['puuid']
        if j == 15:
            time.sleep(1)
            j = 0
        if k == 95:
            time.sleep(115)
            k = 0
    return df

def get_matchid(puuid):
    url = 'https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/'+puuid+'/ids'+'?api_key='+api_key
    page = requests.get(url)
    return page.json()

def get_matchid_df(df_puuid):
    j=0
    k=0
    df_match = []
    df_match2 = []
    for i in df_puuid.index:
        url = 'https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/'+df_puuid['puuid'][i]+'/ids'+'?api_key='+api_key
        page = requests.get(url)
        j += 1
        k += 1
        df_match += page.json()
        df_match2 += [df_puuid['puuid'][i]]*len(page.json())
        if j == 15:
            time.sleep(1)
            j = 0
        if k == 95:
            time.sleep(115)
            k = 0
    df = pd.DataFrame({'matchid' : df_match, 'puuid' : df_match2})
    new_df = pd.merge(df, df_puuid, how= 'left', left_on= 'puuid', right_on= 'puuid')
    return new_df

def get_ingame(matchid):
    url='https://asia.api.riotgames.com/lol/match/v5/matches/'+matchid+'?api_key=' + api_key
    page = requests.get(url)
    return page.json()

def get_ingame_df(df):
    for i in range(len(df)):
      url='https://asia.api.riotgames.com/lol/match/v5/matches/' + str(df['gameId'].iloc[i]) + '?api_key=' + api_key
      r = requests.get(url)
      if r.status_code == 200:
        pass
      elif r.status_code == 429:
        print('api cost full : infinite loop start')
        print('loop location : ',i)
        start_time = time.time()

        while True:
            if r.status_code == 429:

                print('try 10 second wait time')
                time.sleep(10)

                r = requests.get(url)
                print(r.status_code)

            elif r.status_code == 200:
                print('total wait time : ', time.time() - start_time)
                print('recovery api cost')
                break
      elif r.status_code == 503:
        print('service available error')
        start_time = time.time()

        while True:
            if r.status_code == 503 or r.status_code == 429:

                print('try 10 second wait time')
                time.sleep(10)

                r = requests.get(api_url)
                print(r.status_code)

            elif r.status_code == 200:
                print('total error wait time : ', time.time() - start_time)
                print('recovery api cost')
                break
      elif r.status_code == 403:
        print('you need api renewal')
        print('break')
        break

    mat = pd.DataFrame(list(r.json().values()), index=list(r.json().keys())).T
    match_fin = pd.concat([df, mat])
    a_ls = list(match_fin['teams'])
    team1_df = pd.DataFrame()
    for i in range(len(a_ls)):
      try:
        a_ls[i][0].pop('bans',None)
        team1 = pd.DataFrame(list(a_ls[i][0].values()),index = list(a_ls[i][0].keys())).T
        team1_df = team1_df.append(team1)
      except:
        pass
    team1_df.index = range(len(team1_df))
    team2_df = pd.DataFrame()
    for i in range(len(a_ls)):
      try:
        a_ls[i][1].pop('bans',None)
        team2 = pd.DataFrame(list(a_ls[i][1].values()),index = list(a_ls[i][1].keys())).T
        team2_df = team2_df.append(team2)
      except:
        pass
    team2_df.index = range(len(team2_df))
    data_team = pd.concat([team1_df,team2_df, match_fin[['gameDuration']]],axis=1)
    return data_team