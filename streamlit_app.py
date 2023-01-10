import streamlit
streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omeaga 3 & Bluberry Oatmeal')
streamlit.text('🥗 Kale,Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
import pandas
import requests
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
#let us put a picklist so they can pick the fruit they want to include
#streamlit.multiselect("Pick some fruits:",list(my_fruit_list.index),['Avocado','Strawberries'])
#streamlit.dataframe(my_fruit_list)
fruits_selected = streamlit.multiselect("Pick some fruits:",list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
#display table onthe page 
streamlit.dataframe(fruits_to_show)
#Old section to display response 200
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#streamlit.text(fruityvice_response)

#New section to display fruityvice api response
streamlit.header('Fruityvice Fruit Advice!')
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
streamlit.text(fruityvice_response.json())

# take the json version of the request and normalize it
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
streamlit.dataframe(fruityvice_normalized)
