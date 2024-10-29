import polars as pl
import streamlit as st
import plotly.express as px
import folium as fl

cia_factbook = pl.read_csv(
    "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2024/2024-10-22/cia_factbook.csv", null_values="NA")

country_iso_codes = pl.DataFrame({
    "Country": [
        "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda",
        "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas",
        "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize",
        "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana",
        "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi",
        "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Central African Republic",
        "Chad", "Chile", "China", "Colombia", "Comoros", "Congo, Republic of the",
        "Congo, Democratic Republic of the", "Costa Rica", "Croatia", "Cuba",
        "Cyprus", "Czech Republic", "Denmark", "Djibouti", "Dominica",
        "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea",
        "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Fiji", "Finland",
        "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana",
        "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau",
        "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India",
        "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy",
        "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati",
        "Korea, North", "Korea, South", "Kuwait", "Kyrgyzstan", "Laos",
        "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein",
        "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia",
        "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania",
        "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco",
        "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar",
        "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand",
        "Nicaragua", "Niger", "Nigeria", "North Macedonia", "Norway",
        "Oman", "Pakistan", "Palau", "Palestine", "Panama", "Papua New Guinea",
        "Paraguay", "Peru", "Philippines", "Poland", "Portugal",
        "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis",
        "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino",
        "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia",
        "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia",
        "Solomon Islands", "Somalia", "South Africa", "South Sudan",
        "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland",
        "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand",
        "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia",
        "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine",
        "United Arab Emirates", "United Kingdom", "United States", "Uruguay",
        "Uzbekistan", "Vanuatu", "Vatican City", "Venezuela", "Vietnam",
        "Yemen", "Zambia", "Zimbabwe"
    ],
    "ISO Code": [
        "AFG", "ALB", "DZA", "AND", "AGO", "ATG",
        "ARG", "ARM", "AUS", "AUT", "AZE", "BHS",
        "BHR", "BGD", "BRB", "BLR", "BEL", "BLZ",
        "BEN", "BTN", "BOL", "BIH", "BWA",
        "BRA", "BRN", "BGR", "BFA", "BDI",
        "CPV", "KHM", "CMR", "CAN", "CAF",
        "TCD", "CHL", "CHN", "COL", "COM", "COG",
        "COD", "CRI", "HRV", "CUB", "CYP",
        "CZE", "DNK", "DJI", "DMA", "DOM",
        "ECU", "EGY", "SLV", "GNQ", "ERI",
        "EST", "SWZ", "ETH", "FJI", "FIN",
        "FRA", "GAB", "GMB", "GEO", "DEU", "GHA",
        "GRC", "GRD", "GTM", "GIN", "GNB",
        "GUY", "HTI", "HND", "HUN", "ISL", "IND",
        "IDN", "IRN", "IRQ", "IRL", "ISR", "ITA",
        "JAM", "JPN", "JOR", "KAZ", "KEN", "KIR",
        "PRK", "KOR", "KWT", "KGZ", "LAO",
        "LVA", "LBN", "LSO", "LBR", "LBY", "LIE",
        "LTU", "LUX", "MDG", "MWI", "MYS",
        "MDV", "MLI", "MLT", "MHL", "MRT",
        "MUS", "MEX", "FSM", "MDA", "MCO",
        "MNG", "MNE", "MAR", "MOZ", "MMR",
        "NAM", "NRU", "NPL", "NLD", "NZL",
        "NIC", "NER", "NGA", "MKD", "NOR",
        "OMN", "PAK", "PLW", "PSE", "PAN", "PNG",
        "PRY", "PER", "PHL", "POL", "PRT",
        "QAT", "ROU", "RUS", "RWA", "KNA",
        "LCA", "VCT", "WSM", "SMR", "STP",
        "SAU", "SEN", "SRB", "SYC", "SLE",
        "SGP", "SVK", "SVN", "SLB", "SOM",
        "ZAF", "SSD", "ESP", "LKA", "SDN",
        "SUR", "SWE", "CHE", "SYR", "TWN",
        "TJK", "TZA", "THA", "TLS", "TGO",
        "TON", "TTO", "TUN", "TUR", "TKM",
        "TUV", "UGA", "UKR", "ARE", "GBR",
        "USA", "URY", "UZB", "VUT", "VAT",
        "VEN", "VNM", "YEM", "ZMB", "ZWE"
    ]
})

cia_factbook_friendly_names = cia_factbook.rename({
    "country": "Country",
    "area": "Area (sq km)",
    "birth_rate": "Birth Rate",
    "death_rate": "Death Rate",
    "infant_mortality_rate": "Infant Mortality Rate",
    "internet_users": "Internet Users",
    "life_exp_at_birth": "Life Expectancy at Birth",
    "maternal_mortality_rate": "Maternal Mortality Rate",
    "net_migration_rate": "Net Migration Rate",
    "population": "Population",
    "population_growth_rate": "Population Growth Rate"
})

cia_factbook_friendly_names = cia_factbook_friendly_names.join(
    country_iso_codes,
    left_on="Country",
    right_on="Country",
    how="left"
)

cia_factbook_friendly_names = (cia_factbook_friendly_names
                               .with_columns((pl.col("Population") / pl.col("Area (sq km)")).alias("Population Density"))
                               .filter(pl.col("ISO Code").is_not_null())
                               .filter(pl.col("Area (sq km)") >= 700)
)

# ---------------------------------------------

numeric_columns = ["Area (sq km)", "Birth Rate", "Death Rate", "Infant Mortality Rate",
                   "Internet Users", "Life Expectancy at Birth", "Maternal Mortality Rate",
                   "Net Migration Rate", "Population", "Population Growth Rate", "Population Density"]
countries = cia_factbook_friendly_names["Country"].unique()

st.title("CIA World Factbook Visualization")
tab1, tab2, tab3 = st.tabs(
    ["Variable Comparison", "Country Comparison", "Map"])

with tab1:
    st.header("Variable Comparison")
    st.write("Select variables to compare:")

    col1, col2, col3 = st.columns(3)
    with col1:
        var1 = st.selectbox("X-Axis:", numeric_columns)
    with col2:
        var2 = st.selectbox("Y-Axis:", numeric_columns)
    with col3:
        st.write("")
        st.write("")
        log_scale = st.checkbox("Log Scale")
        
    scatterplot = px.scatter(
        cia_factbook_friendly_names,
        x=var1,
        y=var2,
        hover_name="Country",
        hover_data={var1, var2}
    )
    
    if log_scale:
        scatterplot.update_layout(
            xaxis_type="log",
            yaxis_type="log"
        )
        
    st.plotly_chart(scatterplot)

with tab2:
    st.header("Country Comparison")
    st.write("Select a metric to compare countries by:")

    var4 = st.selectbox("Comparison Metric", numeric_columns)

    top_countries = (
        cia_factbook_friendly_names
        .filter(pl.col(var4).is_not_null())
        .sort(var4, descending=True)
        .head(10)
    )
    bargraph = px.bar(top_countries, x="Country", y=var4)
    st.plotly_chart(bargraph)

with tab3:
    st.header("Map")
    st.write("Select a metric to compare countries by:")
    var5 = st.selectbox("Mapping Metric", numeric_columns)

    map = px.choropleth(
        cia_factbook_friendly_names,
        locations="ISO Code",
        color=var5,
        hover_name="Country",
        color_continuous_scale=px.colors.sequential.Plasma,
        projection="natural earth",
        title="Title",
    )

    st.plotly_chart(map)


st.expander("View data ↓").dataframe(cia_factbook_friendly_names)
