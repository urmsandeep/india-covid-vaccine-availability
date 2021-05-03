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
#    -v VACCINE   Vaccine Type [CS=Covishield CX=Covaxin, default=any]
#
#  RESTRICTIONS:
#     Filtering based on Vaccine Type (Covishield/Covaix) is not supported
#     as this data is not accurate from Cowin source.
#
#  Revisions:
#     ver 1.0, 01-May-2021, Sandeep R, initial version
###############################################################################
#  Sample output
#  python cowin_appt.py -p 560027 -d 03-05-2021 
#
# ============================================================================
# Checking availability for Pincode=560027 Date=03-05-2021 Vaccine=Any
# ==============================================================================
#
# PinCode:560027 Center:Shanthinagar UPHC BLOCK 1 Vaccine: MinAge:45 Availability:3
#
# PinCode:560027 Center:SHANTHI NAGAR UPHC C1 Vaccine: MinAge:45 Availability:1
##########################
# Pre-requsites
# Python 2.x or later
#########################


import requests
import time
import json
import argparse
from datetime import date

cowin_appt_api = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?"
url_cowin_vax_by_pin = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?"

def cowin_vax_availability_by_pincode (pincode, vax_date, vaccine, log):
    found=False
    req_url = url_cowin_vax_by_pin + "pincode=" + pincode + "&date=" + vax_date
    if (log):
        print(req_url)
    res = requests.get(req_url)
    if (res.status_code != 200):
        print("Response: Not OK")
        return
    
    # parse json response
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

    if (found == False):
        print("\n** No Avaliability at any Center **")

def cowin_vax_availability_iterate_pincode (pincode, vax_date, vaccine, log):
    pin = int(pincode)
    end_pin = pin + 1
    while (pin < end_pin):
        cowin_vax_availability_by_pincode(str(pin), vax_date, vaccine, log)
        pin += 1

def vaccine_name (vaccine, arg):
    if (arg == True):
        switcher = {
           'CS' : "COVISHIELD",
           'CX' : "COVAXIN",
        }
        return switcher.get(vaccine, "Any")
    else:
        print(vaccine)
        if not vaccine:
            return("COVISHIELD*")
        else:
            return(vaccine)
      
  
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

    ##############################################
    # We search for any Vaccine as the data on
    # vaccine type is not accurate in CoWin
    ##############################################
    vaccine = "Any"
    print("\n======================================================================================")
    print("Checking availability for Pincode=%s Date=%s Vaccine=%s" %
          (args.pincode, vax_date, vaccine))
    print("========================================================================================")

    cowin_vax_availability_iterate_pincode (args.pincode, vax_date, vaccine, args.log)


if __name__ == "__main__":
    start=time.time()
    initialize()
    elapsed = (time.time() - start)
    #print("Time elapsed is : {:.2f} seconds".format(elapsed))


