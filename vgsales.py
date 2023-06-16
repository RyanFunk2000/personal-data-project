# %%
# Import modules
import pandas as pd
import numpy as np
import altair as alt

# %%
# Convert data from csv into pandas dataframe.
vgdata = pd.read_csv('vgsales.csv')
print(vgdata.to_markdown(index=False))

# %%
# Q1: Which console manufacturer (Nintendo/Sony/Microsoft/Other) has the greater overall software sales when all their platforms are combined?
# Filter data to only have platform and total sales columns
vgdata_Sales = vgdata.filter(['Platform', 'Global_Sales'])

# Return rows that contain Nintendo's platforms
platforms_Nintendo = ['NES', 'GB', 'SNES', 'N64', 'GC', 'GBA', 'DS', 'Wii', '3DS', 'Wii', 'WiiU']
vgdata_Nintendo = vgdata_Sales[
    vgdata_Sales['Platform']
    .isin(platforms_Nintendo)
]

# Return rows that contain Sony's platforms
platforms_Sony = ['PS', 'PS2', 'PSP', 'PS3', 'PSV', 'PS4']
vgdata_Sony = vgdata_Sales[
    vgdata_Sales['Platform']
    .isin(platforms_Sony)
]

# Return rows that contain Microsoft's platforms
platforms_Microsoft = ['XB', 'X360', 'XOne']
vgdata_Microsoft = vgdata_Sales[
    vgdata_Sales['Platform']
    .isin(platforms_Microsoft)
]

# Return remaining rows that don't contain platforms from major companies
vgdata_Other = vgdata_Sales[
    ~vgdata_Sales['Platform']
    .isin(platforms_Nintendo + platforms_Sony + platforms_Microsoft)
]

# Create new dataframe that sums sales data and places them with correlated company
company_Data = pd.DataFrame(
    {'Company': ['Nintendo', 'Sony', 'Microsoft', 'Other'],
    'Sales': [vgdata_Nintendo['Global_Sales'].sum(),
                    vgdata_Sony['Global_Sales'].sum(),
                    vgdata_Microsoft['Global_Sales'].sum(),
                    vgdata_Other['Global_Sales'].sum()]}
)
print(company_Data.to_markdown(index=False))
# %%
# Create and save altair chart of company data as png
company_Chart = (alt.Chart(company_Data, title = "Sony has accumulated more game sales in their history")
    .encode(
        x = alt.X("Sales",
            title = "Total Sales (by million)"),
        y = alt.Y("Company", sort='-x'),
            color = alt.Color('Company',
                scale = alt.Scale(domain=company_Data.sort_values(['Sales'])['Company'].tolist(), range=['grey', 'green', 'red', 'blue']),
                legend=None),
    )
    .properties(
        height=200,
        width=300
    )
    .mark_bar()
)

company_Chart.save('altair_viz_1.png')

# %%
# Q2: How does region affect how games sell by their genre?
# Filter data to only have genre and regional sales columns, return sum of sales for each genre, and combine sales columns to one 'Region' column
genre_Data = (vgdata
    .filter(['Genre', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales'])
    .groupby('Genre')
    .sum()
    .reset_index()
    .melt(id_vars = ['Genre'], value_vars=['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales'], var_name = 'Region', value_name = 'Sales')
)
print(genre_Data.to_markdown(index=False))
# %%
# Create and save altair chart of genre data as png
genre_Chart = (alt.Chart(genre_Data, title = "Role playing games sell more in Japan")
    .encode(
        x = alt.X('Genre', sort = '-y'),
        y = 'Sales',
        color = alt.Color('Genre', legend=None),
        column = 'Region'
    )
    .mark_bar()
)
genre_Chart.save("altair_viz_2.png")
# %%