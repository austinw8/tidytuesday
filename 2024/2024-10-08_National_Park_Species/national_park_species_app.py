import streamlit as st
import pandas as pd
import polars as pl
import matplotlib.pyplot as plt
import numpy as np
from lets_plot import *
import plotly.express as px
import matplotlib.image as mpimg
import requests
from io import BytesIO
from PIL import Image
LetsPlot.setup_html()

# Load dataset
url = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2024/2024-10-08/most_visited_nps_species_data.csv"
species_data = pl.read_csv(url)
species_data = species_data.with_columns(
    pl.col("ParkName").str.replace(" National Park$", "", literal=False).alias("ParkName")
).with_columns(
        pl.when(pl.col("CategoryName") == "Slug/Snail").then(pl.lit("Other Invertebrates"))
        .when(pl.col("CategoryName") == "Other Non-vertebrates").then(pl.lit("Other Invertebrates"))
        .when(pl.col("CategoryName") == "Spider/Scorpion").then(pl.lit("Other Invertebrates"))
        .when(pl.col("CategoryName") == "Crab/Lobster/Shrimp").then(pl.lit("Other Invertebrates"))
        .otherwise(pl.col("CategoryName"))
        .alias("Category")
    )


# Dropdown to select park
parks = species_data["ParkName"].unique().sort() # Get a list of unique parks
st.sidebar.title("National Park Species")
selected_park = st.sidebar.selectbox("Select a National Park", parks)


# Filter data based on selected park
specific_park_data = species_data.filter(pl.col("ParkName") == selected_park)

st.title(f"Welcome to " + selected_park + " National Park!")
st.header(f"How many unique species live here?")
st.divider()

def create_box(title, count, icon):
    return f"""
    <div style='background-color: #FFFFFF; border-radius: 10px; padding: 5px; text-align: center; color: black;'>
        <p style='margin: 0; font-size: 18px;'>{title}</p>
        <div style='font-size: 20px;'>
            <img src="{icon}" alt="{title} Icon" style="width: 60px; height: 60px; vertical-align: middle;"/>
        </div>
        <p style='margin: 10px 0; text-align: center; font-weight: bold; font-size: 25px;'>{count}</p>
    </div>
    """
    
# region <Animals>
animal_list = ("Mammal", "Bird", "Fish", "Reptile", "Amphibian", "Insect")


mammals_data = specific_park_data.filter(pl.col("CategoryName") == 'Mammal')
mammals_count = specific_park_data.filter(pl.col("CategoryName") == 'Mammal').shape[0]

birds_count = specific_park_data.filter(pl.col("CategoryName") == 'Bird').shape[0]
fish_count = specific_park_data.filter(pl.col("CategoryName") == 'Fish').shape[0]
reptiles_count = specific_park_data.filter(pl.col("CategoryName") == 'Reptile').shape[0]
amphibian_count = specific_park_data.filter(pl.col("CategoryName") == 'Amphibian').shape[0]
insect_count = specific_park_data.filter(pl.col("CategoryName") == 'Insect').shape[0]

mammal_icon = "https://cdn3.iconfinder.com/data/icons/camping-icons/527/Black_Bear-512.png"
bird_icon = "https://static.vecteezy.com/system/resources/previews/041/412/999/non_2x/black-bird-icon-isolated-on-white-background-free-vector.jpg"
fish_icon = "https://static.vecteezy.com/system/resources/previews/041/413/066/non_2x/black-fish-icon-isolated-on-white-background-free-vector.jpg"
reptile_icon = "https://cdn-icons-png.flaticon.com/512/47/47371.png"
amphibian_icon = "https://static.vecteezy.com/system/resources/previews/036/175/286/original/frog-black-icon-isolated-on-white-background-free-vector.jpg"
insect_icon = "https://img.freepik.com/premium-vector/beetle-insect-icon-white-background-simple-vector-illustration_404166-1785.jpg"
graph_icons = [mammal_icon, bird_icon, fish_icon, reptile_icon, amphibian_icon, insect_icon]

st.subheader(f"Animals")


#allow for non-existand categories to be labeled "0" -------------------------------------------------------------------------
all_animals = pl.DataFrame({"CategoryName": animal_list, "Count": [0] * len(animal_list)})

