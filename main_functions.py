# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import   requests
import   time

from picamera import PiCamera
from PIL import Image, ImageEnhance
camera            = PiCamera()

def take_photo():
    
   #camera.resolution = (1024, 768)
    image_dir         = '/home/pi/python/ALPR/images/'
    image_filename    = 'Camera001_'+str(time.ctime()+'.jpg')
    filename          = image_dir+image_filename
    
    camera.capture(filename)
    
    im = Image.open(filename)
    im = im.resize((1024, 768), Image.ANTIALIAS) 
    im.save(image_dir+'low_'+image_filename, 'JPEG', quality=80)
    
    #contrast = ImageEnhance.Contrast(im)
    #im = contrast.enhance(2)
    #im.save(image_dir+'contrast_'+image_filename, 'JPEG', quality=80)
    
    return image_dir+'low_'+image_filename


def image_to_plate(image_file, token):

    
    end_point  = 'https://platerecognizer.com/plate-reader/'
    header     = {'Authorization': 'token {}'.format(token)}
    with open(image_file, 'rb') as fp:
        response = requests.post(end_point,files = dict(upload=fp),headers=header)
    plate      = response.json()
    return plate['results'][0]['plate'].upper()

def get_registration_details(rego):

    sleep_delay = 500
    url         = "https://www.vicroads.vic.gov.au/registration/buy-sell-or-transfer-a-vehicle/buy-a-vehicle/check-vehicle-registration/vehicle-registration-enquiry?utm_campaign=VR-checkrego&utm_medium=button&utm_source=VR-checkrego"
    headers     = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.103 YaBrowser/18.7.0.2695 Yowser/2.5 Safari/537.36'}
    s           = requests.session()
    r           = s.get(url,proxies=None,headers=headers)
    soup        = BeautifulSoup(r.text,"lxml")
    vs          = soup.find("input",attrs={'id':'__VIEWSTATE'})['value']
    vsg         = soup.find("input",attrs={'id':'__VIEWSTATEGENERATOR'})['value']

    # Really important pause
    time.sleep(sleep_delay/1000)

    data={
          '__EVENTTARGET': '',
          '__EVENTARGUMENT': '',
          '__VIEWSTATEGENERATOR':vsg,
          '__VIEWSTATE':vs,
          '__VIEWSTATEENCRYPTED':'',
          'site-search-head':'',
          'ph_pagebody_0$phheader_0$_FlyoutLogin$PersonalEmail$EmailAddress':'',
          'ph_pagebody_0$phheader_0$_FlyoutLogin$PersonalPassword$SingleLine_CtrlHolderDivShown': '',
        'ph_pagebody_0$phheader_0$_FlyoutLogin$OrganisationEmail$EmailAddress': '',
        'ph_pagebody_0$phheader_0$_FlyoutLogin$OrganisationPassword$SingleLine_CtrlHolderDivShown': '',
        'ph_pagebody_0$phheader_0$_FlyoutLogin$PartnerEmail$EmailAddress': '',
        'ph_pagebody_0$phheader_0$_FlyoutLogin$PartnerPassword$SingleLine_CtrlHolderDivShown': '',
        'ph_pagebody_0$phthreecolumnmaincontent_1$panel$VehicleSearch$vehicle-type': 'car/truck',
        'ph_pagebody_0$phthreecolumnmaincontent_1$panel$VehicleSearch$vehicle-identifier-type': 'registration number',
        'ph_pagebody_0$phthreecolumnmaincontent_1$panel$VehicleSearch$RegistrationNumberCar$RegistrationNumber_CtrlHolderDivShown': rego,
        #'honeypot':'',
        'ph_pagebody_0$phthreecolumnmaincontent_1$panel$btnSearch': 'Search'
          }
    try:
        # Post form
        p=s.post(url,proxies=None,headers=headers,data=data)#,timeout=5)

        # Process data
        post_soup = BeautifulSoup(p.text, 'html.parser')
        mydiv     = post_soup.find("div", {"class": "detail-module"})
        data      = mydiv.find_all("div",{'class':'display'})
        output = 'License plate:'+str(data[0].text)+' - Car:'+data[2].text+' - Rego status:'+data[1].text
        return output

    except:
        return 'Failed'


def image_to_plate(image_file):

    token      = '2ef17db4e347230cd37aa1da1cb41d4571633dc6'
    end_point  = 'https://platerecognizer.com/plate-reader/'
    header     = {'Authorization': 'token {}'.format(token)}
    with open(image_file, 'rb') as fp:
        response = requests.post(end_point,files = dict(upload=fp),headers=header)
    plate      = response.json()
    return plate['results'][0]['plate'].upper()

def get_registration_details(rego):

    sleep_delay = 500
    url         = "https://www.vicroads.vic.gov.au/registration/buy-sell-or-transfer-a-vehicle/buy-a-vehicle/check-vehicle-registration/vehicle-registration-enquiry?utm_campaign=VR-checkrego&utm_medium=button&utm_source=VR-checkrego"
    headers     = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.103 YaBrowser/18.7.0.2695 Yowser/2.5 Safari/537.36'}
    s           = requests.session()
    r           = s.get(url,proxies=None,headers=headers)
    soup        = BeautifulSoup(r.text,"lxml")
    vs          = soup.find("input",attrs={'id':'__VIEWSTATE'})['value']
    vsg         = soup.find("input",attrs={'id':'__VIEWSTATEGENERATOR'})['value']

    # Really important pause
    time.sleep(sleep_delay/1000)

    data={
          '__EVENTTARGET': '',
          '__EVENTARGUMENT': '',
          '__VIEWSTATEGENERATOR':vsg,
          '__VIEWSTATE':vs,
          '__VIEWSTATEENCRYPTED':'',
          'site-search-head':'',
          'ph_pagebody_0$phheader_0$_FlyoutLogin$PersonalEmail$EmailAddress':'',
          'ph_pagebody_0$phheader_0$_FlyoutLogin$PersonalPassword$SingleLine_CtrlHolderDivShown': '',
        'ph_pagebody_0$phheader_0$_FlyoutLogin$OrganisationEmail$EmailAddress': '',
        'ph_pagebody_0$phheader_0$_FlyoutLogin$OrganisationPassword$SingleLine_CtrlHolderDivShown': '',
        'ph_pagebody_0$phheader_0$_FlyoutLogin$PartnerEmail$EmailAddress': '',
        'ph_pagebody_0$phheader_0$_FlyoutLogin$PartnerPassword$SingleLine_CtrlHolderDivShown': '',
        'ph_pagebody_0$phthreecolumnmaincontent_1$panel$VehicleSearch$vehicle-type': 'car/truck',
        'ph_pagebody_0$phthreecolumnmaincontent_1$panel$VehicleSearch$vehicle-identifier-type': 'registration number',
        'ph_pagebody_0$phthreecolumnmaincontent_1$panel$VehicleSearch$RegistrationNumberCar$RegistrationNumber_CtrlHolderDivShown': rego,
        #'honeypot':'',
        'ph_pagebody_0$phthreecolumnmaincontent_1$panel$btnSearch': 'Search'
          }
    try:
        # Post form
        p=s.post(url,proxies=None,headers=headers,data=data)#,timeout=5)

        # Process data
        post_soup = BeautifulSoup(p.text, 'html.parser')
        mydiv     = post_soup.find("div", {"class": "detail-module"})
        data      = mydiv.find_all("div",{'class':'display'})
        output = 'License plate:'+str(data[0].text)+' - Car:'+data[2].text+' - Rego status:'+data[1].text
        return output

    except:
        return 'Failed'
