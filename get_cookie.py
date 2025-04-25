import requests

def get_session_from_cookie_file(cookie_file="cookies.json"):
    import json
    session = requests.Session()

    try:
        with open(cookie_file, "r", encoding="utf-8") as f:
            cookies = json.load(f)
        for cookie in cookies:
            session.cookies.set(cookie["name"], cookie["value"], domain=cookie.get("domain", "atcoder.jp"))
    except FileNotFoundError:
        return None

    # Cookieの有効性チェック
    resp = session.get("https://atcoder.jp/home")
    if "ログイン" in resp.text:
        return None
    return session

def get_valid_session():
    session = get_session_from_cookie_file()
    if session is not None:
        print("✅ Cookie有効です。ログイン済み。")
        return session

    # 無効な場合は、手動入力を求める
    print("🔐 Cookieが無効です。ブラウザからREVEL_SESSIONをコピーして貼り付けてください。")
    session = requests.Session()
    cookie_value = input("REVEL_SESSION = ").strip()
    session.cookies.set("REVEL_SESSION", cookie_value, domain="atcoder.jp")

    # 有効か再チェック
    resp = session.get("https://atcoder.jp/home")
    if "ログイン" in resp.text:
        print("❌ 入力されたCookieが無効です。もう一度確認してください。")
        return None

    # 有効なら保存
    print("✅ Cookieが有効なので保存します。")
    import json
    cookies = [{"name": "REVEL_SESSION", "value": cookie_value, "domain": "atcoder.jp"}]
    with open("cookies.json", "w", encoding="utf-8") as f:
        json.dump(cookies, f, indent=2)

    return session


if __name__ == "__main__":
    session = get_valid_session()
    if session:
        print("Cookieを取得しました")
        print(session.cookies)
    else:
        print("Cookieを取得できませんでした")