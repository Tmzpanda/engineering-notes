import pandas as pd    

# create df
data = [["James","","Smith",30,"M",60000], 
        ["Michael","Rose","",50,"M",70000], 
        ["Robert","","Williams",42,"",400000], 
        ["Maria","Anne","Jones",38,"F",500000], 
        ["Jen","Mary","Brown",45,None,0]] 
columns=['First Name','Middle Name','Last Name','Age','Gender','Salary']
pandasDF=pd.DataFrame(data=data, columns=columns) 

# transform
df.columns = df.columns.str.strip()
df['col'] = df['col'].apply(json.dumps)

# 
