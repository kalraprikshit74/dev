import csv
import xml.etree.ElementTree as ET

def csv_to_xml(csv_file_path, xml_file_path):
    # Read the CSV file
    with open(csv_file_path, newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)

        # Create the root XML element
        root = ET.Element('root')

        # Iterate over each row in the CSV
        for row in reader:
            # Create an XML element for each row
            item = ET.SubElement(root, 'item')
            
            # Add each field as a sub-element
            for field, value in row.items():
                field_element = ET.SubElement(item, field)
                field_element.text = value

        # Create an ElementTree and write to XML file
        tree = ET.ElementTree(root)
        with open(xml_file_path, 'wb') as xml_file:
            tree.write(xml_file, encoding='utf-8', xml_declaration=True)

# Example usage:
csv_file_path = 'sample.csv'
xml_file_path = 'output.xml'
csv_to_xml(csv_file_path, xml_file_path)

print(f"Conversion completed. Check the {xml_file_path} file.")
