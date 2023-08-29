"""
The National Weather Service has gone down, and pilots don't know if they can legally fly their airplanes.
Due to the system outages pilots will only be allowed to fly using Visual Flight Rules (VFR.)

Visual Flight Rules are defined as:
Greater than 5SM (Statue Miles) of Visibility. Visibility columns may come in two formats
    - 4 digits, representing KM, which must be greater than or equal to 8000KM
    - strings ending in SM, in which case an integer will immediately preceed the value, which must be greater than or equal to 5SM
Cloud Ceilings Above 3000ft
    - If the cloud ceiling is reported as CLR, FEW, or SCT, the cloud ceiling are OK for VFR.
    - If the ceiling is reported as BKN or OVC, you must check if the value is greater than or equal to 3000ft (shown as "30" representing 100s of feet.)

You have a copy of the METAR weather observations for all of the airports in the United States saved in '/home/coderpad/data/metars.csv'.  
An example record follows, though the reported columns may vary greatly due to different equipment at each airport.
"KSMO 220651Z AUTO 19006KT 10SM OVC010 17/14 A2997 RMK AO2 SLP146 T01720144"

YOUR TASK:
Search for and return a count of as many airports that you can prove are using VFR.

"""
import re
vfr_airports_count = 0

with open('/home/coderpad/data/metars.csv', 'r') as csvfile:
    csv_reader = csv.reader(csvfile)  # iterator

    for row in csv_reader:    
        # "KSMO 220651Z AUTO 19006KT 10SM OVC010 17/14 A2997 RMK AO2 SLP146 T01720144"
        visibility_match = re.search(r'(\b\d{4})\b|\b\d+SM\b', row)  # search
        cloud_ceiling_match = re.search(r'\b(CLR|FEW|SCT|BKN|OVC)(\d+)?\b', row)  
        
        if visibility_match and cloud_ceiling_match:
            visibility = visibility_match.group()  # Match object
            cloud_ceiling = cloud_ceiling_match.group()
            
            if is_vfr_compliant(visibility, cloud_ceiling):
                vfr_airports_count += 1

print("Number of VFR-compliant airports:", vfr_airports_count)

def is_vfr_compliant(visibility, cloud_ceiling):
    if visibility.endswith('SM'):
        if int(visibility[:-2]) >= 5:
            return True
    else:
        visibility_km = int(visibility)
        if visibility_km >= 8000:
            return True
        
    cloud_ceiling_match = re.match(r'(\w+)(\d+)?', cloud_ceiling)  # match
    cloud_cover = cloud_ceiling_match.group(1)    
    cloud_height = cloud_ceiling_match.group(2)
    if cloud_cover in ['CLR', 'FEW', 'SCT']:
        return True
    elif cloud_cover in ['BKN', 'OVC']:
        if int(cloud_height) * 100 >= 3000:
            return True
        
    return False
