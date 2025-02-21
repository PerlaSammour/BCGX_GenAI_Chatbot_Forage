import pandas as pd
import os



class Dataset():
    
    def __init__(self):
        
        script_dir = os.path.dirname(os.path.abspath(__file__))  # Get script's directory
        file_path = os.path.join(script_dir, "Extracted_10K_financial_data.csv")    # Build absolute path so that the csv file is always found
        try:
            self.df = pd.read_csv(file_path)
            print(self.df)
            # Convert the string values to float:
            cols_to_convert = ['Total Revenue', 'Net Income', 'Total Assets','Total Liabilities','Net cash from operations']
            self.df[cols_to_convert] =  self.df[cols_to_convert].apply(pd.to_numeric, errors='coerce')
        
        except:
            print("Error loading dataset, using default values instead.")
            data = {
                "Company": ["Microsoft", "Microsoft", "Microsoft", "Tesla", "Tesla", "Tesla", "Apple", "Apple", "Apple"],
                "Year": [2022, 2023, 2024, 2022, 2023, 2024, 2022, 2023, 2024],
                "Total Revenue": [198270, 211915, 245122, 81462, 96773, 97690, 394328, 383285, 391035],
                "Net Income": [72738, 72361, 88136, 12587, 14974, 7153, 99803, 96995, 93736],
                "Total Assets": [364840, 411976, 512163, 82338, 106618, 122070, 352755, 352583, 364980],
                "Total Liabilities": [198298, 205753, 243686, 36440, 43009, 48390, 302083, 290437, 308030],
                "Net cash from operations": [89035, 87582, 118548, 14724, 13256, 14923, 122151, 110543, 118254]
            }

            self.df = pd.DataFrame(data)
        
    @staticmethod
    def compute_pct_change(df):
        df['Revenue Growth (%)'] = df.groupby(['Company'])['Total Revenue'].pct_change() * 100
        df['Net Income Growth (%)'] = df.groupby(['Company'])['Net Income'].pct_change() * 100
        df['Assets Growth (%)'] = df.groupby(['Company'])['Total Assets'].pct_change() * 100
        df['Liabilities Growth (%)'] = df.groupby(['Company'])['Total Liabilities'].pct_change() * 100
        df['Cash Flow Growth (%)'] = df.groupby(['Company'])['Net cash from operations'].pct_change() * 100

        # Fill NA values that result from pct_change calculations with 0 or an appropriate value
        df.fillna(0, inplace=True)

        # Round to two decimal places
        df[['Revenue Growth (%)', 'Net Income Growth (%)', 'Assets Growth (%)', 
            'Liabilities Growth (%)', 'Cash Flow Growth (%)']] = df[[
            'Revenue Growth (%)', 'Net Income Growth (%)', 'Assets Growth (%)', 
            'Liabilities Growth (%)', 'Cash Flow Growth (%)']].round(2)
        
        return df
    
    @staticmethod
    def compute_key_ratios(df):
        df["Profit Margin (%)"] = (df["Net Income"] / df["Total Revenue"]) * 100
        df["Debt-to-Asset Ratio (%)"] = (df["Total Liabilities"] / df["Total Assets"]) * 100

        # Round to two decimal places
        df[['Profit Margin (%)', 'Debt-to-Asset Ratio (%)']] = df[['Profit Margin (%)', 'Debt-to-Asset Ratio (%)']].round(2)

        return df
    
    def preprocess_dataset(self):
        self.df = self.compute_pct_change(self.df)
        self.df = self.compute_key_ratios(self.df)
        # Set the company and year as indices for easier referencing:
        self.df.set_index(["Company", "Year"], inplace=True)
        print(self.df)



    
            

