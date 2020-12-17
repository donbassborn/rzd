import os
import time
import pymsgbox
import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException        

def main():
    URL = "https://pass.rzd.ru/tickets/public/ru?layer_name=e3-route&st1=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0&code1=2000000&st0=%D0%9D%D0%B8%D0%B6%D0%BD%D0%B8%D0%B9+%D0%9D%D0%BE%D0%B2%D0%B3%D0%BE%D1%80%D0%BE%D0%B4&code0=2060001&tfl=3&md=0&checkSeats=1&dt0="
    dateNow = datetime.date(2020, 10, 24)
    dateEnd = datetime.date(2020, 11, 24)

    сsvString = "Поезд;Дата;Отправление;Прибытие;Цена\r"

    firefox = webdriver.Firefox()


    while dateNow <= dateEnd:
        firefox.get(URL + "&dt0=" + dateNow.strftime("%d.%m.%Y"))
        
        trains = list()

        while len(trains) == 0:
            trains = firefox.find_elements_by_class_name("route-item")
            time.sleep(0.5)


        for train in trains:
            trainName = train.find_element_by_class_name("route-trtitle").text
            if trainName.find("ЛАСТОЧКА") > 0 or trainName.find("СТРИЖ") > 0:
                trainDepTime = train.find_elements_by_class_name("train-info__route_time")[1].text
                trainArrTime = train.find_elements_by_class_name("train-info__route_time")[3].text

                trainCarPrice = 0
                trainCarTypes = train.find_elements_by_class_name("route-carType-item")
                for trainCarType in trainCarTypes:
                    if trainCarType.find_element_by_class_name("serv-cat").text == "Сидячий":
                        trainCarPrice = trainCarType.find_element_by_class_name("route-cartype-price-rub").text.replace(",", "")
                        break
                
                trainType = "Error"
                if trainName.find("ЛАСТОЧКА") > 0:
                    trainType = "Ласточка"
                elif trainName.find("СТРИЖ") > 0:
                    trainType = "Стриж"


                printString = trainType + ";" + dateNow.strftime("%d.%m.%Y") + ";" + trainDepTime + ";" + trainArrTime + ";" + trainCarPrice
                print(printString)
                сsvString += (printString + "\n")

        
        dateNow += datetime.timedelta(days=1)

    firefox.close()
    with open("C:\\Users\\teremok\\Desktop\\хочу здохнуть\\СТПО\\Labs\\rzd\\output_back.csv", "w") as text_file:
        print(сsvString, file=text_file)

if __name__ == "__main__":
    main()
