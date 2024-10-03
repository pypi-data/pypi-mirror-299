from air_web import get, redirectors


print(get("https://medium.com/p/dca128e0202a", redirectors=[redirectors.medium]))
