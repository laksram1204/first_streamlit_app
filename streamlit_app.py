import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError
streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omeaga 3 & Bluberry Oatmeal')
streamlit.text('🥗 Kale,Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
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
#streamlit.header('Fruityvice Fruit Advice!')
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#streamlit.text(fruityvice_response.json())

# take the json version of the request and normalize it
#fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
#streamlit.dataframe(fruityvice_normalized)

#New section to display fruityvice api response
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

streamlit.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = streamlit.text_input('what fruit would you like information about?')  
  if not fruit_choice:
    streamlit.error('Please select a fruit to get information')
  else:
    back_from_function = get_fruityvice_data(fruit_choice)        
    streamlit.dataframe(back_from_function)
    
except URLError as e:
  streamlit.error()

# my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
# my_cur = my_cnx.cursor()
# my_cur.execute("Select * from fruit_load_list")
# my_data_rows = my_cur.fetchall()
#streamlit.text("The fruit load list contains:")
streamlit.title("View Our Fruit List - Add Your Favorites!")
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("Select * from fruit_load_list")
    return my_cur.fetchall()
 # Add a button to load the fruit
if streamlit.button('Get Fruit List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  my_cnx.close()
  streamlit.dataframe(my_data_rows)
 
#do not run anything past while we troubleshoot
#streamlit.stop()

def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values ('" + new_fruit +"')")
    return "Thanks for adding "+ new_fruit

#streamlit.text(my_data_rows)
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the List:'):
                    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
                    back_from_function = insert_row_snowflake(add_my_fruit)
                    my_cnx.close()
                    streamlit.text(back_from_function)
