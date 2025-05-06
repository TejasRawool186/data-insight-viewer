# 📊 Data Insight Viewer

**Data Insight Viewer** is an interactive and AI-augmented Streamlit application that enables users to upload CSV or Excel files and explore their datasets through automatic summarization, visualizations, and basic natural language processing (NLP) features.

## 🚀 Features

### ✅ File Upload and Preview
- Supports CSV and Excel files.
- Displays the full data preview after upload.
- Provides basic dataset statistics like number of rows and columns.

### 📈 Data Summarization Tabs
- **Summary**: Statistical summary using `.describe()`.
- **Top and Bottom Rows**: Adjustable number of head and tail rows.
- **Data Types**: Shows data types of each column.
- **Columns**: Displays all column names.

### 🔢 Column Value Counts with Visualization
- Choose a column to analyze value counts.
- Visualize counts with:
  - Bar chart
  - Line chart
  - Pie chart

### 🧮 Groupby Aggregation and Visualization
- Group by one or more columns.
- Choose an aggregation (sum, mean, count, etc.).
- Visualize grouped data using:
  - Line chart
  - Bar chart
  - Scatter plot
  - Pie chart
  - Sunburst chart

### 🧠 NLP Capabilities
Includes support for text columns:

- **Sentiment Analysis**: Detect polarity and sentiment (positive, neutral, negative).
- **Word Frequency Counter**: View top 10 most common words.
- **Keyword Search**: Find all rows containing a keyword or phrase.

---

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/TejasRawool186/data-insight-viewer.git
cd data-insight-viewer
