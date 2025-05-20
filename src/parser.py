import re
import pandas as pd
from dateutil import parser as dateparser

def parse_whatsapp_chat(filepath):
    # Regex para: [dd/mm/yyyy, hh:mm:ss] Nombre: Mensaje
    pattern = re.compile(r'^\[(\d{2}/\d{2}/\d{4}), (\d{2}:\d{2}:\d{2})\] ([^:]+): (.*)$')
    data = []
    current = None

    with open(filepath, encoding='utf-8') as file:
        for line in file:
            line = line.rstrip('\n')
            match = pattern.match(line)
            if match:
                if current:
                    data.append(current)
                date_str, time_str, sender, message = match.groups()
                timestamp = dateparser.parse(f"{date_str} {time_str}", dayfirst=True)
                current = {
                    "timestamp": timestamp,
                    "sender": sender,
                    "message": message
                }
            else:
                # Continuación de mensaje multilínea
                if current:
                    current["message"] += "\n" + line
        # Agrega el último mensaje
        if current:
            data.append(current)

    df = pd.DataFrame(data)
    return df

