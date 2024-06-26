#!/usr/bin/env python
# coding: utf-8

# ## Data Cleaning Task Procedure 
# 
# 01. Load the Data: 
# 02. Inspect the Data: 
# 03. Handle Missing Values: 
# 04. Remove Duplicates:  
# 05. Correct Email Formats:
# 06. Clean Name Fields:
# 07. Standardise Date Formats:
# 08. Correct Department Names:
# 09. Handle Salary Noise:
# 10. Save the cleaned dataset as `cleaned_dataset.csv`.

# In[1]:


#01
import pandas as pd

df=pd.read_csv('messy_data.csv')
df.head()


# In[2]:


#02
df.info()
cat_col = [col for col in df.columns if df[col].dtype == 'object'] 
print('Categorical columns :',cat_col) 
num_col = [col for col in df.columns if df[col].dtype != 'object'] 
print('Numerical columns :',num_col)


# In[3]:


#03
missing_values = df.isnull().sum()
print('MISSING VALUES BEFORE REMOVING ROWS:\n', missing_values)


# In[4]:


#03-handling categorical column (Correct Department Names)
print('VALUES COUNT IN DEPARTMENT COLUMN:\n', df['Department'].value_counts())
departments = {
    'engineering': 'Engineering',
    'hr': 'HR',
    'support': 'Support',
    'sales': 'Sales',
    'marketing': 'Marketing'
}

def correct_department(dep
    if isinstance(dept, str):
        dept = dept.lower()
        for key in departments:
            if dept.startswith(key):
                return departments[key]
    return dept

df['Department'] = df['Department'].apply(correct_department)

df.to_csv('messy_data.csv', index=False)

print('VALUES COUNT IN DEPARTMENT COLUMN AFTER HANDLING:\n', df['Department'].value_counts())


# In[5]:


#03-handling categorical column
print('UNIQUE NUMBER OF VALUES WITHIN EACH COLUMN :\n', df[cat_col].nunique())

df['Department'] = df['Department'].fillna('Unknown')
df['Name'] = df['Name'].fillna('Unknown')
df['Email'] = df['Email'].fillna('Unknown')
df['Join Date'] = df['Join Date'].fillna('Unknown')

df = df[df['Name'] != 'Unknown']
df = df[df['Name'] != 'unknown']

df = df[df['Email'] != 'Unknown']
df = df[df['Join Date'] != 'Unknown']
df = df[df['Department'] != 'Unknown']

missing_values = df.isnull().sum()
print('MISSING VALUES AFTER REMOVING ROWS (CATEGORICAL):\n', missing_values)


# In[6]:


#03-handling numerical column
df = df.rename(columns={'Unnamed: 0': 'UNNECESSARY'})
df = df.drop(columns=['UNNECESSARY'])
df['Age'].fillna(df['Age'].median(), inplace=True)
department_median = df.groupby('Department')['Salary'].median()

def fill_missing_salary(row):
    if pd.isnull(row['Salary']):
        department = row['Department']
        if department in department_median:
            return department_median[department]
    return row['Salary']

df['Salary'] = df.apply(fill_missing_salary, axis=1)
# Optionally, fill remaining missing salaries with overall median
overall_median_salary = df['Salary'].median()
df['Salary'].fillna(overall_median_salary, inplace=True)
df.to_csv('messy_data.csv', index=False)

missing_values = df.isnull().sum()
print(missing_values)
print('MISSING VALUES AFTER REMOVING ROWS (NUMERICAL):\n', missing_values)

print('RESULT STATUS:\n')
df.info()


# In[7]:


#04
df = df.drop_duplicates(subset=['ID', 'Name', 'Email', 'Join Date', 'Department'])
df.to_csv('messy_data.csv', index=False)
print('RESULT STATUS AFTER DUPLICATE REMOVAL:\n')
df.info()


# In[8]:


#05
import re

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

valid_email_mask = df['Email'].apply(is_valid_email)
df = df[valid_email_mask]
#df.to_csv('messy_data.csv', index=False)


# In[9]:


#06
def clean_name(name):
    noise_words = ['Mr.', 'Ms.', 'Mrs.', 'Dr.']
    for word in noise_words:
        name = name.replace(word, '')
    name = name.strip()
    name = name.title()
    return name
df['Name'] = df['Name'].apply(clean_name)


# In[10]:


df.info()


# In[11]:


#07
date_counts = df['Join Date'].apply(lambda x: pd.to_datetime(x, errors='coerce')).value_counts()
df['Join Date'] = pd.to_datetime(df['Join Date'], errors='coerce').dt.strftime('%Y-%m-%d')

df['Join Date'].fillna('Unknown', inplace=True)  # Example: Replace missing values with 'Unknown'


# In[12]:


df.info()


# #08
# #UNDER: 03-handling categorical column (Correct Department Names)

# In[13]:


#09
#salary noise handling partialy done during missing value calculation  (calculated according to the 'DEPARTMENT' median salary)
def clean_salary(salary):

    if isinstance(salary, float) and str(salary).startswith('.'):
        return int(salary)
    
    if isinstance(salary, float):
        return round(salary)
    
    min_salary = 30000
    max_salary = 200000
    
    if salary < min_salary:
        return min_salary
    elif salary > max_salary:
        return max_salary
    
    return salary

df['Salary'] = df['Salary'].apply(clean_salary)


# In[14]:


#10
cleaned_file_path = 'cleaned_dataset.csv'
df.to_csv(cleaned_file_path, index=False)

print(f"Cleaned dataset saved to '{cleaned_file_path}'")

