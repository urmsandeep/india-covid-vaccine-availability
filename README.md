# India Covid Vaccine availability finder

This python script helps find vaccine availability at various center given Pincode and date.

It uses COWIN API in the backend to source vaccination centers, eligibility age, vaccine type and Availability count.

# Usage

usage: cowin_vax_avail_check.py [-h] -p PINCODE [-d VAX_DATE] 
     
India Cowin Vax Availability Status

optional arguments:
  -h, --help      show this help message and exit
  -p PINCODE      Pin Code
  -d VAX_DATE     Date for Vaccine Availability in dd-mm-yyyy format,
                  default=today's date

# Restrictions
1. Filtering of availability based on vaccine type not supported as the vaccine type date sourced from COWIN API is not accurate.
2. With COWIN API many centers do not have the 'Vaccine' type updated, for most centers, vaccine type is blank.

# Sample Usage

(1) Pincode: 560029 Date: 04-05-2021

> python cowin_vax_avail_check.py -p 560029 -d 04-05-2021

```
======================================================================================
Checking availability for Pincode=560029 Date=04-05-2021 Vaccine=Any
========================================================================================

PinCode: 560029 | Center: NIMHANS Hospitals         | MinAge: 45 | Availability: 0   | Vaccine: 

** No Avaliability at any Center **
```

(2) Pincode: 560078 Date: 04-05-2021

> python cowin_vax_avail_check.py -p 560078 -d 04-05-2021

```
======================================================================================
Checking availability for Pincode=560078 Date=04-05-2021 Vaccine=Any
========================================================================================

PinCode: 560078 | Center: Manipal Clinic            | MinAge: 18 | Availability: 0   | Vaccine: COVAXIN

** No Avaliability at any Center **

```

(3) Pincode: 125033 Date: 04-05-2021

> python cowin_vax_avail_check.py -p 125033 -d 04-05-2021

```
======================================================================================
Checking availability for Pincode=125033 Date=04-05-2021 Vaccine=Any
========================================================================================

PinCode: 125033 | Center: Subcenter Dhani Pirawali  | MinAge: 45 | Availability: 83  | Vaccine: 

PinCode: 125033 | Center: Subcenter Dhani Pirawali  | MinAge: 45 | Availability: 97  | Vaccine: 

PinCode: 125033 | Center: Subcenter Dhani Pirawali  | MinAge: 45 | Availability: 100 | Vaccine: 

PinCode: 125033 | Center: Subcenter Dhani Pirawali  | MinAge: 45 | Availability: 95  | Vaccine: 

PinCode: 125033 | Center: Subcenter Dhana Khurd     | MinAge: 45 | Availability: 98  | Vaccine: 

PinCode: 125033 | Center: Subcenter Dhana Khurd     | MinAge: 45 | Availability: 100 | Vaccine: 

PinCode: 125033 | Center: Subcenter Dhana Khurd     | MinAge: 45 | Availability: 100 | Vaccine: 

PinCode: 125033 | Center: Subcenter Dhana Khurd     | MinAge: 45 | Availability: 100 | Vaccine: 

PinCode: 125033 | Center: Subcenter Kharkhari       | MinAge: 45 | Availability: 43  | Vaccine: 

PinCode: 125033 | Center: Subcenter Fransi          | MinAge: 45 | Availability: 99  | Vaccine: 

PinCode: 125033 | Center: Subcenter Fransi          | MinAge: 45 | Availability: 100 | Vaccine: 

PinCode: 125033 | Center: Subcenter Fransi          | MinAge: 45 | Availability: 100 | Vaccine: 

PinCode: 125033 | Center: Subcenter Fransi          | MinAge: 45 | Availability: 100 | Vaccine: 

PinCode: 125033 | Center: Subcenter Dhana Kalan     | MinAge: 45 | Availability: 87  | Vaccine: 
```

(4) Pincode: 524002 Date: 04-05-2021

> python cowin_vax_avail_check.py -p 524002 -d 04-05-2021

```
======================================================================================
Checking availability for Pincode=524002 Date=04-05-2021 Vaccine=Any
========================================================================================

PinCode: 524002 | Center: Allipuram PHC CVC         | MinAge: 45 | Availability: 0   | Vaccine: 

PinCode: 524002 | Center: Allipuram PHC CVC         | MinAge: 45 | Availability: 0   | Vaccine: 

PinCode: 524002 | Center: Allipuram PHC CVC         | MinAge: 45 | Availability: 0   | Vaccine: 

PinCode: 524002 | Center: Allipuram PHC CVC         | MinAge: 45 | Availability: 0   | Vaccine: 

PinCode: 524002 | Center: NTR Nagar EUPHC CVC       | MinAge: 45 | Availability: 0   | Vaccine: 

PinCode: 524002 | Center: NTR Nagar EUPHC CVC       | MinAge: 45 | Availability: 0   | Vaccine: 

PinCode: 524002 | Center: NTR Nagar EUPHC CVC       | MinAge: 45 | Availability: 0   | Vaccine: 

PinCode: 524002 | Center: NTR Nagar EUPHC CVC       | MinAge: 45 | Availability: 0   | Vaccine: 

PinCode: 524002 | Center: NTR Nagar EUPHC CVC       | MinAge: 45 | Availability: 0   | Vaccine: 

PinCode: 524002 | Center: NTR Nagar EUPHC CVC       | MinAge: 45 | Availability: 0   | Vaccine: 

PinCode: 524002 | Center: NTR Nagar EUPHC CVC       | MinAge: 45 | Availability: 0   | Vaccine: 

PinCode: 524002 | Center: Koduru PHC CVC            | MinAge: 45 | Availability: 0   | Vaccine: 

PinCode: 524002 | Center: Koduru PHC CVC            | MinAge: 45 | Availability: 0   | Vaccine: 

```
