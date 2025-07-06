import json

file_path = "Good News, Bad News.txt"
dialogues = []
current_role = None
current_content = ""


with open(file_path,'r') as file:
    data = file.read()
    lines = data.split('\n')
    for line in lines:
        clean_line = line.strip()
        if clean_line.startswith('JERRY') or clean_line.startswith('GEORGE') or clean_line.startswith('CLAIRE') or clean_line.startswith('KRAMER'):
            if current_role:
                current_content = current_content.replace('\n', '')
                dialogues.append({"role": current_role, "content": current_content[len(current_role):].strip()})
            current_role = clean_line
            current_content = clean_line
        elif current_role and clean_line:
            current_content += " " + clean_line.replace('\n', '')

    if current_role:
        current_content = current_content.replace('\n', '')
        dialogues.append({"role": current_role, "content": current_content[len(current_role):].strip()})

    json_string = json.dumps(dialogues, indent=2)

   

    with open('dialogues.json', 'w') as json_file:
        json_file.write(json_string)