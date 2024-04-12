import streamlit as st
import pandas as pd
import numpy as np 
import plotly.express as px

st.header("Market of Used Cars Data")
st.write('Filter the data below to see certain information relating to different car manufacturers.')

df = pd.read_csv('vehicles_us.csv')

# Converting the data type to str and the value of 1.0 = yes and Nan = no
conversion_dict = {1.0: 'yes', None: 'no'}
df['is_4wd'] = df['is_4wd'].map(conversion_dict)

# Removing missing values in the model_year column & Changing the data type to int
df.dropna(subset=['model_year'], inplace=True)
df['model_year'] = df['model_year'].astype(int)


# Changing the data type of the odometer column as well as filling missing values with 0
df['odometer'] = df['odometer'].fillna(0)
df['odometer'] = df['odometer'].astype(int)

# Filling missing values in the paint_color column with 'not found'
df['paint_color'] = df['paint_color'].fillna('not found')

# Filling missing values in the cylinders column with 0
df['cylinders'] = df['cylinders'].fillna(0)

# Changing the data type of the cylinders column
df['cylinders'] = df['cylinders'].astype(int)

#Creating the drop down selection 
manufacturer_choice = df['model'].unique()

selected_menu = st.selectbox('Model Name', manufacturer_choice)

df_filtered = df[df.model == selected_menu]

df_filtered

# Plotting histograms and graphs

st.header('Price Analysis')
st.write("Lets see what influences price the most. We will check how price distribution differs depending on fuel type, transmission, and vehicle type.")

list_for_hist = ['fuel', 'transmission', 'type']

selected_type = st.selectbox('Split for price distribution', list_for_hist)

fig1 = px.histogram(df, x="price",color = selected_type)
fig1.update_layout(title= "<b> Split of price by {}</b>".format(selected_type))
st.plotly_chart(fig1)

def age_category(x):
    if x<5: return '<5'
    elif x>=5 and x<10: return '5-10'
    elif x>=10 and x<20: return '10-20'
    else: return '>20'

df['age'] = 2024 - df['model_year']
df['age_category'] = df['age'].apply(age_category)


list_for_scatter = ['odometer', 'cylinders', 'condition']
choice_for_scatter = st.selectbox('Price dependency on', list_for_scatter)

fig2 = px.scatter(df, x="price", y=choice_for_scatter, color="age_category", hover_data=['model_year'])
fig2.update_layout(title="<b> Price vs {}</b>".format(choice_for_scatter))
st.plotly_chart(fig2) 
