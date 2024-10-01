import ocfinance as of
email = "dhruvan2006@gmail.com"
password = "70F#9F48C25ZqUB$9"
df = of.download("https://cryptoquant.com/analytics/query/66637453d376670a9fe4ee61?v=6669c51123b047232b32fae1", email=email, password=password)
print(df)