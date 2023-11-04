# VFR
```
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
```
```py
import re
vfr_airports_count = 0

with open('/home/coderpad/data/metars.csv', 'r') as csvfile:
    csv_reader = csv.reader(csvfile)    # iterator

    for row in csv_reader:    
        # "KSMO 220651Z AUTO 19006KT 10SM OVC010 17/14 A2997 RMK AO2 SLP146 T01720144"
        visibility_match = re.search(r'(\b\d{4})\b|\b\d+SM\b', row)    # search
        cloud_ceiling_match = re.search(r'\b(CLR|FEW|SCT|BKN|OVC)(\d+)?\b', row)  
        
        if visibility_match and cloud_ceiling_match:
            visibility = visibility_match.group()    
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
        
    cloud_ceiling_match = re.match(r'([A-Za-z]+)(\d+)?', cloud_ceiling)    # match
    cloud_cover = cloud_ceiling_match.group(1)    
    cloud_height = cloud_ceiling_match.group(2)
    if cloud_cover in ['CLR', 'FEW', 'SCT']:
        return True
    elif cloud_cover in ['BKN', 'OVC']:
        if int(cloud_height) * 100 >= 3000:
            return True
        
    return False
```

# log file 
```
192.168.1.1 - - [01/Nov/2023:10:30:45 +0000] "GET /home HTTP/1.1" 200 1234
192.168.1.2 - - [01/Nov/2023:10:31:15 +0000] "GET /product?id=123 HTTP/1.1" 404 567
192.168.1.3 - - [01/Nov/2023:10:32:30 +0000] "POST /login HTTP/1.1" 200 890
```
```py
import pandas as pd
import re

columns = ["ip_address", "timestamp", "request_method", "http_status", "bytes_sent"]
df = pd.DataFrame(columns=columns)

log_pattern = r'(\S+) - - \[(.*?)\] "(.*?)" (\d+) (\d+)'
with open("sample_log.txt", "r") as file:
    for line in file:
        match = re.match(log_pattern, line)    # match
        if match:
            data = list(match.groups())
            df = df.append(dict(zip(columns, data)), ignore_index=True)

df["timestamp"] = pd.to_datetime(df["timestamp"], format="%d/%b/%Y:%H:%M:%S %z")
print(df)

```

# regex
```py
import re
# match
pattern = r'\d+'
text = "123abc456"
match_obj = re.match(pattern, text)
print(match_obj.group())

# search
pattern = r'\d+'
text = "abc123def456"
match_obj = re.search(pattern, text)
print(match_obj.group())

# findall
pattern = r'\d+'
text = "abc123def456"
matches = re.findall(pattern, text)
print(matches)

```

```py
# patterns
r'(\b\d{4})\b|\b\d+SM\b'    
r'\b(CLR|FEW|SCT|BKN|OVC)(\d+)?\b'    # `?` makes the preceding group optional
r'([A-Za-z]+)(\d+)?'
r'(\S+) - - \[(.*?)\] "(.*?)" (\d+) (\d+)'    # `\S` matches any non-whitespace character `(.*?)` matches any sequence of characters

```


