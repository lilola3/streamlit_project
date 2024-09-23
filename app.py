import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Lebanon's Educational Ressources :sunglasses:")

data_frame = df = pd.read_csv('Education_resources.csv')


# Grouping data by 'Town' and summing the educational resource types
resource_distribution = data_frame.groupby('Town')[
    ['Type and size of educational resources - public schools',
     'Type and size of educational resources - vocational institute',
     'Type and size of educational resources - universities',
     'Type and size of educational resources - private schools']
].sum()

# Selecting the top 10 towns based on the total size of educational resources
top_10_towns = resource_distribution.sum(axis=1).nlargest(10).index

# Filtering data for these top 10 towns
filtered_data = resource_distribution.loc[top_10_towns].reset_index()

# Create an interactive bar chart
fig = px.bar(
    filtered_data,
    x='Town',
    y=filtered_data.columns[1:],  # Use all resource types
    title='Distribution of Educational Resources in Top 10 Towns',
    labels={'value': 'Number of Resources', 'variable': 'Resource Type'},
    text_auto=True
)

# Update layout for larger size
fig.update_layout(
    width=1000,  # Width of the figure
    height=600,  # Height of the figure
    title_font=dict(size=20),  # Title font size
    xaxis_title_font=dict(size=14),  # X-axis title font size
    yaxis_title_font=dict(size=14),  # Y-axis title font size
    legend_font=dict(size=12)  # Legend font size
)

# Display the plot in Streamlit
st.plotly_chart(fig, use_container_width=True)

# Optional description
st.write("This interactive chart shows the distribution of educational resources across the top 10 towns.")


import streamlit as st
import pandas as pd
import plotly.express as px



# Filter out towns with zero resources in all categories
non_zero_towns = data_frame[
    (data_frame['Type and size of educational resources - public schools'] > 0) |
    (data_frame['Type and size of educational resources - private schools'] > 0) |
    (data_frame['Type and size of educational resources - vocational institute'] > 0) |
    (data_frame['Type and size of educational resources - universities'] > 0)
]

# Unique towns for selectbox
towns = non_zero_towns['Town'].unique()
selected_town = st.selectbox('Choose a town', towns)

# Filter data for the selected town
town_data = data_frame[data_frame['Town'] == selected_town]


# Visualization 1: Breakdown for the selected town
st.subheader(f"Resource Breakdown for {selected_town}")
fig1 = px.bar(
    town_data.melt(id_vars='Town', 
                   value_vars=[
                       'Type and size of educational resources - public schools',
                       'Type and size of educational resources - private schools',
                       'Type and size of educational resources - vocational institute',
                       'Type and size of educational resources - universities']),
    x='variable',
    y='value',
    title=f'Education Resources in {selected_town}',
    labels={'variable': 'Resource Type', 'value': 'Count'},
    color='variable'
)
st.plotly_chart(fig1)
st.write("This vizualisation enable us to select any town and investigate their respective educational resources.")
st.write("We can see that Trablous and Saida have the most schools and the most diverse resources.")

# Interactive Feature 2: Slider to filter towns by the number of public schools
min_public_schools = int(data_frame['Type and size of educational resources - public schools'].min())
max_public_schools = int(data_frame['Type and size of educational resources - public schools'].max())

school_filter = st.slider(
    'Select the minimum number of public schools a town should have:',
    min_public_schools, max_public_schools, min_public_schools
)

# Filter data based on the slider value
filtered_data = data_frame[data_frame['Type and size of educational resources - public schools'] >= school_filter]

# Visualization 2: Distribution for filtered towns
st.subheader(f"Towns with at least {school_filter} public schools")
fig2 = px.bar(
    filtered_data,
    x='Town',
    y=[
        'Type and size of educational resources - public schools',
        'Type and size of educational resources - private schools',
        'Type and size of educational resources - vocational institute',
        'Type and size of educational resources - universities'
    ],
    title=f'Resource Distribution in Towns with at Least {school_filter} Public Schools',
    barmode='stack'
)
st.plotly_chart(fig2)

# Optional description
st.write("This dashboard allows you to explore educational resources by town and apply filters to see only towns with a minimum number of public schools.")


import pandas as pd
import plotly.express as px
import streamlit as st

# Assuming 'data_frame' is already loaded with your CSV data

# Aggregate the data
school_types = {
    'Public Schools': data_frame['Type and size of educational resources - public schools'].sum(),
    'Private Schools': data_frame['Type and size of educational resources - private schools'].sum(),
    'Vocational Institutes': data_frame['Type and size of educational resources - vocational institute'].sum()
}

# Convert to a DataFrame
school_types_df = pd.DataFrame(list(school_types.items()), columns=['School Type', 'Count'])

# Create a multi-select box for users to select which school types they want to include
selected_school_types = st.multiselect(
    'Select school types to display:',
    options=school_types_df['School Type'].unique(),
    default=school_types_df['School Type'].unique()  # Default to all selected
)

# Filter the DataFrame based on the selected school types
filtered_school_types_df = school_types_df[school_types_df['School Type'].isin(selected_school_types)]

# Plot the pie chart using Plotly
fig = px.pie(filtered_school_types_df, values='Count', names='School Type', 
             title='Distribution of School Types Across All Towns',
             color_discrete_sequence=['#ff9999', '#66b3ff', '#99ff99'])

# Display the chart in Streamlit
st.plotly_chart(fig)
st.write("We can see through this vizualisation that the repartition of public and private schools in Lebanon are evenly distributed")


