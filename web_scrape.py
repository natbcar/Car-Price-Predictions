from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv

def scrape_data(my_url):
    """Scrapes data from used trucks webpage on TrueCar.com using BeautifulSoup package.

    Parameters:
        my_url (str): website url to be scraped
    """
    url_client = urlopen(my_url) #open url
    html_page = url_client.read() #read html doc from url
    soup = BeautifulSoup(html_page, 'html.parser') #parse html document
    cars = soup.find_all("div", {"data-qa":"Listing"}) #get all of the used car listings on webpage
    car_data = [] #create blank list to store data tuples
    for car in cars:
        make_model = car.find('span', class_="vehicle-header-make-model text-truncate").text
        make = make_model.split()[0]
        model = ' '.join(make_model.split()[1:])
        miles = car.find('div', {"data-test":"vehicleMileage"}).text
        year = car.find('span', class_="vehicle-card-year").text
        exterior_interior_color = car.find('div', {"data-qa":"ExteriorInteriorColor"}).text
        exterior_color = exterior_interior_color.split()[0]
        interior_color = exterior_interior_color.split()[2]
        accidents_usage = car.find('div', {"data-qa":"ConditionHistory"}).text #too hard to parse will do once data is scraped
        try:
            price = car.find('div', {"data-qa":"VehicleCardPricingBlock"}).text
        except AttributeError:
            #some cars do not have a price listed, ignore error and deal with during data cleaning
            price = ''
        car_data.append([make, model, miles, year, exterior_color, interior_color, accidents_usage, price])
    write_csv(car_data)

def write_csv(car_data):
    """Writes car data to a csv file

    Parameters:
        car_data (list): A list containting make, miles, year, color, accidents, and usage for every car
    """
    with open('car_prices.csv', 'a') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(car_data)

def scrape_pages(num_pages):
    """Loops through all the web pages on TrueCar website for used trucks and
    scapes data using scrape_data function

    Parameters:
        num_pages (int): number of weppages to scrape
    """
    for i in range(2,num_pages):
        my_url = "https://www.truecar.com/used-cars-for-sale/listings/body-truck/location-provo-ut/?page={}&searchRadius=500&sort[]=best_match".format(i)
        scrape_data(my_url)
        print('completed webpage number {}'.format(i))

if __name__ == "__main__":
    #write headers to the .csv file
    headers = "Make, Model, Miles, Year, Exterior Color, Interior Color, Other Info, Price\n"
    f = open('car_prices.csv', 'a')
    f.write(headers)
    f.close()
    scrape_pages(286)
