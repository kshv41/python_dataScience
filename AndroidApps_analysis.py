#!/usr/bin/env python
# coding: utf-8

# # Android apps data analysis
# In this assignment we're given a data with 10000 entries about Ratings, Genre, Reviews etc. The dataset can be found attached [AndroidApps_data](https://drive.google.com/file/d/1RCx964NxP7zpdgTyhVtWIXgX2FDnvRAe/view?usp=sharing) 

# Now let's create a **function** which enable us to explore the dataset conveniently. The function should display the first few rows and if asked should also give out the the number of rows and columns in the dataset.
# 

# In[55]:


opened_file = open('googleplaystore.csv')
from csv import reader
read_file = reader(opened_file)
android_data = list(read_file) 


# In[56]:


def explore(dataset, count_rc = False) :
    print('The following are the columns:')
    print('\n')
    
    for element in dataset[0]:
        print(element)
        print('\n')
        
    print('The first row')
    print('\n')
    
    for row in dataset[1:2]:
        print(row)
        print('\n')
        
    if count_rc :
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))


# In[57]:


explore(android_data, count_rc = True)


# There seems to be some anomaly with row 10472. Lets check it out.

# In[58]:


print(android_data[10473])


# Clearly this row has the rating column missing and shift seems to have happened for the subsequent columns. Lets delete this row.

# In[59]:


del(android_data[10473])


# In[60]:


print(len(android_data))


# The defaulter row has been deleted.

# Lets check if there are multiple entries of the same app.

# In[61]:


uniqueApp_name = []
duplicate_name = []
for app in android_data:
    name = app[0]
    if name in uniqueApp_name:
        duplicate_name.append(name)
    else :
        uniqueApp_name.append(name)
        
print(len(uniqueApp_name))


# Clearly the number of unique apps is 9659 (1 is the header row). Rest are repeated. Lets remove the repeats.Among the repeated entries, we'll choose he entry with maximum reviews. Chances of it being the latest are highest.

# In[62]:


#Creating dictionary 
unique_entries = {}
for row in android_data[1:]:
    name = row[0]
    reviews = float(row[3])
    if (name not in unique_entries) or (unique_entries[name] < reviews):
        unique_entries[name] = reviews
print(len(unique_entries))


# In[63]:


unique_dataset = []
UniqueApp_name = []
for row in android_data[1:]:
    name = row[0]
    reviews = float(row[3])
    if name not in UniqueApp_name and reviews == unique_entries[name]:
        unique_dataset.append(row)
        UniqueApp_name.append(name)
        
len(unique_dataset)


# Now since we need only english apps. Let's filter out the non english apps.

# In[64]:


def english_only(string) :
    count = 0
    for element in string :
        if ord(element) > 127 :
            count += 1  
    if count > 3 :
        return False 
    
    return True 
     


# In[65]:


englishApps_dataset = []
for app in unique_dataset :
    name = app[0]
    result = english_only(name)
    if result == True:
        englishApps_dataset.append(app) 
        
print(len(englishApps_dataset))


# Now this is final cleaned dataset and we can work on it for analysis purposes.

# In[66]:


freeApps = []
for element in englishApps_dataset:
    price = element[7]
    if price == '0':
        freeApps.append(element)
print(len(freeApps))


# Now let's try to understand the genre of the **Most** popular app. Let us understand the market first and see which genre has most apps on app store. 

# In[71]:


def gen_freq_table(dataset, index):
    genre_freq = {}
    for app in dataset:
        genre = app[index]
        if genre in genre_freq:
            genre_freq[genre] += 1
        else:
            genre_freq[genre] = 1
            
    for value in genre_freq:
        genre_freq[value] = (genre_freq[value] / len(dataset)) * 100
    return genre_freq
        

def display_table(dataset, index):
    table = gen_freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)
        
    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted: 
        print(entry[1], ':', entry[0])

display_table(freeApps, 5)


# In[68]:


list_genre = []
for app in freeApps :
    genre = app[9]
    if genre not in list_genre:
        list_genre.append(genre)
for name_genre in list_genre:
    print(name_genre)
    print('\n')


# In[89]:


genre_installs = []
entry = {}

for name in list_genre:
    n = 0 
    for app in freeApps:
        if app[9] == name:
            installs = app[5]
            installs = installs.replace('+' , '')
            installs = installs.replace(',' , '')    
            installs = float(installs)
            n = n + installs
    entry[name] = n
    rufus = ( entry[name], name)
    genre_installs.append(rufus)

genre_installs_sorted = sorted(genre_installs, reverse = True)
for element in genre_installs_sorted :
    print(element[1], ':', element[0])
    print('\n')


# # Conclusion 
# The above mentioned are the different genres in decreasing order of their installs.
