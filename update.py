import requests
from bs4 import BeautifulSoup
import sys
import json
import time
import datetime
from get_cookie import get_valid_session

def extract_usernames(json_data):
    # JSONデータをPythonオブジェクトに変換
    data = json.loads(json_data)
    
    # ユーザー名を格納するリスト
    usernames = []
    user_size = 30
    
    # StandingsDataから順にユーザー名を抽出
    for user in data["StandingsData"]:
        username = user["UserScreenName"]
        if not username in usernames:
            usernames.append(username)
        if len(usernames) == user_size:
            break

    return usernames

def get_extended_standings(session, contest):
    time.sleep(0.2)
    url = f"https://atcoder.jp/contests/{contest}/standings/extended/json/?showAllUsers=true"
    response = session.get(url)
    json = response.text
    return extract_usernames(json)

def update_last_update_time():
    # HTMLファイルのパスを指定
    html_file_path = 'index.html'

    # 現在の日時を取得
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # HTMLファイルを読み込む
    with open(html_file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # 最終更新日時を表示する要素を見つける
    last_update_div = soup.find(id="last-update")

    if last_update_div:
        # 日時を更新
        last_update_div.string = f"最終更新日時: {current_time}"
    else:
        print("Error: Could not find the element with id 'last-update'")

    # 変更をHTMLファイルに書き込む
    with open(html_file_path, 'w', encoding='utf-8') as file:
        file.write(str(soup))


# メイン処理
if __name__ == "__main__":
    print("スクリプトを開始します...")
    
    
    import configparser

    config = configparser.ConfigParser()
    config.read('config.ini')
    username = config['atcoder']['username']
    password = config['atcoder']['password']

    #session = login_to_atcoder(username, password)
    session = get_valid_session()
    if session is None:
        print("ログインに失敗しました。スクリプトを終了します。")
        sys.exit(1)
    
    print("ログイン後の処理を開始します...")
    point = [100,75,60,50,45,40,36,32,29,26,24,22,20,18,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1]

    from collections import defaultdict
    gp30 = defaultdict(int)

    standings_data = {}

    
    contest_list = ["ahc002", "ahc004", "ahc005", "ahc006", 
                    "ahc007", "ahc009", "ahc010", "ahc012", 
                    "ahc013", "ahc014", "ahc015", "ahc016", 
                    "ahc017", "ahc018", "ahc019", "ahc020", "ahc021", 
                    "ahc022", "ahc023", "ahc024", "ahc025", 
                    "ahc026", "ahc027", "ahc028", "ahc029", 
                    "ahc030", "ahc031", "ahc032", "ahc033", 
                    "ahc034", "ahc035", "ahc036", "ahc037",
                    "ahc038", "ahc039", "ahc040", "ahc041",
                    "ahc042", "ahc043", "ahc044", "ahc045",
                    "ahc046", "ahc047",
                    "intro-heuristics", "future-contest-2021-qual", 
                    "future-contest-2021-final", "future-contest-2022-final", 
                    "future-contest-2023-final", "toyota-hc-2023spring", 
                    "newjudge-2308-heuristic", "toyota2023summer-final"]
    for contest in contest_list:
        usernames = get_extended_standings(session, contest)
        date = "2000-01-01"
        standings_data[contest] = {
            "date": date,
            "ranking": [{"rank": i+1, "username": usernames[i]} for i in range(len(usernames))]
        }
    print("updated standings_data")
    with open('atcoder_standings.json', 'w', encoding='utf-8') as f:
        json.dump(standings_data, f, ensure_ascii=False, indent=4)

    update_last_update_time()