import requests
import sys
from bs4 import BeautifulSoup
import io
import json

# hash(#) sign is used for writting comment in the code. Eg check below
# header to be sent when opening a url using request.get() method
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0"}


# url to open - it contains list of restaurants
url = "https://www.zomato.com/india"
# opening the above url using request.get()
response = requests.get(url, headers=HEADERS)
# check if url could be open properly
if response.ok == True:
    # url opened correctly, convert the page into text
    print ""
    print "Could open correctly: url = " + url
else:
    # url could not be opened correctly. There was some error. print error and skip this url
    print ""
    print "Error opening page : url = " + url
    print "Error is \n", response.text
    print "Skipping url = ", url

soup = BeautifulSoup(response.text, "html.parser")


def crawl_city(url_base, total_pages, city_name):
    file_name = city_name+".csv"
    zomato_file = io.open(file_name, "w", encoding='utf8')
    restaurant_count = 0
    total_pages = int(total_pages)
    for page_no in range(1, total_pages+1):
        url = url_base + "?page=" + str(page_no)

        # opening the above url using request.get()
        response = requests.get(url, headers=HEADERS)
        # check if url could be open properly
        if response.ok == True:
            # url opened correctly, convert the page into text
            print ""
            print "Could open page = " + str(page_no) + " correctly: url = " + url
        else:
            # url could not be opened correctly. There was some error. print error and skip this url
            print ""
            print "Error opening page = " + str(page_no) + ": url = " + url
            print "Error is \n", response.text
            print "Skipping url = ", url
            return False


        # converting the page to text
        list_of_restaurants_page = response.text

        # send this page in text to BeautifulSoup. using BeautifulSoup we can parse any data in the page
        # we call this soup :D
        soup = BeautifulSoup(list_of_restaurants_page, "html.parser")

        # let us find in the soup all the links(<a>) which has "class"="result-title" using findAll() function
        for link in soup.findAll('a', {"class": "result-title"}):
            # increment the counter of restaurants
            restaurant_count = restaurant_count + 1
            # get the restaurant name from the link
            restaurant_name = link.text
            # but this restaurant_name contains some random shits like spaces, enters etc
            # let's remove them and get the clean restaurant_name
            restaurant_name = restaurant_name.replace("\n", "").encode('utf-8','ignore').decode('utf-8','replace').strip()
            # now let's get the url of the restaurant from the link. It is in link like this href="the-actual-url"
            restaurant_url = link["href"]

            # nicely print the information found :D
            print ""
            print str(restaurant_count) + ") Restaurant Name:", restaurant_name.encode('ascii','ignore').decode('ascii','replace')
            print "Url: ", restaurant_url.encode('ascii','ignore').decode('ascii','replace')

            # now let's open the link of the restaurant we found out
            response_of_restaurant_url = requests.get(restaurant_url, headers=HEADERS)

            # check if restaurant_url could be opened
            if response_of_restaurant_url.ok == True:
                # url opened correctly, convert the page into text
                print "Could open " + restaurant_name.encode('ascii','ignore').decode('ascii','replace') + "'s page correctly: url = " + restaurant_url.encode('ascii','ignore').decode('ascii','replace')
            else:
                # url could not be opened correctly. There was some error. print error and skip this url
                print "Error opening " + restaurant_name.encode('ascii','ignore').decode('ascii','replace') + "'s page: url = " + restaurant_url.encode('ascii','ignore').decode('ascii','replace')
                print "Error is \n", response_of_restaurant_url.text
                print "Skipping url = ", restaurant_url.encode('ascii','ignore').decode('ascii','replace')
                return False

            # converting the page to text
            restaurant_page = response_of_restaurant_url.text

            # send this page in text to BeautifulSoup. using BeautifulSoup we can parse any data in the restaurant page like contact number, timings etc
            # we call this restaurant_soup :D
            restaurant_soup = BeautifulSoup(restaurant_page,"html.parser")

            # let's find restaurant's phone number. it is in <span> with class="tel" using find() and not findAll
            # using find() because we know there is only one <span> withe class="tel" in the entire page
            restaurant_phone = restaurant_soup.find('span', {"class": "tel"})
            # check if we could find the restaurant_phone
            if restaurant_phone != None:
                # we could find the restaurant_phone in the page
                restaurant_phone = restaurant_phone.text.replace("\n", "").encode('utf-8','ignore').decode('utf-8','replace').strip()
            else:
                # Damn it! restaurant_phone could not be found
                # let's give it some default value
                restaurant_phone = "NA"
            # nicely print phone
            print "Phone: ", restaurant_phone.encode('ascii','ignore').decode('ascii','replace')

            # let's find locality
            # it is in <b>(which is not unique)
            # but <b> is in a unique div with class="res-main-subzone-links"
            div = restaurant_soup.find('div',{"class":"res-main-subzone-links"})
            if div != None:
                b= div.find ('b')
            else:
                b = None

            if b != None:
                # found locality
                # remove shit
                restaurant_locality = b.text.replace("\n", "").encode('utf-8','ignore').decode('utf-8','replace').strip()
            else:
                # locality could not be found. set default value
                restaurant_locality = "NA"
            print "Locality: ", restaurant_locality.encode('ascii','ignore').decode('ascii','replace')



            zomato_id = "NA"
            meta = restaurant_soup.find("meta", {"property":"al:android:url"})
            if meta != None:
                zomato_id = meta["content"].strip()
                zomato_id = zomato_id.split("/").pop()
                zomato_id = zomato_id.replace("\n", "").encode('utf-8','ignore').decode('utf-8','replace').strip()
            print "Zomato ID:", zomato_id.encode('ascii','ignore').decode('ascii','replace')


            left_count = 10
            load_more_page = 0

            while left_count > 0:
                url_load_more = 'https://www.zomato.com/php/social_load_more.php'
                data_load_more = {'entity_id': zomato_id, 'limit': '500', 'profile_action': 'reviews-dd', 'page': str(load_more_page)}

                response_load_more = requests.post(url_load_more, headers=HEADERS, data=data_load_more)
                print restaurant_name.encode('ascii','ignore').decode('ascii','replace'), "Status - Review Could be opened - ", response_load_more.ok

                final_data = json.loads(response_load_more.text)
                print "page =", final_data["page"], "left_count", final_data["left_count"]

                left_count = int(final_data["left_count"])
                load_more_page = load_more_page + 1

                soup_review = BeautifulSoup(final_data["html"], "html.parser")
                div_all_review = soup_review.findAll("div", {"class":"res-review clearfix js-activity-root mbot   item-to-hide-parent stupendousact"})

                for div in div_all_review:
                    user_span = div.find("span", {"class":"h-level4 zblack"})
                    if user_span != None:
                        user_name = user_span.text
                        user_name = user_name.replace("\n", "").encode('utf-8','ignore').decode('utf-8','replace').strip()
                    else:
                        user_name = "NA"

                    div_review = div.find("div", {"class":"rev-text"})
                    user_review = div_review.contents[2]
                    if user_review != None:
                        user_review = user_review.encode('utf-8','ignore').decode('utf-8','replace').strip()
                    else:
                        user_review = "NA"


                    div_rating = div_review.contents[1].find("div", {"class":"ttupper"})
                    user_rating = None
                    if div_rating != None:
                        user_rating =  div_rating["title"]
                    if user_rating != None:
                        user_rating = user_rating.replace("\n", "").encode('utf-8','ignore').decode('utf-8','replace').strip()
                    else:
                        user_rating = "NA"

                    # print ""
                    # print user_name.encode('ascii','ignore').decode('ascii','replace'),", ", user_rating.encode('ascii','ignore').decode('ascii','replace'), ", ", user_review.encode('ascii','ignore').decode('ascii','replace')

                    zomato_file.write( str(restaurant_count) +
                        "| " + restaurant_name +
                        "| " + zomato_id +
                        "| " + restaurant_locality +
                        "| " + user_name +
                        "| " + user_rating +
                        "| " + user_review +
                        "| " + "\n")

    zomato_file.close()

crawl_city("https://www.zomato.com/bangalore/restaurants", 197, "bangalore")
