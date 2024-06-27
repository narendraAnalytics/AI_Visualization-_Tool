import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Page configuration
st.set_page_config(page_title="AI-Powered Data Visualization Tool", layout="wide")

# Title and Note
st.title("AI-Powered Data Visualization Tool")
st.markdown("""
    **Note:** Please ensure your data is clean, with no null values, duplicates, or outliers, for optimal performance.
""")

# File Upload
uploaded_file = st.file_uploader("Upload your CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    # Read the file
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.write("### Data Preview:")
    st.write(df.head())

    # Layout with standard Streamlit tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "Univariate Analysis",
        "Bivariate Analysis",
        "Multivariate Analysis",
        "Top 5 Market Share"
    ])

    with tab1:
        st.header("Univariate Analysis")
        numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        selected_column = st.selectbox("Select column for Univariate Analysis", numeric_columns)

        if selected_column:
            st.write("#### Summary Statistics:")
            st.write(df[selected_column].describe())

            if st.button("Show Distribution Plot"):
                st.write("#### Distribution Plot:")
                fig, ax = plt.subplots(figsize=(10, 4))  # Set the height of the plot
                sns.histplot(df[selected_column], bins=30, kde=True, ax=ax)
                st.pyplot(fig)
                st.markdown(f"""
                **Description**:
                This distribution plot shows the frequency distribution of the selected numeric column **{selected_column}**.
                The histogram bins are set to 30, and a KDE (Kernel Density Estimate) is overlaid to show the probability density.
                """)

            if st.button("Show Box Plot"):
                st.write("#### Box Plot:")
                fig, ax = plt.subplots(figsize=(10, 4))  # Set the height of the plot
                sns.boxplot(x=df[selected_column], ax=ax)
                st.pyplot(fig)
                st.markdown(f"""
                **Description**:
                The box plot displays the distribution of the data based on a five-number summary: minimum, first quartile, median, third quartile, and maximum.
                """)

            if st.button("Show Violin Plot"):
                st.write("#### Violin Plot:")
                fig, ax = plt.subplots(figsize=(10, 4))  # Set the height of the plot
                sns.violinplot(x=df[selected_column], ax=ax)
                st.pyplot(fig)
                st.markdown(f"""
                **Description**:
                The violin plot combines aspects of the box plot with a kernel density plot, showing peaks in the data.
                """)

    with tab2:
        st.header("Bivariate Analysis")
        columns = df.columns.tolist()
        x_column = st.selectbox("Select X-axis column", columns)
        y_column = st.selectbox("Select Y-axis column", columns)

        if x_column and y_column:
            st.write("#### Bar Plot:")
            fig = px.bar(df, x=x_column, y=y_column, 
                         title="Bar Plot", 
                         template="plotly", 
                         color=y_column, 
                         color_continuous_scale=px.colors.sequential.Plotly3)
            st.plotly_chart(fig)
            st.markdown(f"""
            **Description**:
            This bar plot shows the relationship between **{x_column}** and **{y_column}**.
            It is useful for comparing quantities across different categories or groups.
            """)

    with tab3:
        st.header("Multivariate Analysis")
        st.write("#### Pairplot:")
        fig = sns.pairplot(df.select_dtypes(include=['float64', 'int64']))
        st.pyplot(fig)

        # Dynamic description for Pairplot
        st.markdown("""
        **Description**:
        The pair plot visualizes pairwise relationships in the dataset for all numeric columns.
        It provides scatter plots for each pair of variables and histograms on the diagonal.
        """)

        st.write("#### Heatmap:")
        correlation = df.select_dtypes(include=['float64', 'int64']).corr()
        fig, ax = plt.subplots(figsize=(10, 8))  # Adjust the height of the heatmap
        sns.heatmap(correlation, annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)

        # Dynamic description for Heatmap
        st.markdown("""
        **Description**:
        The heatmap displays the correlation matrix of numeric columns in the dataset.
        The color intensity represents the strength of the correlation, with annotations showing the correlation coefficients.
        """)

    with tab4:
        st.header("Top 5 Market Share")
        categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
        selected_category = st.selectbox("Select category for Market Share", categorical_columns)

        if selected_category:
            top_5 = df[selected_category].value_counts().head(5)
            fig = px.pie(top_5, values=top_5.values, names=top_5.index, 
                         title='Top 5 Market Share', 
                         template="plotly_dark", 
                         hover_data=[top_5.values],
                         color_discrete_sequence=px.colors.qualitative.Plotly)
            fig.update_traces(textinfo='percent')
            st.plotly_chart(fig)

            # Dynamic description
            st.markdown(f"""
            **Description**:
            This pie chart visualizes the top 5 categories in **{selected_category}** by their frequency.
            The chart segments represent the proportion of each category, providing insights into the market share.
            """)

if not uploaded_file:
    st.write("Please upload a CSV or Excel file to proceed.")