animals_in_park = (species_data
                   .filter((pl.col("ParkName") == selected_park) & (pl.col("CategoryName").is_in(animal_list)))
                   .group_by("CategoryName").agg(pl.col("CategoryName").count().alias("Count"))
                   )

animals_in_park = (all_animals
                   .join(animals_in_park, on="CategoryName", how="left")
                   .with_columns(
                       pl.when(pl.col("Count_right").is_null()).then(
                           0).otherwise(pl.col("Count_right")).alias("Count")
                   )
                   .select(
                       pl.col("CategoryName"),
                       pl.col("Count").alias("Count")
                   ))


values = {
    "Bird":"#8EA163", #green
    "Fish":"#1A8FA5", #blue
    "Mammal":"#EFCF72", #yellow
    "Reptile":"#EF8C64", #orange
    "Amphibian":"#9DC9B7", #teal
    "Insect": "#D3D3D3" #grey
}

colors = [values[category] for category in animals_in_park['CategoryName']]

#animals pie chart ------------
fig, ax = plt.subplots(figsize = (3, 3), dpi = 400)
ax.pie(
    animals_in_park['Count'], 
    labels=animals_in_park['CategoryName'], 
    autopct='%1.1f%%', 
    colors=colors,
    textprops = {"fontsize": 8},
    wedgeprops={"edgecolor": "white"}
    )
ax.axis('equal') 

col1, col2, col3 = st.columns([1, 2, 1])  # Creates three columns
with col2:  # Centered column
    st.pyplot(fig)
    
# end pie chart ----------------------------

#animals bar chart ---------------------------------
#create animals dataframe
# animals_df = pl.DataFrame({
#     "CategoryName": ["Mammals", "Birds", "Fish", "Reptiles", "Amphibians", "Insects"],
#     "Count": [mammals_count, birds_count, fish_count, reptiles_count, amphibian_count, insect_count]
#     })

# animals_bar_chart, ax = plt.subplots(figsize=(6, 3), dpi=200)
# ax.bar(animals_df['CategoryName'].to_list(), animals_df['Count'].to_list(), width = 0.5, color=colors)
# ax.set_title('')
# ax.set_xlabel('')
# ax.set_ylabel('') 
# ax.tick_params(axis='both', which='both', bottom=False, left=False)
# ax.spines['top'].set_visible(False)
# ax.spines['right'].set_visible(False)
# ax.spines['left'].set_visible(False) 
# ax.spines['bottom'].set_visible(False)
# ax.set_xticks([])
# ax.set_yticks([])

# st.pyplot(animals_bar_chart)
#end animals bar chart ---------------------------------

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.markdown(create_box("Mammal", mammals_count, mammal_icon), unsafe_allow_html=True)

with col2:
    st.markdown(create_box("Bird", birds_count, bird_icon), unsafe_allow_html=True)
    
with col3:
    st.markdown(create_box("Fish", fish_count, fish_icon), unsafe_allow_html=True)
    
with col4:
    st.markdown(create_box("Reptile", reptiles_count, reptile_icon), unsafe_allow_html=True)
    
with col5:
    st.markdown(create_box("Amphibian", amphibian_count, amphibian_icon), unsafe_allow_html=True)
    
with col6:
    st.markdown(create_box("Insect", insect_count, insect_icon), unsafe_allow_html=True)

# endregion

st.divider()

# region <plants>

vascular_count = specific_park_data.filter(pl.col("CategoryName") == 'Vascular Plant').shape[0]
nonvascular_count = specific_park_data.filter(pl.col("CategoryName") == 'Non-vascular Plant').shape[0]
fungi_count = specific_park_data.filter(pl.col("CategoryName") == 'Fungi').shape[0]
bacteria_count = specific_park_data.filter(pl.col("CategoryName") == 'Bacteria').shape[0]
protozoa_count = specific_park_data.filter(pl.col("CategoryName") == 'Protozoa').shape[0]
chromista_count = specific_park_data.filter(pl.col("CategoryName") == 'Chromista').shape[0]

