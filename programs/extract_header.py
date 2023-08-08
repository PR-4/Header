import pandas as pd
import lasio
import os


def header_extractor(directory_path, output_path):
    '''
    Function to read LAS files, extract the headers from the 'Well' section,
    and save the data to both .xlsx and .csv files in the specified output_path.
    '''
    files_processed = 0  # counter

    # Loop for each .las file
    for file in os.listdir(directory_path):
        if file.endswith('.las'):
            las = lasio.read(os.path.join(directory_path, file))

            # Extract data from the 'Well' section
            well_data = {}
            for item in las.sections['Well']:
                # Check for missing values and replace if you want
                mnemonic = item.mnemonic
                value = item.value if item.value != 'NULL' else '-9999' # Replace the N/A with -9999 (or any other)
                unit = item.unit if item.unit != 'NULL' else '-9999' # Replace the N/A with -9999 (or any other)
                descr = item.descr if item.descr != 'NULL' else '-9999' # Replace the N/A with -9999 (or any other)

                well_data[item.mnemonic] = [mnemonic, value, unit, descr]

            # Create a DF
            df = pd.DataFrame(well_data).T # T switch's rows and columns
            df.columns = ['Mnemonic', 'Value', 'Unit', 'Description']

            # Save DF to a .xlsx file
            xlsx_file_name = os.path.splitext(file)[0] + '_header.xlsx'
            output_file_path = os.path.join(output_path, xlsx_file_name)
            df.to_excel(output_file_path, index=False)

            # Save the DF to a CSV file
            #csv_file_name = os.path.splitext(file)[0] + '_header.csv'
            #output_file_path = os.path.join(output_path, csv_file_name)
            #df.to_csv(output_file_path, index=False)

            files_processed += 1  # counter + one

    print(f"Total files processed: {files_processed}")

# Paths
directory_path = r'C:\Documentos\Github\Header\input'
output_path = r'..Header/outputs'

# Call the function to save in both formats
header_extractor(directory_path, output_path)
