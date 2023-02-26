import os
import json

# Load the list of names to be redacted
if os.path.isfile('redact.txt'):
    with open('redact.txt', 'r') as f:
        names_to_redact = [line.strip() for line in f]
        redact_warning = ""
        if len(names_to_redact) > 0:
            redact_warning = f"\n\nThe following strings have been redacted: {', '.join(names_to_redact)}\n"
else:
    names_to_redact = []
    redact_warning = "\n\nWarning: redact.txt file not found. No strings have been redacted.\n"

# Loop through all the JSON files in the current directory
json_files_found = False
for filename in os.listdir('.'):
    if filename.endswith('.json'):
        json_files_found = True
        # Load the JSON file
        with open(filename, 'r') as f:
            data = json.load(f)
        
        # Create the output filename by replacing .json with .txt
        output_filename = f'{filename[:-5]}.txt'
        
        # Extract the text from each message and write it to the output file
        with open(output_filename, 'w') as f:
            for message in data['histories']['histories'][0]['msgs']:
                sender_name = message['src']['name']
                text = message['text']
                
                # Redact any instances of names in the message
                for name in names_to_redact:
                    text = text.replace(name, '[NAME_IN_MESSAGE_REDACTED]')
                
                # Replace any instances of double line breaks with single line breaks
                text = text.replace('\n\n', '\n')
                
                f.write(f"{sender_name}: {text}\n")

if not json_files_found:
    print("No .json files found. Place the .json files into the same folder where this program is located.")
    input("\nPress Enter to exit.")
else:
    print("Extracted successfully." + redact_warning)
    input("Press Enter to exit.")
