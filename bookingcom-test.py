import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd

def getBookingUrls():
    urls = list()

    for i in hotels:
        url_gen = "https://www.booking.com/hotel/au/"+i+".en-gb.html?checkin="+checkin_date+"&checkout="+checkout_date+"&group_adults="+str(adults_no)+"&group_children="+str(child_no)+"&no_rooms="+str(rooms_no)+"&selected_currency="+currency

        urls.append(url_gen)
    return urls

def getHotelInfo(urls,checkin_date):
    headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}

    hotels_df = pd.DataFrame()

    for i in range(len(urls)):    
        resp = requests.get(urls[i],headers=headers)

        if resp.status_code==200:
            print("..{} url success!".format(urls[i]))
        else: 
            print("..{} url error".format(urls[i]))
        
        soup = BeautifulSoup(resp.text, 'html.parser')

        hotel_info = {}
        hotel_info["name"] = soup.find("h2",{"class":"pp-header__title"}).text
        hotel_info["address"] = soup.find("span",{"class":"hp_address_subtitle"}).text.strip("\n")
        hotel_info["rating"] = soup.find("div",{"class":"a447b19dfd"}).text

        facilities = soup.find("ul",{"b3605c5e50 eb11e518ca bdfadf615e"})
        fac_lists = facilities.find_all("span",{"class":"e39ce2c19b"})
        for j in range(len(fac_lists)):
            fac_lists[j] = fac_lists[j].text.replace("\n","")
        hotel_info["facilities"] = fac_lists

        last_hotel_name = hotel_info["name"]

        print(hotel_info)

        ids= list()

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
                
        for j in range(0,len(ids)):    
            
            allData = soup.find("tr",{"data-block-id":ids[j]})
            try:
                rooms = allData.find("span",{"class":"hprt-roomtype-icon-link"})
                if rooms is not None:
                    last_room = rooms.text.replace("\n","")
                try: 
                    rooms = rooms.text.replace("\n","")
                except:
                    if last_hotel_name == hotel_info["name"]:
                        rooms = last_room
                    else:
                        rooms = None
            except:
                rooms = None
            try:
                guests = allData.find("span",{"class":"bui-u-sr-only"})
                guests = guests.text.replace("\n","")
            except:
                guests = None
            try:
                prices = allData.find("div",{"class":"bui-price-display__value prco-text-nowrap-helper prco-inline-block-maker-helper prco-f-font-heading"})
                prices = prices.text.replace("\n","")
            except:
                prices = None
            
            print(rooms)
            print(guests)
            print(prices)

            if rooms is None and guests is None and prices is None: continue

            room_info = {"room_type":rooms,"guests":guests,"prices":str(prices)}
            print(room_info) 

            info = {**hotel_info, **room_info}
            hotels_df = hotels_df.append(info,ignore_index=True) 

        print("-------------") 
    return hotels_df

def writeCsvFile(filename, df):    
    df.to_csv(filename, index=False)

if __name__ == "main":
    
    checkin_date = str(datetime.date.today()+ datetime.timedelta(days=1))
    checkout_date = str(datetime.date.today()+ datetime.timedelta(days=2))
    adults_no = 2
    child_no = 0
    rooms_no = 1
    currency = "AUD"

    hotel1 = "<hotel-name1-city>"
    hotel2 = "<hotel-name2-city>"
    hotel3 = "<hotel-name3-city>"

    hotels = [hotel1, hotel2, hotel3]

    urls = getBookingUrls(hotels, checkin_date, checkout_date, adults_no, child_no, rooms_no, currency)

    hotels_df = getHotelInfo(urls,checkin_date)    
    filename = "<filename.csv>"
    writeCsvFile(filename, hotels_df)
