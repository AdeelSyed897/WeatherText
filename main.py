from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
from email.message import EmailMessage
import smtplib



options = webdriver.ChromeOptions()
#options.add_argument("--headless")


driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

try:
    url = 'https://www.accuweather.com/en/us/west-lake-hills/78746/current-weather/2106993'
    driver.get(url)

    time.sleep(10)

    page_source = driver.page_source


    soup = BeautifulSoup(page_source, 'html.parser')

    #HIGH LOW
    index=0
    temps = soup.find_all(attrs={"class":"temperature"})
    if temps:
        for temp in temps:
            if index==0:
                high=temp.get_text(strip=True)
            if index==1:
                low=temp.get_text(strip=True)
            index+=1
            if index==2:
                break

    #HUMID
    rows = soup.find_all(attrs={"class":"detail-item spaced-content"})

    for row in rows:
        str= row.get_text(strip=True)
        if str[0:8] == "Humidity":
            humid=str[8:len(str)]


    #CURRENT TEMP
    currentTemp = soup.find(class_='display-temp')
    if currentTemp:
        currentTemp = currentTemp.get_text(strip=True)



    #Cloud Coverage and Rain
    rows = soup.find_all(attrs={"class":"panel-item"})
    for row in rows:
        str= row.get_text(strip=True)
        if str[0:8] == "Cloud Co":
            cloCo=str[11:len(str)]
            break
        if str[15:18] == "Pre":
            rain=str[28:len(str)]


    print(high,low,humid,cloCo, currentTemp, rain)

except:
    print("something went wrong")

finally:
    # Quit the driver
    driver.quit()


print("check")

emailSender="############"
password="############"
emailReciever="############"

subject = ""
body="\n\n Temperature " + currentTemp[0:len(currentTemp)-2] +"\n High " +high[0:len(high)-3] + "\n Low " + low[0:2] + "\n Change of Rain " + rain + "\n Humidity " + humid + "\n Cloud Coverage " + cloCo


em = EmailMessage()

em['From'] = emailSender
em['To'] = emailReciever
em['Subject'] = subject
em.set_content(body)



with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(emailSender, password)
    smtp.sendmail(emailSender,emailReciever, em.as_string())

print("FINISHED")

