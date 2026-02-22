import pandas as pd
import xml.etree.ElementTree as ET

def xml_to_excel(xml_file, excel_file):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Prepare a list to store data
    data = []

    # Assuming XML structure is consistent and the first child element is the header
    columns = [elem.tag for elem in root[0]]

    # Iterate over each XML element and extract data
    for item in root:
        row_data = [elem.text for elem in item]
        data.append(row_data)

    # Create a DataFrame
    df = pd.DataFrame(data, columns=columns)

    # Save DataFrame to Excel file
    df.to_excel(excel_file, index=False, engine='openpyxl')

# Example usage
xml_file = 'output.xml'
excel_file = 'output.xlsx'
xml_to_excel(xml_file, excel_file)