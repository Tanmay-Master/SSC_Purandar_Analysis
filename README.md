# 🏫 School-wise Pass Percentage Comparison (SSC) for Purandar Taluka

A comprehensive Streamlit web application for analyzing and comparing SSC (Secondary School Certificate) examination results across multiple schools in Pune district.

## Features

### 📊 Main Dashboard
- **School-wise Pass Percentage Comparison**: Interactive horizontal bar chart showing pass percentages for all schools in a selected year
- **Dynamic School Filtering**: Select one or multiple schools to compare their performance side-by-side
- **Year Selection**: View data for different academic years

### 📈 School Performance Timeline
- **Candidates Appeared vs Passed**: Line chart tracking student appearance and pass counts over multiple years
- **Pass Percentage Trend**: Visual trend analysis of pass percentage changes over time
- **Detailed Performance Table**: Year-wise breakdown of all key metrics for any selected school

### 🏆 Top Schools Analytics
- **Top 10 Schools Ranking**: Automatic ranking of top-performing schools based on average pass percentage over the last 5 years
- **Summary Metrics**: Quick stats on the best-performing school and total student participation

### 📋 Raw Data Access
- **Expandable Data Table**: View complete filtered dataset for the selected year

## Installation

### Requirements
- Python 3.8+
- See `requirements.txt` for all dependencies

### Setup

1. Clone or download this project to your local machine
2. Navigate to the project directory
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the Streamlit application:
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## Data Structure

The application expects a CSV file named `combined_ssc_data.csv` with the following columns:
- `Name of the School` - School name
- `Candidates Registered` - Number of registered candidates
- `Candidates Appeared` - Number of candidates who appeared
- `Distin-ction` - Number with distinction grade
- `Grade I` - Number with Grade I
- `Grade II` - Number with Grade II
- `Pass Grade` - Number with pass grade
- `Total Pass` - Total number of passing students
- `Pass Percent` - Pass percentage (0-100)
- `Year` - Academic year

## How to Use the App

### 1. Select Year
Use the sidebar dropdown to choose an academic year (defaults to the latest available year)

### 2. Filter by Schools (Optional)
- Use the multi-select dropdown to choose specific schools
- Leave empty to view all schools for that year
- The main chart updates automatically based on your selection

### 3. Explore School Timeline
- Select a school from the "Select School for Timeline View" dropdown
- View historical performance data and trends
- Check year-wise details in the performance table below

### 4. View Top Performers
- Automatically shows the top 10 schools by average pass percentage
- Data covers the last 5 academic years
- Quick summary metrics displayed on the right

### 5. Access Raw Data
- Expand the "Show raw data for selected year" section
- View complete filtered dataset in table format

## Project Files

- `app.py` - Main Streamlit application
- `combined_ssc_data.csv` - Source data file (SSC examination results)
- `requirements.txt` - Python dependencies
- `README.md` - This documentation file
- `EDA&FE.ipynb` - Jupyter notebook for exploratory data analysis and feature engineering
- `Data/` - Additional data files directory

## Features in Detail

### Interactive Filters
- **Year Filter**: Dynamically loads all available academic years
- **School Filter**: Multi-select dropdown with schools from selected year only
- Both filters update all visualizations automatically

### Visualizations
- **Horizontal Bar Charts**: Easy comparison of pass percentages across schools
- **Line Charts with Markers**: Track trends and changes over time
- **Color Coding**: Pass percentages color-coded for quick visual analysis
- **Responsive Design**: Charts automatically adjust height based on number of schools

### Performance Metrics
- Total candidates appeared
- Total passing candidates
- Pass percentage (%) 
- Grade distribution (Distinction, Grade I, Grade II, Pass Grade)
- 5-year average analysis

## Browser Compatibility

Works on all modern web browsers that support HTML5:
- Chrome/Chromium
- Firefox
- Safari
- Edge

## Performance Notes

- Data is cached on first load for faster interactions
- Charts render efficiently even with large datasets
- Multiselect filters ensure snappy performance

## Future Enhancements

Potential improvements:
- Export filtered data to Excel/PDF
- Comparative analysis across multiple selected schools
- Trend predictions using machine learning
- Grade distribution analysis
- Subject-wise performance (if data available)
- Time-series forecasting

## Troubleshooting

### "No data available for the year [year]"
- Ensure your CSV file contains data for the selected year
- Check CSV file path is correct: `combined_ssc_data.csv`

### Charts not displaying
- Verify Plotly is installed: `pip install plotly`
- Check data format matches expected structure

### Slow performance
- Close other applications to free up system resources
- Ensure CSV file is not corrupted

## License

This project is intended for educational and analytical purposes.

## Contact

For questions or issues, please refer to the project documentation or data source contact.
