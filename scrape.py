import requests
from bs4 import BeautifulSoup

url = "https://www.icocalendar.io/active-icos"
page = requests.get(url=url)
from csv import writer

soup = BeautifulSoup(page.content, "html.parser")
results = soup.find_all("div", class_="div-block-3 mob")

with open("crypto.csv", "w", newline="", encoding="utf8") as f:
    thewriter = writer(f)
    header = ["Blockchain", "Launch Type", "Fundraising Goal", "Token Price", "Price Change", "Launch date",
              "Project Link"]
    thewriter.writerow(header)

    for result in results:
        # Blockchain
        try:
            blockchain = result.find("a", class_="card-blockchain icorows").text.strip()
        except:
            blockchain = "None"
        #     Launch Type
        try:
            launch_type = result.find("a", class_="fundsraised tempfr marketcap icorow").text.strip()
        except:
            launch_type = "None"
        #     Fundraising Goal
        try:
            fundraising_goal = result.find("a", class_="fundsraised tempfr marketcap icorow amount").text.strip()
            if fundraising_goal != "TBA":
                fundraising_goal = "$" + fundraising_goal
        except:
            fundraising_goal = "None"
        #     Token Price
        try:
            token_price = result.find("a", class_="fundsraised marketcap icorow").text.strip()
        except:
            token_price = "None"

        # price change
        downstatsection_div = result.find('div', class_='description-block downstatsection')
        upstatsection_div = result.find("div", class_="description-block upstatsection")
        if downstatsection_div:
            price_change_text = downstatsection_div.find(
                class_='fundsraised tempfr marketcap pricechange downprice').text.strip()
            price_change = f"Decrease ({price_change_text})"
        elif upstatsection_div:
            price_change_text = result.find(class_="fundsraised tempfr marketcap pricechange").text.strip()
            price_change = f"Increase ({price_change_text})"
        else:
            price_change = "No price change"
        #     Launch date
        launch_date_links = result.find('a', class_='social-link')
        launch_date = launch_date_links.get("href")
        if launch_date == "#":
            launch_date = "None"
        else:
            launch_date = launch_date
        #     Project link
        project_links = result.find("a", class_="social-link fa-solid learnmore")
        if project_links:
            project_link = project_links.get('href')
        else:
            project_link = "None"
        info = [blockchain, launch_type, fundraising_goal, token_price, price_change, launch_date, project_link]
        thewriter.writerow(info)
