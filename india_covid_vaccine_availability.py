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

# Global
global total_availability

##########################################################
# Look for vaccination centers and availability status for
# given Pincode and Date
#########################################################
def cowin_vax_availability_by_pincode (pincode, vax_date, vaccine, display_all, minage, log):
    total_availability=0
    found = False;
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
        print("Response:[%s] Not OK Code:" % (res.status_code))
        return
     
    ##########################
    # Parse JSON Response
    ##########################
    minage = int(minage)
    found = False
    center_list = json.loads(res.text)
    for center in center_list['centers']:
        for session in center['sessions']:
            availability = session['available_capacity']

            # Filter on specified min_age
            if (minage != 0) and ((session['min_age_limit'] != int(minage))):
                break
           
            # Filter on Vaccine type 
            #print(vaccine_name(vaccine, False), session['vaccine'])
            if (vaccine is not 'Any') and (vaccine_name(vaccine, False) != session['vaccine']):
                break

            if (availability > 0):
                found=True;
                total_availability += availability
                print("\nPinCode: %s | Center: %-25s | MinAge: %-2s | Availability: %-3s | Vaccine: %s" %
                      (pincode, center['name'], session['min_age_limit'], 
                       session['available_capacity'], session['vaccine']))
            else:
                if (display_all):
                   print("\nPinCode: %s | Center: %-25s | MinAge: %-2s | Availability: %-3s | Vaccine: %s" %
                         (pincode, center['name'], session['min_age_limit'], 
                         session['available_capacity'], session['vaccine']))

    ###############################################
    # If we did not find even a single center with
    # availability > 0, we declare.. 
    ###############################################
    if (found == False) and (display_all):
        print("\nPinCode: %s ** No Avaliability at any Center **\n" % pincode)
    else:
        if (found == True):
            print("\nPinCode: %s Total available: %s" % (pincode, total_availability))



################################################################
# TBD: Iternate over pincode "range" to look for vaccination centers
################################################################
def cowin_vax_availability_iterate_pincode (pincode, vax_date, vaccine, 
                                            iterate, display_all, minage, log):
    pin = int(pincode)
   
    # If iterate option is specified, iterate to at least 125 pin codes
    # from initial given pincode
    if (iterate):
        end_pin = pin + 125
    else: 
        end_pin = pin + 1

    while (pin < end_pin):
        cowin_vax_availability_by_pincode(str(pin), vax_date, vaccine, display_all, minage, log)
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
    parser.add_argument('-v', action="store", dest="vaccine", default="Any", required=False,
                        help="Vaccine Type [CX=Covaxin, default=COVISHIELD")
    parser.add_argument('-a', action="store", dest="minage", default=0, required=False,
                        help="Vaccine Type [CX=Covaxin, default=COVISHIELD")
    parser.add_argument('-f', action='store_true', dest="display_all", required=False,
                        help="Iterate to around 125 pin codes. Uses specified pincode as starting code")
    parser.add_argument('-i', '--iterate', action='store_true', dest="iterate", required=False,
                        help="Iterate to around 125 pin codes. Uses specified pincode as starting code")
    parser.add_argument('-l', '--simulate', action='store_true', dest="log", required=False,
                        help="Enable debug logs")
    args = parser.parse_args()
    args = parser.parse_args()

    if args.vax_date == None:
        vax_date=date.today().strftime('%d-%m-%Y')
    else:
        vax_date=args.vax_date

    vaccine = args.vaccine
    ##########################################################
    # Here we just look for any Vaccine availability as the 
    # data on vaccine type is not accurate in CoWin
    ##########################################################
    print("\n======================================================================================")
    print("Checking availability for Pincode=%s Date=%s Age=%s+ Vaccine=%s" %
          (args.pincode, vax_date, args.minage, vaccine))
    print("========================================================================================")

    ###############################
    # Begin look up process...
    ###############################
    total_availability = 0
    cowin_vax_availability_iterate_pincode(args.pincode, vax_date, vaccine, 
          args.iterate, args.display_all, args.minage, args.log)

if __name__ == "__main__":
    start=time.time()
    initialize()
    elapsed = (time.time() - start)
    #print("Time elapsed is : {:.2f} seconds".format(elapsed))


