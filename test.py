import selrequests

with selrequests.Session() as s:
    r = s.get("https://www.roblox.com/")
    print(r)