vascular_icon = "https://st2.depositphotos.com/3369547/11637/v/450/depositphotos_116375040-stock-illustration-tree-silhouette-icon-nature-design.jpg"
non_vascular_icon = "https://media.istockphoto.com/id/1372466271/vector/moss-lichen.jpg?s=612x612&w=0&k=20&c=wym4-QeEE1Zj6Ap6EkCIj8QQtkpxU3uLZKKyZL8dOJU="
fungi_icon = "https://cdn4.iconfinder.com/data/icons/chinese-food-2-black-fill/128/Mushroom-toadstool-fungi-mushroom-plant-wild-mushroom-oyster-mushroom-512.png"
bacteria_icon = "https://img.freepik.com/premium-vector/bacteria-icon-isolated-white-background-vector-icon-medical-apps-web_918334-256.jpg"
protozoa_icon = "https://static.thenounproject.com/png/6024340-200.png"
chromista_icon = "https://cdn.create.vista.com/api/media/small/350761562/stock-vector-virus-icon-white-background"


st.subheader(f"Plants and Other Things")

plant_other_list = ("Vascular Plant", "Non-vascular Plant", "Fungi", "Bacteria", "Protozoa", "Chromista")

plants_other_in_park = (species_data
                   .filter((pl.col("ParkName") == selected_park) & (pl.col("CategoryName").is_in(plant_other_list)))
                   .group_by("CategoryName").agg(pl.col("CategoryName").count().alias("Count"))
                   )

values_plants_others = {
    "Vascular Plant": "#EFCF72", #yellow
    "Non-vascular Plant": "#8EA163", #green
    "Fungi": "#1A8FA5", #blue
    "Bacteria": "#EF8C64", #orange
    "Protozoa": "#9DC9B7", #teal
    "Chromista": "#D3D3D3" #grey
}

colors_po = [values_plants_others[category] for category in plants_other_in_park['CategoryName']]

#animals pie chart ------------
fig2, ax_po = plt.subplots(figsize = (3, 3), dpi = 400)
ax_po.pie(
    plants_other_in_park['Count'], 
    labels=plants_other_in_park['CategoryName'], 
    autopct='%1.1f%%', 
    colors=colors_po,
    textprops = {"fontsize": 8},
    wedgeprops={"edgecolor": "white"}
    )
ax_po.axis('equal') 

col1, col2, col3 = st.columns([1, 2, 1])  # Creates three columns
with col2:  # Centered column
    st.pyplot(fig2)
    
# end pie chart ----------------------------

#bar chart ---------------------------------

#create plants and others dataframe
# plants_others_df = pl.DataFrame({
#     "CategoryName": ["Vascular Plant", "Non-vascular Plant", "Fungi", "Bacteria", "Protozoa", "Chromista"],
#     "Count": [vascular_count, nonvascular_count, fungi_count, bacteria_count, protozoa_count, chromista_count]
#     })

# plants_others_bar_chart, ax_po = plt.subplots(figsize=(6, 3), dpi=200)
# ax_po.bar(plants_others_df['CategoryName'].to_list(), plants_others_df['Count'].to_list(), width = 0.5, color=colors_po)
# ax_po.set_title('')
# ax_po.set_xlabel('')
# ax_po.set_ylabel('') 
# ax_po.tick_params(axis='both', which='both', bottom=False, left=False)
# ax_po.spines['top'].set_visible(False)
# ax_po.spines['right'].set_visible(False)
# ax_po.spines['left'].set_visible(False) 
# ax_po.spines['bottom'].set_visible(False)
# ax_po.set_xticks([])
# ax_po.set_yticks([])

# st.pyplot(plants_others_bar_chart)
#end bar chart ---------------------------------


col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.markdown(create_box("Vascular", vascular_count, vascular_icon), unsafe_allow_html=True)

with col2:
    st.markdown(create_box("Bryophytes", nonvascular_count, non_vascular_icon), unsafe_allow_html=True)
    
with col3:
    st.markdown(create_box("Fungi", fungi_count, fungi_icon), unsafe_allow_html=True)

with col4:
    st.markdown(create_box("Bacteria", bacteria_count, bacteria_icon), unsafe_allow_html=True)
    
with col5:
    st.markdown(create_box("Protozoa", protozoa_count, protozoa_icon), unsafe_allow_html=True)

with col6:
    st.markdown(create_box("Chromista", chromista_count, chromista_icon), unsafe_allow_html=True)

# endregion