import datetime
import requests
from bs4 import BeautifulSoup

if __name__ == "main":
    headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}

    checkin_date = str(datetime.date.today()+ datetime.timedelta(days=1))
    checkout_date = str(datetime.date.today()+ datetime.timedelta(days=2))
    adults_no = 2
    child_no = 0
    rooms_no = 1
    currency = "AUD"

    hotels = "<hotel-name-city>"

    hotel_url = "https://www.booking.com/hotel/au/"+hotels+".en-gb.html?checkin="+checkin_date+"&checkout="+checkout_date+"&group_adults="+str(adults_no)+"&group_children="+str(child_no)+"&no_rooms="+str(rooms_no)+"&selected_currency="+currency

    resp = requests.get(hotel_url,headers=headers)

    if resp.status_code==200:
        print("..url success!")
    else: 
        print("..url error")

    soup = BeautifulSoup(resp.text, 'html.parser')

    hotel_info = {}
    hotel_info["name"] = soup.find("h2",{"class":"pp-header__title"}).text
    hotel_info["address"] = soup.find("span",{"class":"hp_address_subtitle"}).text.strip("\n")
    hotel_info["rating"] = soup.find("div",{"class":"a447b19dfd"}).text

    facilities = soup.find("ul",{"b3605c5e50 eb11e518ca bdfadf615e"})
    fac_lists = facilities.find_all("span",{"class":"e39ce2c19b"})
    for i in range(len(fac_lists)):
        fac_lists[i] = fac_lists[i].text.replace("\n","")

    hotel_info["facilities"] = fac_lists
    print(hotel_info)

    ids= list()

    targetId=list()
    try:
        tr = soup.find_all("tr")
    except:
        tr = None

    ids = list()
    for y in range(0,len(tr)):
        try:
            id = tr[y].get('data-block-id')

        except:
            id = None
            print("..no room available {}".format(checkin_date))

        if( id is not None):
            ids.append(id) 
            
    for i in range(0,len(ids)):    

        allData = soup.find("tr",{"data-block-id":ids[i]})
        #  try:
        rooms = allData.find("span",{"class":"hprt-roomtype-icon-link"})
        rooms = rooms.text.replace("\n","")
        # print(rooms)

        guests = allData.find("span",{"class":"bui-u-sr-only"})
        guests = guests.text.replace("\n","")

        prices = allData.find("div",{"class":"bui-price-display__value prco-text-nowrap-helper prco-inline-block-maker-helper prco-f-font-heading"})
        prices = prices.text.replace("\n","")
        
        print(rooms)
        print(guests)
        print(prices)
        print("-------------")


