# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session # only work with StreamLit in Snowflake so need to be removed...
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

#option = st.selectbox(
#    "What is your favorite fruit?",
#    ("Banana", "Strawberries", "Peaches"),
#)
#st.write("You favorite fruit is:", option)

import streamlit as st

name_on_order = st.text_input('Name on Smoothie:')
st.write("The name on on your Smoothie will be:", name_on_order)

#session = get_active_session() # only work with StreamLit in Snowflake so need to be removed...
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# shows the dataframe contents on the page.
#st.dataframe(data=my_dataframe, use_container_width=True) 

# Do multiselect and return selected items as a LIST
ingredients_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe, max_selections=5)

if ingredients_list:
    st.write(ingredients_list)
    #st.text(ingredients_list)

    ingredients_string = ''

    # To display smoothefroot nutrition information
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        #st.text(smoothiefroot_response.json()) #Expose/Show the JSON Data Inside the Response Object
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True) #display JSON data in a Dataframe

    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order +  """')"""

    st.write(my_insert_stmt)
    #st.stop()
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")
        
