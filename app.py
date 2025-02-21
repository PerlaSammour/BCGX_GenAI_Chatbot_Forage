from flask import Flask, render_template, request, jsonify
from dataset import Dataset
import re

# Initialise the dataset
dataset = Dataset()
dataset.preprocess_dataset()
df = dataset.df

# Define valid values for queries
valid_metrics = ["Total Revenue", "Net Income", "Total Assets", "Total Liabilities", 
    "Net cash from operations", "Revenue Growth (%)", "Net Income Growth (%)", 
    "Assets Growth (%)", "Liabilities Growth (%)", "Cash Flow Growth (%)", 
    "Profit Margin (%)", "Debt-to-Asset Ratio (%)"
]
valid_metric_perc=["Revenue Growth (%)", "Net Income Growth (%)", 
    "Assets Growth (%)", "Liabilities Growth (%)", "Cash Flow Growth (%)", 
    "Profit Margin (%)", "Debt-to-Asset Ratio (%)"
]
valid_metric_perc2=["Revenue Growth (%)", "Net Income Growth (%)", 
    "Assets Growth (%)", "Liabilities Growth (%)", "Cash Flow Growth (%)"
]
valid_metrics_pct_change = ["Total Revenue", "Net Income", "Total Assets", "Total Liabilities", 
    "Net cash from operations"
]

valid_companies = ["Microsoft", "Apple", "Tesla"]
valid_years = ["2022", "2023", "2024"]

# Define a mapping of base metric names to their growth percentage columns
growth_mapping = {
    "Total Revenue": "Revenue Growth (%)",
    "Net Income": "Net Income Growth (%)",
    "Total Assets": "Assets Growth (%)",
    "Total Liabilities": "Liabilities Growth (%)",
    "Net cash from operations": "Cash Flow Growth (%)"
}


# Create regex patterns for valid queries:

# The \s+ ensures any number of white spaces are valid between words, the . represents any character 
# except newline character, the + ensures 1 or more repetitions, the * ensures 0 or more repetitions, the ? is for non greedy search or for 0 or 1 repetitions, the \d{4} 
# ensures 4 digits for the year and the ?P<metric> names the group "metric"

pattern0 = r"Hello\s*!*|Hi\s*!*|Hey\s*!*$"
pattern00 = r"No\s*(thank\s+you\s*)?!*$"
pattern1 = r".*?What\s+was\s+the\s+(?P<metric>.+?)\s+of\s+(?P<company>.+?)\s+in\s+(?P<year>\d{4})\s*\?$"
pattern2 = r".*?How\s+did\s+the\s+(?P<metric>.+?)\s+of\s+(?P<company>.+?)\s+change\s+in\s+(?P<year>\d{4})\s*\?$"
pattern3 = r".*?Which\s+company\s+had\s+the\s+largest\s+(?P<metric>.+?)\s+in\s+(?P<year>\d{4})\s*\?$"


# Initialise the flask server
app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/get", methods=["GET","POST"])
def chat():
    input_msg = request.form["msg"]
    return get_chatbot_response(input_msg)

def get_chatbot_response(in_msg):
    
    # Check the first pattern:
    match1= re.match(pattern1, in_msg, re.IGNORECASE)

    if match1:
        metric = match1.group("metric").strip()  # to remove additional spaces at the end  or start of the word
        company = match1.group("company").strip()
        year = match1.group("year").strip()
        
        # Validate extracted values
        if metric in valid_metrics and company in valid_companies and year in valid_years:
            value = df.loc[(company, int(year)), metric] # get the value from the dataframe
            if metric in valid_metric_perc:
                return f"The {metric} for {company} in {year} was {value} %. Would you like to know how a financial metric of a company has changed in a certain year?"
            else:
                return f"The {metric} for {company} in {year} was {value} million $. Would you like to know how a financial metric of a company has changed in a certain year?"
        else:
            return "Sorry, that is not a valid metric or company or year."
    else:
        # Check the second pattern:
        match2= re.match(pattern2, in_msg, re.IGNORECASE)

        if match2:
            metric = match2.group("metric").strip()  # to remove additional spaces at the end  or start of the word
            company = match2.group("company").strip()
            year = match2.group("year").strip()
            # Validate extracted values
            if metric in valid_metrics_pct_change and company in valid_companies and year in valid_years:
                if int(year)==2022:
                    return "Sorry, I don't have any data before 2022 to compute how it has changed. Would you like to ask me about another year?"
                else:
                    value = df.loc[(company, int(year)), growth_mapping[metric]] # get the corresponding percent change value from the dataframe
                    if value>0:
                        return f"The {metric} of {company} has increased by {value} % in {year} with respect to the previous year. Would you like to know which company had the largest financial metric in a certain year?"
                    else:
                        return f"The {metric} of {company} has decreased by {value} % in {year} with respect to the previous year. Would you like to know which company had the largest financial metric in a certain year?"
            else:
                return "Sorry, that is not a valid metric or company or year."
        else:
            # Check the third pattern:
            match3= re.match(pattern3, in_msg, re.IGNORECASE)

            if match3:
                metric = match3.group("metric").strip()  # to remove additional spaces at the end  or start of the word
                year = match3.group("year").strip()
                # Validate extracted values
                if metric in valid_metrics and year in valid_years:
                    if metric in valid_metric_perc2 and int(year)==2022:
                        return f"Sorry, I don't have any data before 2022 to compute which company had the largest {metric}. Would you like to ask me about another year?"
                    else:
                        df_year = df.xs(int(year), level="Year")  # filter the dataframe for a specific year
                        top_company = df_year[metric].idxmax()    # check which company had the largest value
                        value = df.loc[(top_company, int(year)), metric] # exctract the value for this company
                        if metric in valid_metric_perc:
                            return f"{top_company} had the largest {metric} in {year} with {value} %. Would you like to know another financial metric?"
                        else:
                            return f"{top_company} had the largest {metric} in {year} with {value} million $. Would you like to know another financial metric?"
                else:
                    return "Sorry, that is not a valid metric or company or year."

            else:
                # Check if the message is a hello, hi or hey:
                match0 = re.match(pattern0, in_msg, re.IGNORECASE)
                if match0:
                    return "Hello! What financial metric would you like to know for Apple, Tesla or Microsoft in the last three years? Here are the ones I know: Total Revenue, Net Income, Total Assets, Total Liabilities, Net cash from operations, Revenue Growth (%), Net Income Growth (%), Assets Growth (%), Liabilities Growth (%), Cash Flow Growth (%), Profit Margin (%) and Debt-to-Asset Ratio (%)."
                else:
                    # Check if the message is a No:
                    match00 = re.match(pattern00, in_msg, re.IGNORECASE)
                    if match00:
                        return "Okay, let me know if you need anything else."
                    else:
                        return "Sorry, I only respond to specific queries!"



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)