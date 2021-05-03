#!/usr/bin/python

#############################################################################
#  SCRIPT NAME:
#  India Cowin vaccine availability finder
#
#  PURPOSE:
#  Find available vaccination centers for given Pincode, Date, Vaccine type
#
#  USAGE:
#  python cowin_appt.py [-h] -p PINCODE [-d VAX_DATE] [-v VACCINE]
#
#  India Cowin Vax Availability Status
#
#   optional arguments:
#    -h, --help   show this help message and exit
#    -p PINCODE   Pin Code
#    -d VAX_DATE  Date for Vaccine Availability in dd-mm-yyyy format,
#                 default=today's date
#
#  RESTRICTIONS:
#     Filtering based on Vaccine Type (Covishield/Covaix) is not supported
#     as this data is not accurate from Cowin source.
#
#  Revisions:
#     ver 1.0, 01-May-2021, Sandeep Rao, initial version
#     ver 1.1, 03-May-2021, Sandeep Rao, update to reporting
###############################################################################
#  Sample output
#
#  python ./india_covid_vaccine_availability.py -p 560011 -d 04-05-2021
#
#  ======================================================================================
#  Checking availability for Pincode=560011 Date=04-05-2021 Vaccine=Any
#  ========================================================================================
#
#  PinCode: 560011 | Center: APOLLO CRADLE HOSPITAL    | MinAge: 45 | Availability: 1   | Vaccine: COVISHIELD
#
#  PinCode: 560011 | Center: Jayanagara Dispensary COVAXIN | MinAge: 45 | Availability: 0   | Vaccine: COVAXIN
##########################
# Pre-requsites
# Python 2.x or later
#########################
import requests
import time
import json
import argparse
from datetime import date

# COWIN URL PATH
cowin_appt_api = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?"
url_cowin_vax_by_pin = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?"

##########################################################
# Look for vaccination centers and availability status for
# given Pincode and Date
#########################################################
def cowin_vax_availability_by_pincode (pincode, vax_date, vaccine, log):
    found=False
 
    ##########################
    # Create the request URL
    ##########################
    req_url = url_cowin_vax_by_pin + "pincode=" + pincode + "&date=" + vax_date
    if (log):
        print(req_url)

    ##########################
    # Send request
    ##########################
    res = requests.get(req_url)
    if (res.status_code != 200):
        print("Response: Not OK")
        return
     
    ##########################
    # Parse JSON Response
    ##########################
    center_list = json.loads(res.text)
    for center in center_list['centers']:
        for session in center['sessions']:
            availability = session['available_capacity']
            if (availability > 0):
                found=True;
                print("\nPinCode: %s | Center: %-25s | MinAge: %-2s | Availability: %-3s | Vaccine: %s" %
                      (pincode, center['name'], session['min_age_limit'], 
                       session['available_capacity'], session['vaccine']))
            else:
                print("\nPinCode: %s | Center: %-25s | MinAge: %-2s | Availability: %-3s | Vaccine: %s" %
                      (pincode, center['name'], session['min_age_limit'], 
                       session['available_capacity'], session['vaccine']))

    ###############################################
    # If we did not find even a single center with
    # availability > 0, we declare.. 
    ###############################################
    if (found == False):
        print("\n** No Avaliability at any Center **")



################################################################
# TBD: Iternate over pincode "range" to look for vaccination centers
################################################################
def cowin_vax_availability_iterate_pincode (pincode, vax_date, vaccine, log):
    pin = int(pincode)
    end_pin = pin + 1
    while (pin < end_pin):
        cowin_vax_availability_by_pincode(str(pin), vax_date, vaccine, log)
        pin += 1



################################################################
# TBD: Add option to look up on vaccine type.
# At the moment COWIN data does not accurately provide the type
# of vaccine available at a center.  
################################################################
def vaccine_name (vaccine, arg):
    if (arg == True):
        switcher = {
           'CS' : "COVISHIELD",
           'CX' : "COVAXIN",
        }
        return switcher.get(vaccine, "Any")
    else:
        if not vaccine:
            return("COVISHIELD*")
        else:
            return(vaccine)
      
  
################################################################
# Setup things
################################################################
def initialize():
    parser = argparse.ArgumentParser(description="India Cowin Vax Availability Status")
    parser.add_argument('-p', action="store", dest="pincode", required=True,
                        help="Pin Code")
    parser.add_argument('-d', action="store", dest="vax_date", required=False,
                        help="Date for Vaccine Availability in dd-mm-yyyy format, default=today's date")
    parser.add_argument('-v', action="store", dest="vaccine", required=False,
                        help="Vaccine Type [CX=Covaxin, default=COVISHIELD")
    parser.add_argument('-l', '--simulate', action='store_true', dest="log", required=False,
                        help="Enable debug logs")
    args = parser.parse_args()
    args = parser.parse_args()

    if args.vax_date == None:
        vax_date=date.today().strftime('%d-%m-%Y')
    else:
        vax_date=args.vax_date

    ##########################################################
    # Here we just look for any Vaccine availability as the 
    # data on vaccine type is not accurate in CoWin
    ##########################################################
    vaccine = "Any"
    print("\n======================================================================================")
    print("Checking availability for Pincode=%s Date=%s Vaccine=%s" %
          (args.pincode, vax_date, vaccine))
    print("========================================================================================")

    ###############################
    # Begin look up process...
    ###############################
    cowin_vax_availability_iterate_pincode (args.pincode, vax_date, vaccine, args.log)


if __name__ == "__main__":
    start=time.time()
    initialize()
    elapsed = (time.time() - start)
    #print("Time elapsed is : {:.2f} seconds".format(elapsed))


