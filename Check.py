import os
import pandas as pd

# Define your base paths
base_folder = '/path/to/main/folders'
reports_folder = '/path/to/reports/folder'

# Load IDs, critical IDs, and reference object info from external tables
reference_df = pd.read_excel('/path/to/reference_table.xlsx')
critical_df = pd.read_excel('/path/to/critical_files_table.xlsx')
critical_ids = set(critical_df['Id'].astype(str))

# Initialize result DataFrame
columns = ['Id', 'Critical File', 'Link to Folder', 'Critical Link to Report',
           'Total Files', '#Excel Files', '#Docx Files', '#PDF Files', '#Other Files', 'Reference Obj', 'Color']
results = []

for idx, row in reference_df.iterrows():
    folder_id = str(row['Id'])
    folder_path = os.path.join(base_folder, folder_id)

    # Initialize counters
    excel_files = docx_files = pdf_files = other_files = 0

    # Check if folder exists
    if os.path.exists(folder_path):
        files = os.listdir(folder_path)
        total_files = len(files)

        for file in files:
            if file.lower().endswith('.xlsx'):
                excel_files += 1
            elif file.lower().endswith('.docx'):
                docx_files += 1
            elif file.lower().endswith('.pdf'):
                pdf_files += 1
            else:
                other_files += 1

        link_to_folder = f'=HYPERLINK("{folder_path}", "Link")'
    else:
        total_files = 0
        link_to_folder = 'Folder missing'

    # Check critical file
    critical_file = 'Y' if folder_id in critical_ids else 'N'

    # Critical report link
    critical_report_link = ''
    if critical_file == 'Y':
        for root, dirs, files in os.walk(reports_folder):
            if folder_id in dirs:
                critical_report_link = f'=HYPERLINK("{os.path.join(root, folder_id)}", "Report")'
                break

    # Determine color based on conditions
    if critical_file == 'Y' and total_files == 0:
        color = 'Red'
    elif critical_file == 'Y' and total_files < 3:
        color = 'Yellow'
    elif critical_file == 'Y':
        color = 'Green'
    else:
        color = 'Yellow' if total_files < 3 else 'Green'

    results.append([
        folder_id, critical_file, link_to_folder, critical_report_link, total_files,
        excel_files, docx_files, pdf_files, other_files, row['Reference Obj'], color
    ])

# Create DataFrame
results_df = pd.DataFrame(results, columns=columns)

# Save to Excel
results_df.to_excel('/path/to/output/report.xlsx', index=False)


