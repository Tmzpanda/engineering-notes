import pandas as pd    
# **************************** Create ************************************************* #
# create df
data = [["James","Smith",30,"M"], 
        ["Michael","Rose",50,"M"], 
        ["Robert","Williams",42,""], 
        ["Maria","Jones",38,"F"], 
        ["Jen","Brown",45,None]
       ] 
columns = ['First Name','Last Name','Age','Gender']
df = pd.DataFrame(data=data, columns=columns) 

# read csv into df
df = pd.read_csv('filename.csv')

# **************************** Clean *************************************************** #

# trim the spaces from the column names 
df.columns = df.columns.str.strip()

# trim the spaces from the column values 
df = df.apply(lambda x: x.str.strip())




# **************************** Tranform ************************************************ #
# convert column values to json
df['col'] = df['col'].apply(json.dumps)

# extract info from raw column and add a new column
df['visibility'] = df['raw'].str.extract(r'(\d{4})|\d+SM\b')
df['cloud_ceiling'] = df['raw'].str.extract(r'\b(CLR|FEW|SCT|BKN|OVC)(\d+)?\b')

# apply custom function to each row of df
df['vfr_compliant'] = df.apply(lambda row: is_vfr_compliant(row['visibility'], row['cloud_ceiling']), axis=1)        



# **************************** Aggregate *********************************************** #
# group by
highest_salaries = df.groupby('department')['salary'].max()






