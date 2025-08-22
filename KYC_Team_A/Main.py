import cv2
from PIL import Image
import pytesseract
import json
import re 

def convert_to_json(text):
    result = {}
    
    lines = text.strip().split('\n')
    
    address_lines = []  # This will store the lines for address
    capturing_address = False  # Flag to indicate we're capturing the address

    aadhar_pattern = r'\b\d{4} \d{4} \d{4}\b'
    
    for line in lines:
        # Skip empty lines
        if line.strip() == "":
            continue
        
        # Extract Name
        if line.startswith("Name:"):
            result["Name"] = line.split(":", 1)[1].strip()
            continue
        
        # Extract DOB
        if line.startswith("DOB:"):
            result["DOB"] = line.split(":", 1)[1].strip()
            continue
        
        # Extract Gender
        if line.startswith("Gender:"):
            result["Gender"] = line.split(":", 1)[1].strip()
            continue
        
        if line.startswith("Address:"):
            capturing_address = True
            line = line.split(":", 1)[1].strip()
            if line:
                address_lines.append(line)
            continue
        
        if capturing_address:
            if re.search(aadhar_pattern, line):  # If Aadhar number appears, stop capturing address
                capturing_address = False
                result["Address"] = " ".join(address_lines)  # Join all lines as one string
                aadhar_number = re.search(aadhar_pattern, line).group()
                result["Aadhar Number"] = aadhar_number
                continue
            else:
                address_lines.append(line.strip())  
    
  
        result["Address"] = " ".join(address_lines)
    
    return result


im = Image.open(r"aadharSamples\sample_aadhar.jpg")
img = cv2.imread(r"aadharSamples\sample_aadhar.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
text = pytesseract.image_to_string(gray)
json_data = convert_to_json(text)

with open(r'CSV\JSONFiles\output.json', 'w') as json_file:
    json.dump(json_data, json_file, indent=4)

