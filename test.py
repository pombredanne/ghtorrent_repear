import requests
url = "https://api.github.com/repos/chartjs/chartjs-plugin-datalabels/commits"
uname = "Kowndinya2000"
token = "94f54d47604013ae801126b1dac439762e19bdf7"
page = requests.get(url).json()[0]["commit"]["committer"]["date"].split("T")[0]
print(page)