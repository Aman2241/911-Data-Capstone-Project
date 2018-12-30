
# coding: utf-8

# # 911 Calls Capstone Project 

# ## Data and Setup

# ____
# ** Import numpy and pandas **

# In[1]:


import numpy as np
import pandas as pd


# ** Import visualization libraries and set %matplotlib inline. **

# In[2]:


import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
get_ipython().run_line_magic('matplotlib', 'inline')


# ** Read in the csv file as a dataframe called df **

# In[6]:


df = pd.read_csv('/home/aman/Data Capstone Project/911.csv')


# ** Check the info() of the df **

# In[7]:


df.info()


# ** Check the head of df **

# In[8]:


df.head(3)


# # Basic Questions
# 

# ** What are the top 5 zipcodes for 911 calls? **

# In[9]:


df['zip'].value_counts().head(5)


# ** What are the top 5 townships (twp) for 911 calls? **

# In[10]:


df['twp'].value_counts().head(5)


# ** Take a look at the 'title' column, how many unique title codes are there? **

# In[11]:


df['title'].nunique()


# ## Creating new features

# In[12]:


df['Reason'] = df['title'].apply(lambda title: title.split(':')[0])


# ** What is the most common Reason for a 911 call based off of this new column? **

# In[13]:


df['Reason'].value_counts()


# ** Now use seaborn to create a countplot of 911 calls by Reason. **

# In[14]:


sns.countplot(x='Reason',data=df,palette='viridis')


# ___
# ** Now let us begin to focus on time information. What is the data type of the objects in the timeStamp column? **

# In[15]:


type(df['timeStamp'].iloc[0])


# ** You should have seen that these timestamps are still strings. Use [pd.to_datetime](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.to_datetime.html) to convert the column from strings to DateTime objects. **

# In[16]:


df['timeStamp'] = pd.to_datetime(df['timeStamp'])


# ** You can now grab specific attributes from a Datetime object by calling them. For example:**
# 
#     time = df['timeStamp'].iloc[0]
#     time.hour
# 
# 

# In[17]:


df['Hour'] = df['timeStamp'].apply(lambda time: time.hour)
df['Month'] = df['timeStamp'].apply(lambda time: time.month)
df['Day of Week'] = df['timeStamp'].apply(lambda time: time.dayofweek)


# ** Notice how the Day of Week is an integer 0-6. Use the .map() with this dictionary to map the actual string names to the day of the week: **
# 
#     dmap = {0:'Mon',1:'Tue',2:'Wed',3:'Thu',4:'Fri',5:'Sat',6:'Sun'}

# In[18]:


dmap = {0:'Mon',1:'Tue',2:'Wed',3:'Thu',4:'Fri',5:'Sat',6:'Sun'}


# In[19]:


df['Day of Week'] = df['Day of Week'].map(dmap)


# ** Now use seaborn to create a countplot of the Day of Week column with the hue based off of the Reason column. **

# In[20]:


sns.countplot(x='Day of Week',data=df,hue='Reason',palette='viridis')

# To relocate the legend
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)


# ** Now do the same for Month:**

# In[21]:


sns.countplot(x='Month',data=df,hue='Reason',palette='viridis')

# To relocate the legend
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)


# ** Did you notice something strange about the Plot? **

# In[22]:


# It is missing some months! 9,10, and 11 are not there.


# #Some months are missing

# In[23]:


byMonth = df.groupby('Month').count()
byMonth.head()


# ** Now create a simple plot off of the dataframe indicating the count of calls per month. **

# In[24]:


# Could be any column
byMonth['twp'].plot()


# ** Now see if you can use seaborn's lmplot() to create a linear fit on the number of calls per month. Keep in mind you may need to reset the index to a column. **

# In[25]:


sns.lmplot(x='Month',y='twp',data=byMonth.reset_index())


# **Create a new column called 'Date' that contains the date from the timeStamp column. You'll need to use apply along with the .date() method. ** 

# In[26]:


df['Date']=df['timeStamp'].apply(lambda t: t.date())


# ** Now groupby this Date column with the count() aggregate and create a plot of counts of 911 calls.**

# In[27]:


df.groupby('Date').count()['twp'].plot()
plt.tight_layout()


# ** Now recreate this plot but create 3 separate plots with each plot representing a Reason for the 911 call**

# In[28]:


df[df['Reason']=='Traffic'].groupby('Date').count()['twp'].plot()
plt.title('Traffic')
plt.tight_layout()


# In[29]:


df[df['Reason']=='Fire'].groupby('Date').count()['twp'].plot()
plt.title('Fire')
plt.tight_layout()


# In[30]:


df[df['Reason']=='EMS'].groupby('Date').count()['twp'].plot()
plt.title('EMS')
plt.tight_layout()


# In[31]:


dayHour = df.groupby(by=['Day of Week','Hour']).count()['Reason'].unstack()
dayHour.head()


# ** Now create a HeatMap using this new DataFrame. **

# In[32]:


plt.figure(figsize=(12,6))
sns.heatmap(dayHour,cmap='viridis')


# ** Now create a clustermap using this DataFrame. **

# In[33]:


sns.clustermap(dayHour,cmap='viridis')


# ** Now repeat these same plots and operations, for a DataFrame that shows the Month as the column. **

# In[34]:


dayMonth = df.groupby(by=['Day of Week','Month']).count()['Reason'].unstack()
dayMonth.head()


# In[35]:


plt.figure(figsize=(12,6))
sns.heatmap(dayMonth,cmap='viridis')


# In[36]:


sns.clustermap(dayMonth,cmap='viridis')

