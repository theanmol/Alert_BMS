import logging
import azure.functions as func
import urllib
from bs4 import BeautifulSoup
import smtplib,ssl

def send_email():

    value = "Book Now"

    message = {
        "personalizations": [ {
          "to": [{
            "email": "email@gmail.com"
            }]}],
        "subject": "Available",
        "content": [{
            "type": "text/plain",
            "value": value }]}

    sendGridMessage.set(json.dumps(message))


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    language="" #set language for which you want list else it fetches all showing movies
    URL="https://in.bookmyshow.com/hyderabad/movies/"+language
    hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive'}

    req = urllib.request.Request(url = URL, headers = hdr)
    page = urllib.request.urlopen(req)
    soup = BeautifulSoup(page, 'html.parser')

    movieslist=soup.find_all('div', {"class" : "card-container wow fadeIn movie-card-container"})

    movies = [x.find('a').attrs for x in movieslist]
    names = [ x['title'] for x in movies]

    print("NOW SHOWING MOVIES")
    print(set(names))

    date=""   #date for which the movie you want alert for
    select="Jojo Rabbit"    #movie name you want the alert for
    #select=input("Enter movie you care about : ")

    for x in movies:
        if x['title'].lower()==select.lower():
            code=x['href'].split('/')[-1]
            #print(code)
            break

    URL= "https://in.bookmyshow.com/buytickets/"+select.replace(' ','-')+"-hyderabad/movie-hyd-"+code+"-MT/"+date
    #print(URL)
    req = urllib.request.Request(url = URL, headers = hdr)
    page = urllib.request.urlopen(req)
    soup = BeautifulSoup(page, 'html.parser')

    l=soup.find('ul',{"id" : "venuelist"})
    l=l.find_all('li', {"class" : "list"})

    availabletheaters = []
    for theatre in l:
        availabletheaters.append(theatre['data-name'])
        print(theatre['data-name'])
        time=theatre.find_all('a', { "class" : "showtime-pill" , "data-availability" : "A"  })
        for show in time:
            print(show['data-date-time']),
        print()

    #print(availabletheaters)
    preffered_venues=['AMB Cinemas: Gachibowli','PVR: Inorbit, Cyberabad'] #set your preffered theatre values here

    a_set = set(availabletheaters)
    b_set = set(preffered_venues)

    if len(a_set.intersection(b_set)) > 0:
        print("Available")
        return func.HttpResponse("Available!")
        send_email()
    else :
        print("Not available yet")
        return func.HttpResponse("Not Yet Available!")
