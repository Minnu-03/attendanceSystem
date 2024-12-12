import pandas as pd

def convert_excel_to_csv(excel_path, csv_path):
    # Load the Excel file
    df = pd.read_excel(excel_path)

    # Save as CSV, specify the encoding to be UTF-8
    df.to_csv(csv_path, index=False, encoding='utf-8-sig')

if __name__ == "__main__":
    # Path to your Excel file
    excel_path = '/home/rahul/Downloads/QR_org/data/2022_CSM_Students.xlsx'
    
    # Path for the new CSV file
    csv_path = '/home/rahul/Downloads/QR_org/data/2022_CSM_Students_converted.csv'
    
    # Call the function to convert the Excel file to CSV
    convert_excel_to_csv(excel_path, csv_path)
