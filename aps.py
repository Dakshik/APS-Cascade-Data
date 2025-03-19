import json
from datetime import datetime

# Define input and output file paths
txt_file_path = "/Users/dakshikaushik/Downloads/aps/dataset.txt" 
output_json_file = "aps_cascades.json"
n_cascades = 1000  # Number of cascades to extract

def read_txt_file(txt_path):
    """Reads the APS dataset txt file and returns its content as a list of lines."""
    with open(txt_path, "r", encoding="utf-8") as file:
        return file.readlines()

def convert_to_unix_timestamp(date_str):
    """Converts a date string (YYYY-MM-DD) to a Unix timestamp."""
    try:
        return int(datetime.strptime(date_str, "%Y-%m-%d").timestamp())
    except ValueError:
        return None  # Invalid date format

def parse_cascade_line(line):
    """Parses a single line of the APS dataset into structured dictionary format."""
    parts = line.strip().split("\t")
    if len(parts) != 5:
        return None  # Skip malformed lines
    
    cascade_id = int(parts[0])
    original_user_id = int(parts[1])

    # Convert timestamp if it's in date format
    try:
        timestamp = int(parts[2])  # Try to parse it as an integer first
    except ValueError:
        timestamp = convert_to_unix_timestamp(parts[2])  # Convert date to timestamp
        if timestamp is None:
            return None  # Skip if timestamp conversion fails

    num_participants = int(parts[3])
    
    participants_data = parts[4].split(" ")
    participants = []
    
    for entry in participants_data:
        if ":" in entry:
            path, time = entry.split(":")
            participants.append({"path": path, "time": int(time)})
    
    return {
        "cascade_id": cascade_id,
        "original_user_id": original_user_id,
        "timestamp": timestamp,
        "number_of_participants": num_participants,
        "participants": sorted(participants, key=lambda x: x["time"])  # Order participants by time
    }

def main():
    print("Reading dataset...")
    lines = read_txt_file(txt_file_path)
    
    print("Processing cascades...")
    cascades = []
    for line in lines:
        cascade = parse_cascade_line(line)
        if cascade:
            cascades.append(cascade)
        if len(cascades) >= n_cascades:
            break
    
    # Sort cascades by their original timestamp
    cascades_sorted = sorted(cascades, key=lambda x: x["timestamp"])
    
    print(f"Saving {len(cascades_sorted)} cascades to JSON...")
    with open(output_json_file, "w", encoding="utf-8") as f:
        json.dump(cascades_sorted, f, indent=4)
    
    print(f"Conversion complete. JSON saved as {output_json_file}")

if __name__ == "__main__":
    main()
