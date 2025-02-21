## BCG X - GenAI - Chatbot:
### Forage Internship Simulation:

#### Overview:

This Chatbot is part of an internship simulation on Forage.com, organized by BCG X - GenAI. It consists of creating a Chatbot
used to aid GFC (Global Financial Corp) in the financial analysis of several US companies, by transforming complex financial data 
into actionable insights and making the intricate data easily accessible and understandable for their financial decisions.

This Chatbot is a simple project that could be part of a much bigger AI Chatbot. It is implemented using a rule-based logic, which means that it can only answer a limited number of queries. However, this is essential to provide immediate and accurate responses to common queries (FAQs).

#### Project Structure:

The project is composed of the following:
- "app.py": That is the main python script that needs to be run to launch the Chatbot on the local host (0.0.0.0) on port 5001 using Flask. It initializes the dataset by calling the Dataset class defined in "dataset.py" then computes the percent change and some key financial ratios. After that, it initialises the variables needed and the Flask app and uses the Regex module to compute the matching of the messages acquired from the user with some predefined patterns and returns a response accordingly.
- "dataset.py": This script defines a class that reads the dataset from the csv file and defines the data into a dataframe attribute of the class.
- "Extracted_10K_financial_data.csv": This is the csv file containing the financial metrics extracted from the last 3 10K documents of Apple, Tesla and Microsoft.
- "templates/index.html": This is the HTML page that is rendered with the Flask server, it is the front-end of the Chatbot where the user inputs their message. It was developed by "Binaryhood" on Github.
- "static/style.css": This is the CSS file for the front-end. It was also developed by "Binaryhood" on Github.

#### Testing Guide:

1) Run the python script: "app.py"
2) Open the browser and type: http://localhost:5001 or an equivalent URL considering that the server is running on 0.0.0.0
3) Input a query, the Chatbot is case-insensitive and can also ignore extra spaces. However, it will only respond to these queries:
(NOTE: the metric and company are case-sensitive and these are the valid ones: Metrics: "Total Revenue", "Net Income", "Total Assets", "Total Liabilities", "Net cash from operations", "Revenue Growth (%)", "Net Income Growth (%)", "Assets Growth (%)", "Liabilities Growth (%)", "Cash Flow Growth (%)", "Profit Margin (%)", "Debt-to-Asset Ratio (%)" and Companies: "Microsoft", "Apple", "Tesla" and Years: "2022", "2023", "2024")
- "Hello"/"Hi"/"Hey" with or without "!"
- "No" or "No thank you" with or without "!"
- "What was the <metric> of <company> in <year>?" (it also ignores words before "What")
- "How did the <metric> of <company> change in <year>?" (it also ignores words before "How")
- "Which company had the largest <metric> in <year>?" (it also ignores words before "which")


#### Limitations:

Since this chatbot is developed using rule-based logic, it will only respond to the previously mentioned queries. Also, although the chatbot is case-insensitive and can ignore extra spaces, the metrics, company names, and years must be written exactly as specified, without modifications in case or additional spaces: 

- Metrics: "Total Revenue", "Net Income", "Total Assets", "Total Liabilities", "Net cash from operations", "Revenue Growth (%)", "Net Income Growth (%)", "Assets Growth (%)", "Liabilities Growth (%)", "Cash Flow Growth (%)", "Profit Margin (%)", "Debt-to-Asset Ratio (%)"

- Companies: "Microsoft", "Apple", "Tesla" 

- Years: "2022", "2023", "2024"