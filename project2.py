from bs4 import BeautifulSoup
import requests
import csv
url="https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"
HEADERS = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64)  AppleWebKit/537.36 (KHTML, like Gecko)  Chrome/44.0.2403.157 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'}
webpage = requests.get(url, headers=HEADERS)
soup = BeautifulSoup(webpage.content, "html.parser")
k=soup.find_all("div",attrs={"data-component-type": "s-search-result"})
filename = "product.csv"
fields = ['Discription', 'Produt Discription','ASIN', 'Manufacturer']
rows=[]
l=[]
for item in k:
    l.append("https://www.amazon.in" + ((item.find_all("a", class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"))[0]).get("href"))
for item in l:
    url=item
    HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)  AppleWebKit/537.36 (KHTML, like Gecko)  Chrome/44.0.2403.157 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'}
    webpage = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "html.parser")
    name=(soup.find_all("span", attrs={"class": "a-size-large product-title-word-break"})[0]).get_text()
    ul=((soup.find_all("ul", attrs={"class": "a-unordered-list a-vertical a-spacing-mini"})))
    lis=""
    for i in ul:
        lis=i.get_text()+lis

    try:
        x=url.split("%2Fdp%2F")
        y=x[1].split("%2")
        new1=y[0]
    except:
        x=url.split("/dp/")
        y=x[1].split("/")
        new1=y[0]

    manufacture="NA"
    try:
        manu = ((soup.find_all("ul", attrs={"class": "a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list"})))[0]
        m=manu.find_all("li")
        for i in range(len(m)):
            if "By Manufacturer" in (((m[i].find_all("span"))[1]).get_text()):
                continue
            elif "manufacturer" in (((m[i].find_all("span"))[1]).get_text()).lower():
                manufacture=(((m[i].find_all("span"))[2]).get_text()).strip()
                break
    except:
        manu=((soup.find_all("table", attrs={"id":"productDetails_techSpec_section_1"})))[0]
        m=manu.find_all("tr")
        for i in m:
            k=i.find_all("th")
            if "manufacturer" in (k[0].get_text()).lower():
                manufacture=(((i.find_all("td"))[0]).get_text()).strip()
                break
    a=[name.strip(),lis.strip(),new1.strip(),manufacture.strip()]
    print(name.strip())
    print(lis.strip())
    print(new1.strip())
    print(manufacture.strip())
    rows.append(a)


with open(filename, 'w',encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)
    csvwriter.writerows(rows)
    print("We have written csv")



