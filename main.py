import requests
import json
from bs4 import BeautifulSoup as bs
from bs4.element import Tag


url = "https://www.scrapethissite.com/pages/simple/"
response = requests.get(url)
soup = bs(response.text, "html.parser")

countries = soup.find_all("div", class_="col-md-4 country")

data = []
for country in countries:
    country_name = country.find("h3").text.strip()
    capital = country.find("span", class_="country-capital").text.strip()
    data.append({
        "Country": country_name,
        "Capital": capital
    })

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("\nСписок стран и столиц:")
for i, item in enumerate(data, start=1):
    print(f"{i}. Country: {item['Country']}; Capital: {item['Capital']};")

with open("template.html", "r", encoding="utf-8") as f:
    template = f.read()

soup = bs(template, "html.parser")

container = soup.find("div", class_="place-here")
if not container:
    raise ValueError("Шаблон не содержит элемент с классом 'place-here'.")

table = Tag(name="table")
thead = Tag(name="thead")
thead_row = Tag(name="tr")

headers = ["Страна", "Столица"]
for header in headers:
    th = Tag(name="th")
    th.string = header
    thead_row.append(th)
thead.append(thead_row)
table.append(thead)

tbody = Tag(name="tbody")
for item in data:
    tr = Tag(name="tr")

    td_country = Tag(name="td")
    td_country.string = item["Country"]
    tr.append(td_country)

    td_capital = Tag(name="td")
    td_capital.string = item["Capital"]
    tr.append(td_capital)

    tbody.append(tr)
table.append(tbody)

container.append(table)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(soup.prettify())

print("\nHTML файл успешно создан: index.html")
