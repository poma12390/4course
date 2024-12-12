import csv
import re
import sys
import os

def parse_text_to_csv(output_csv):
    input_lines = []
    while True:
        line = input()
        if line.strip() == "EOF":  # Special symbol to terminate input
            break
        input_lines.append(line)
    input_text = "\n".join(input_lines)

    # Extract TERMINATE value (1st column)
    terminate_match = re.search(r"ZYX\s+23\s+TERMINATE\s+(\d+)", input_text)
    terminate_value = terminate_match.group(1) if terminate_match else ""

    # Extract UTIL. for UZEL1 (2nd column)
    uzel1_util_match = re.search(r"UZEL1\s+\d+\s+([\d.]+)", input_text)
    uzel1_util_value = uzel1_util_match.group(1) if uzel1_util_match else ""

    # Extract UTIL. for UZEL2 (3rd column)
    uzel2_util_match = re.search(r"UZEL2\s+\d+\s+([\d.]+)", input_text)
    uzel2_util_value = uzel2_util_match.group(1) if uzel2_util_match else ""

    # Extract AVE.CONT. for BUF1 (4th column)
    buf1_ave_cont_match = re.search(r"BUF1\s+\d+\s+\d+\s+\d+\s+\d+\s+([\d.]+)", input_text)
    buf1_ave_cont_value = buf1_ave_cont_match.group(1) if buf1_ave_cont_match else ""

    # Extract AVE.CONT. for BUF2 (5th column)
    buf2_ave_cont_match = re.search(r"BUF2\s+\d+\s+\d+\s+\d+\s+\d+\s+([\d.]+)", input_text)
    buf2_ave_cont_value = buf2_ave_cont_match.group(1) if buf2_ave_cont_match else ""

    # Extract AVE.TIME for BUF1 (6th column)
    buf1_ave_time_match = re.search(r"BUF1\s+\d+\s+\d+\s+\d+\s+\d+\s+[\d.]+\s+([\d.]+)", input_text)
    buf1_ave_time_value = buf1_ave_time_match.group(1) if buf1_ave_time_match else ""

    # Extract AVE.TIME for BUF2 (7th column)
    buf2_ave_time_match = re.search(r"BUF2\s+\d+\s+\d+\s+\d+\s+\d+\s+[\d.]+\s+([\d.]+)", input_text)
    buf2_ave_time_value = buf2_ave_time_match.group(1) if buf2_ave_time_match else ""

    # Extract STD.DEV. for TU_BUF1 (8th column)
    tu_buf1_stddev_match = re.search(r"TU_BUF1\s+[\d.]+\s+([\d.]+)", input_text)
    tu_buf1_stddev_value = tu_buf1_stddev_match.group(1) if tu_buf1_stddev_match else ""

    # Extract STD.DEV. for TU_BUF2 (9th column)
    tu_buf2_stddev_match = re.search(r"TU_BUF2\s+[\d.]+\s+([\d.]+)", input_text)
    tu_buf2_stddev_value = tu_buf2_stddev_match.group(1) if tu_buf2_stddev_match else ""

    # Prepare new row
    new_row = [terminate_value, uzel1_util_value, uzel2_util_value, buf1_ave_cont_value, buf2_ave_cont_value, 
               buf1_ave_time_value, buf2_ave_time_value, tu_buf1_stddev_value, tu_buf2_stddev_value]

    # Replace '.' with ',' in all numeric values in the new_row list
    new_row = [value.replace('.', ',') if '.' in value else value for value in new_row]

    # Read existing content if the file exists
    if os.path.exists(output_csv):
        with open(output_csv, mode='r') as csv_file:
            csv_reader = list(csv.reader(csv_file, delimiter=';'))
            existing_rows = csv_reader if csv_reader else []
    else:
        existing_rows = []

    # Check if the header exists; add if missing
    header = ["TERMINATE", "UZEL1_UTIL", "UZEL2_UTIL", "BUF1_AVE_CONT", "BUF2_AVE_CONT", 
              "BUF1_AVE_TIME", "BUF2_AVE_TIME", "TU_BUF1_STD_DEV", "TU_BUF2_STD_DEV"]
    if not existing_rows or existing_rows[0] != header:
        existing_rows.insert(0, header)

    # Add the new row at the beginning (after the header)
    updated_rows = [existing_rows[0]] + [new_row] + existing_rows[1:]

    # Write updated content back to the file
    with open(output_csv, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';')  # Use semicolon as delimiter
        csv_writer.writerows(updated_rows)



# Example usage
output_csv = "output.csv"
parse_text_to_csv(output_csv)
