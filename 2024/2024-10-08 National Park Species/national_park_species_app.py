import streamlit as st
import pandas as pd
import polars as pl

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
    <div style='background-color: #FFFFFF; border-radius: 10px; padding: 5px; text-align: center; color: black; width: 110px;'>
        <p style='margin: 0; font-size: 18px;'>{title}</p>
        <div style='font-size: 20px;'>
            <img src="{icon}" alt="{title} Icon" style="width: 60px; height: 60px; vertical-align: middle;"/>
        </div>
        <p style='margin: 10px 0; text-align: center; font-weight: bold; font-size: 25px;'>{count}</p>
    </div>
    """
    
# region <Animals>
animal_list = ("Mammal", "Bird", "Fish", "Reptile", "Amphibian", "Insect")

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

st.subheader(f"Animals")

animal_list = ("Mammal", "Bird", "Fish", "Reptile", "Amphibian", "Insect")

all_animals = pl.DataFrame({"CategoryName": animal_list, "Count": [0] * len(animal_list)})

animals_in_park = (species_data
                   .filter((pl.col("ParkName") == selected_park) & (pl.col("CategoryName").is_in(animal_list)))
                   .group_by("CategoryName").agg(pl.col("CategoryName").count().alias("Count"))
                   )

# Join the two DataFrames
animals_in_park = all_animals.join(animals_in_park, on="CategoryName", how="left")

# Fill null counts with 0
animals_in_park = animals_in_park.with_columns(
    pl.when(pl.col("Count_right").is_null()).then(0).otherwise(pl.col("Count_right")).alias("Count")
)

animals_in_park = animals_in_park.select(
    pl.col("CategoryName"),
    pl.col("Count").alias("Count")
)

import matplotlib.pyplot as plt

values = {
    "Bird":"#8EA163", 
    "Fish":"#1A8FA5", 
    "Mammal":"#EFCF72", 
    "Reptile":"#EF8C64", 
    "Amphibian":"#9DC9B7",
    "Insect": "#D3D3D3"
}

colors = [values[category] for category in animals_in_park['CategoryName']]

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


#lolipop chart ------------------------------------------------------------------------------------------------------

# import numpy as np

# categories = animals_in_park['CategoryName']
# counts = animals_in_park['Count']
# num_columns = 6
# num_categories = len(categories)

# # Set the positions for the lollipops
# y_pos = np.linspace(0, num_columns-1, num_categories)

# # Add percentage labels
# for i, count in enumerate(counts):
#     ax.text(i, count + 0.5, f'{count} ({count/sum(counts)*100:.1f}%)', ha='center', fontsize=8)

# # Streamlit column layout
# col1, col2, col3, col4, col5, col6 = st.columns(6)  # Creates six columns

# # List of columns to display the lollipop stems above
# columns = [col1, col2, col3, col4, col5, col6]

# for idx, col in enumerate(columns):
#     with col:  # Each column for displaying the lollipop
#         # Create a new figure for each column
#         fig, ax = plt.subplots(figsize=(1, 3), dpi=400)  # Narrower width for a single lollipop
        
#         # Plot only the current category's count
#         ax.vlines(0, 0, counts[idx], color='#8EA163', linewidth=2)  # Vertical line
#         ax.plot(0, counts[idx], 'o', color='#355E3B', markersize=8)  # Lollipop marker

#         ax.set_ylim(0, max(counts) + 5)  # Extend y-limits to fit label
#         ax.axis('off')  # Turn off axis

#         # Add percentage label above each lollipop
#         ax.text(0, counts[idx] + 15, f'{counts[idx]} ({counts[idx]/sum(counts)*100:.1f}%)', ha='center', fontsize=8)

#         st.pyplot(fig)


#end lolipop chart ------------------------------------------------------------------------------------------------------

# pie chart ------------
col1, col2, col3 = st.columns([1, 2, 1])  # Creates three columns

with col2:  # Centered column
    st.pyplot(fig)

# end pie chart ----------------------------

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.markdown(create_box("Mammals", mammals_count, mammal_icon), unsafe_allow_html=True)

with col2:
    st.markdown(create_box("Birds", birds_count, bird_icon), unsafe_allow_html=True)
    
with col3:
    st.markdown(create_box("Fish", fish_count, fish_icon), unsafe_allow_html=True)
    
with col4:
    st.markdown(create_box("Reptiles", reptiles_count, reptile_icon), unsafe_allow_html=True)
    
with col5:
    st.markdown(create_box("Amphibians", amphibian_count, amphibian_icon), unsafe_allow_html=True)
    
with col6:
    st.markdown(create_box("Insects", insect_count, insect_icon), unsafe_allow_html=True)

# endregion

st.divider()

# region <plants>

vascular_count = specific_park_data.filter(pl.col("CategoryName") == 'Vascular Plant').shape[0]
nonvascular_count = specific_park_data.filter(pl.col("CategoryName") == 'Non-vascular Plant').shape[0]

vascular_icon = "https://st2.depositphotos.com/3369547/11637/v/450/depositphotos_116375040-stock-illustration-tree-silhouette-icon-nature-design.jpg"
non_vascular_icon = "https://media.istockphoto.com/id/1372466271/vector/moss-lichen.jpg?s=612x612&w=0&k=20&c=wym4-QeEE1Zj6Ap6EkCIj8QQtkpxU3uLZKKyZL8dOJU="

st.subheader(f"Plants")

plant_list = ("Vascular Plant", "Non-vascular Plant")

plants_in_park = (species_data
                   .filter((pl.col("ParkName") == selected_park) & (pl.col("CategoryName").is_in(plant_list)))
                   .group_by("CategoryName").agg(pl.col("CategoryName").count().alias("Count"))
                   )

values_plants = {
    "Vascular Plant":"#8EA163", 
    "Non-vascular Plant": "#D3D3D3"
}

colors = [values_plants[category] for category in plants_in_park['CategoryName']]

fig_plants, ax = plt.subplots(figsize = (3, 3), dpi = 400)
ax.pie(
    plants_in_park['Count'], 
    labels=plants_in_park['CategoryName'], 
    autopct='%1.1f%%', 
    colors=colors,
    textprops = {"fontsize": 8},
    wedgeprops={"edgecolor": "white"}
    )
ax.axis('equal') 

col1, col2, col3 = st.columns([1, 2, 1])  # Creates three columns

with col2:  # Centered column
    st.pyplot(fig_plants)

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col3:
    st.markdown(create_box("Vascular", vascular_count, vascular_icon), unsafe_allow_html=True)

with col4:
    st.markdown(create_box("Non-Vascular", nonvascular_count, non_vascular_icon), unsafe_allow_html=True)

# endregion

st.divider()

# region <misc>

fungi_count = specific_park_data.filter(pl.col("CategoryName") == 'Fungi').shape[0]
bacteria_count = specific_park_data.filter(pl.col("CategoryName") == 'Bacteria').shape[0]
protozoa_count = specific_park_data.filter(pl.col("CategoryName") == 'Protozoa').shape[0]
chromista_count = specific_park_data.filter(pl.col("CategoryName") == 'Chromista').shape[0]

fungi_icon = "https://cdn4.iconfinder.com/data/icons/chinese-food-2-black-fill/128/Mushroom-toadstool-fungi-mushroom-plant-wild-mushroom-oyster-mushroom-512.png"
bacteria_icon = "https://img.freepik.com/premium-vector/bacteria-icon-isolated-white-background-vector-icon-medical-apps-web_918334-256.jpg"
protozoa_icon = "https://static.thenounproject.com/png/6024340-200.png"
chromista_icon = "https://cdn.create.vista.com/api/media/small/350761562/stock-vector-virus-icon-white-background"

st.subheader(f"Other")

other_list = ("Fungi", "Bacteria", "Protozoa", "Chromista")

other_in_park = (species_data
                   .filter((pl.col("ParkName") == selected_park) & (pl.col("CategoryName").is_in(other_list)))
                   .group_by("CategoryName").agg(pl.col("CategoryName").count().alias("Count"))
                   )

values_other = {
    "Fungi":"#8EA163", 
    "Bacteria":"#1A8FA5", 
    "Protozoa":"#EFCF72", 
    "Chromista": "#D3D3D3"
}

colors = [values_other[category] for category in other_in_park['CategoryName']]

fig_other, ax = plt.subplots(figsize = (3, 3), dpi = 400)
ax.pie(
    other_in_park['Count'], 
    labels=other_in_park['CategoryName'], 
    autopct='%1.1f%%', 
    colors=colors,
    textprops = {"fontsize": 8},
    wedgeprops={"edgecolor": "white"}
    )
ax.axis('equal') 

col1, col2, col3 = st.columns([1, 2, 1])  # Creates three columns

with col2:  # Centered column
    st.pyplot(fig_other)

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col2:
    st.markdown(create_box("Fungi", fungi_count, fungi_icon), unsafe_allow_html=True)

with col3:
    st.markdown(create_box("Bacteria", bacteria_count, bacteria_icon), unsafe_allow_html=True)
    
with col4:
    st.markdown(create_box("Protozoa", protozoa_count, protozoa_icon), unsafe_allow_html=True)

with col5:
    st.markdown(create_box("Chromista", chromista_count, chromista_icon), unsafe_allow_html=True)

# endregion