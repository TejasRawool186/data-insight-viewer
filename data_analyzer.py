import pandas as pd
import plotly.express as px
import streamlit as st
from textblob import TextBlob
import re
from collections import Counter

# Page config
st.set_page_config(
    page_title="Data Insight Viewer",
    page_icon="📊"
)

# Title
st.title(":rainbow[Data Insight Viewer]")
st.subheader(":rainbow[Explore data with ease]", divider="rainbow")

# File uploader
file = st.file_uploader("Drop CSV or Excel file", type=['csv', 'xlsx'])

if file is not None:
    data = pd.read_csv(file) if file.name.endswith('csv') else pd.read_excel(file)
    st.dataframe(data)
    st.info("✅ File is successfully uploaded")

    # Basic info
    st.subheader(":rainbow[Basic information of dataset]", divider="rainbow")
    tab1, tab2, tab3, tab4 = st.tabs(['Summary', 'Top and Bottom Rows', 'Data Types', 'Columns'])

    with tab1:
        st.write(f"There are {data.shape[0]} rows and {data.shape[1]} columns in the dataset")
        st.subheader(":gray[Statistical summary of the dataset]")
        st.dataframe(data.describe())

    with tab2:
        st.subheader(":gray[Top Rows]")
        toprows = st.slider("Number of top rows", 1, data.shape[0], key="topslider")
        st.dataframe(data.head(toprows))

        st.subheader(":gray[Bottom Rows]")
        bottomrows = st.slider("Number of bottom rows", 1, data.shape[0], key="bottomslider")
        st.dataframe(data.tail(bottomrows))

    with tab3:
        st.subheader(':gray[Data types]')
        st.dataframe(data.dtypes)

    with tab4:
        st.subheader('Column names in dataset')
        st.write(list(data.columns))

    # Value Counts
    st.subheader(":rainbow[Column Value to Count]", divider="rainbow")
    with st.expander("Value Count"):
        col1, col2 = st.columns(2)
        with col1:
            column = st.selectbox("Choose column name", options=list(data.columns))
        with col2:
            toprows = st.number_input("Top rows", min_value=1, step=1, value=5)

        if st.button("Count"):
            result = data[column].value_counts().reset_index().head(toprows)
            result.columns = [column, "count"]
            st.dataframe(result)

            st.subheader("Visualization", divider="gray")
            fig = px.bar(data_frame=result, x=column, y='count', text='count', template="presentation")
            st.plotly_chart(fig)
            fig = px.line(data_frame=result, x=column, y="count", text="count", template="presentation")
            st.plotly_chart(fig)
            fig = px.pie(data_frame=result, names=column, values="count")
            st.plotly_chart(fig)

    # Groupby and Visualization
    st.subheader(":rainbow[Groupby: Simplify your data analysis]", divider="rainbow")
    with st.expander("Group by your columns"):
        col1, col2, col3 = st.columns(3)
        with col1:
            groupby_cols = st.multiselect("Choose columns to group by", options=list(data.columns))
        with col2:
            operation_col = st.selectbox("Choose column for aggregation", options=list(data.columns))
        with col3:
            operation = st.selectbox("Choose operation", options=["sum", "max", "min", "mean", "median", "count"])

        if groupby_cols:
            result = data.groupby(groupby_cols).agg(newcol=(operation_col, operation)).reset_index()
            st.dataframe(result)

            st.subheader(":gray[Data Visualization]", divider="gray")
            graph_type = st.selectbox("Choose graph type", options=["line", "bar", "scatter", "Pie", "sunburst"])

            if graph_type == "line":
                x_axis = st.selectbox("Choose x-axis", options=list(result.columns))
                y_axis = st.selectbox("Choose y-axis", options=list(result.columns))
                color = st.selectbox("Color information", options=[None] + list(result.columns))
                fig = px.line(result, x=x_axis, y=y_axis, color=color, markers=True)
                st.plotly_chart(fig)

            elif graph_type == "bar":
                x_axis = st.selectbox("Choose x-axis", options=list(result.columns))
                y_axis = st.selectbox("Choose y-axis", options=list(result.columns))
                color = st.selectbox("Color information", options=[None] + list(result.columns))
                facet_col = st.selectbox("Facet column (optional)", options=[None] + list(result.columns))
                fig = px.bar(result, x=x_axis, y=y_axis, color=color, facet_col=facet_col if facet_col else None, barmode="group")
                st.plotly_chart(fig)

            elif graph_type == "scatter":
                x_axis = st.selectbox("Choose x-axis", options=list(result.columns))
                y_axis = st.selectbox("Choose y-axis", options=list(result.columns))
                color = st.selectbox("Color information", options=[None] + list(result.columns))
                size = st.selectbox("Size column", options=[None] + list(result.columns))

                if size and pd.api.types.is_numeric_dtype(result[size]) and (result[size] >= 0).all():
                    fig = px.scatter(result, x=x_axis, y=y_axis, color=color, size=size)
                    st.plotly_chart(fig)
                else:
                    st.warning("Size column must be numeric and non-negative")

            elif graph_type == "Pie":
                values = st.selectbox("Choose numeric values", options=list(result.select_dtypes(include='number').columns))
                names = st.selectbox("Choose labels", options=list(result.columns))
                fig = px.pie(data_frame=result, values=values, names=names)
                st.plotly_chart(fig)

            elif graph_type == "sunburst":
                categorical_cols = list(result.select_dtypes(exclude='number').columns)
                path = st.multiselect("Choose path (hierarchical categories)", options=categorical_cols)
                if path and "newcol" in result.columns:
                    fig = px.sunburst(data_frame=result, path=path, values="newcol")
                    st.plotly_chart(fig)
                else:
                    st.warning("Please select valid categorical columns for path and ensure 'newcol' exists.")

    # NLP Section
    st.subheader(":rainbow[🧠 Basic NLP Features]", divider="rainbow")

    # Text Columns
    text_cols = list(data.select_dtypes(include='object').columns)

    with st.expander("📌 Sentiment Analysis"):
        if text_cols:
            text_col = st.selectbox("Select a text column", text_cols)
            if st.button("Analyze Sentiment"):
                data['polarity'] = data[text_col].apply(lambda x: TextBlob(str(x)).sentiment.polarity)
                data['sentiment'] = data['polarity'].apply(lambda x: 'Positive' if x > 0 else ('Negative' if x < 0 else 'Neutral'))
                st.dataframe(data[[text_col, 'polarity', 'sentiment']])
                st.bar_chart(data['sentiment'].value_counts())
        else:
            st.warning("No text columns found for sentiment analysis.")

    with st.expander("📌 Word Frequency Counter"):
        if text_cols:
            wc_col = st.selectbox("Select text column for word count", text_cols, key="wordcount")
            if st.button("Show Top Words"):
                all_text = ' '.join(data[wc_col].dropna().astype(str).tolist())
                words = re.findall(r'\b\w+\b', all_text.lower())
                word_freq = Counter(words).most_common(10)
                freq_df = pd.DataFrame(word_freq, columns=['word', 'count'])
                st.dataframe(freq_df)
                st.bar_chart(freq_df.set_index('word'))
        else:
            st.warning("No text columns found for word frequency.")

    with st.expander("📌 Keyword Search in Text"):
        if text_cols:
            search_col = st.selectbox("Choose text column", text_cols, key="searchtext")
            keyword = st.text_input("Enter keyword or phrase to search")
            if keyword:
                result = data[data[search_col].str.contains(keyword, case=False, na=False)]
                st.write(f"Found {len(result)} matching rows")
                st.dataframe(result)
        else:
            st.warning("No text columns found for search.")
