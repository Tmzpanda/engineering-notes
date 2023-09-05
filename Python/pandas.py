import pandas as pd    
# **************************** Create ************************************************* #
# create df from list
data = [["James","Smith",30,"M"], 
        ["Michael","Rose",50,"M"], 
        ["Robert","Williams",42,""], 
        ["Maria","Jones",38,"F"], 
        ["Jen","Brown",45,None]
       ] 
columns = ['First Name','Last Name','Age','Gender']
df = pd.DataFrame(data=data, columns=columns) 

# create df from dictionary
punch_records = "08:33:in(Second Door),08:35:(Second Door),08:37:(Main Door),09:04:out(Second Door),09:09:in(Second Door),09:15:out(Second Door),09:15:(Second Door),09:18:(Second Door),09:52:in(Second Door),09:54:(Second Door),10:00:out(Main Door),16:34:in(Second Door),19:58:out(Main Door)"
punch_list = punch_records.split(',')

punch_in_list = []
punch_out_list = []

for punch in punch_list:
    time_type = punch.split(':')
    time = time_type[0] + ':' + time_type[1]
    punch_type = time_type[2]
    
    if punch_type.startswith('in'):
        punch_in_list.append(time)
    elif punch_type.startswith('out'):
        punch_out_list.append(time)

data = {'name': 'John Sherrif', 'punch_in': punch_in_list, 'punch_out': punch_out_list}
df = pd.DataFrame(data)


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

# window function
df['SecondHighestSalary'] = df.groupby('Department')['Salary'].rank(method='max', ascending=False)
second_highest_salaries = df[df['SecondHighestSalary'] == 2][['Department', 'Salary']]





