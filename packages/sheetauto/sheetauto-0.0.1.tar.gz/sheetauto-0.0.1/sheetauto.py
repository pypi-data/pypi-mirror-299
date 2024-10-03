import os
import shutil
import pandas as pd
import win32com.client as win32
from PIL import ImageGrab
import logging

# Use the logger defined in the package
logger = logging.getLogger(__name__)

# Function 1: pandas2excel
def read_data(source_path, file_type, **kwargs):
    """
    Read data from various file types supported by pandas (csv, excel, sql, json).
    """
    try:
        if file_type == 'csv':
            return pd.read_csv(source_path, **kwargs)
        elif file_type == 'excel':
            return pd.read_excel(source_path, **kwargs)
        elif file_type == 'json':
            return pd.read_json(source_path, **kwargs)
        elif file_type == 'sql':
            return pd.read_sql(source_path, **kwargs)
        else:
            logger.error(f"Unsupported file type: {file_type}")
            return None
    except Exception as e:
        logger.exception(f"Error reading data from {source_path}: {e}")
        return None

def pandas2excel(template_path, destination_path, source_paths, file_types, sheet_name='raw_data', cell_ranges=None, **kwargs):
    """
    Insert data from multiple source files (CSV, Excel, JSON, SQL) into an Excel file.
    
    - source_paths: List of paths to source files.
    - file_types: List of file types (e.g., 'csv', 'excel', 'json', 'sql') corresponding to the source files.
    - cell_ranges: List of starting cells (e.g., 'A1', 'B1') where data should be inserted.
    - kwargs: Additional arguments for data reading functions (e.g., separator for CSV).
    """
    try:
        # Step 1: Copy the template to a new location using shutil
        shutil.copy(template_path, destination_path)

        if not os.path.exists(destination_path):
            logger.error(f"Error: {destination_path} not found.")
            return
        else:
            logger.info(f"File {destination_path} copied successfully.")

        # Step 2: Open the copied template Excel file using win32com
        excel = win32.Dispatch("Excel.Application")
        excel.Visible = False  # Run Excel in the background

        # Open the workbook and select the sheet
        workbook = excel.Workbooks.Open(destination_path)
        sheet = workbook.Sheets(sheet_name)

        # Step 3: Loop through each source path and corresponding range
        if len(source_paths) != len(cell_ranges):
            logger.error("Mismatch between number of source files and cell ranges.")
            return

        for idx, (source_path, file_type, cell_range) in enumerate(zip(source_paths, file_types, cell_ranges)):
            logger.info(f"Processing {source_path} into range {cell_range}")
            
            # Read data based on file type
            df = read_data(source_path, file_type, **kwargs)

            if df is not None:
                # Step 4: Write the DataFrame to the Excel sheet starting from the specified range
                row_start, col_start = int(cell_range[1:]), ord(cell_range[0].upper()) - ord('A') + 1
                
                for row_idx, row in enumerate(df.values.tolist(), start=row_start):
                    for col_idx, value in enumerate(row, start=col_start):
                        sheet.Cells(row_idx, col_idx).Value = value

        # Save and close the workbook
        workbook.Save()
        workbook.Close()

        logger.info(f"Data from {', '.join(source_paths)} inserted into {destination_path}.")

    except Exception as e:
        logger.exception(f"Error while working with Excel: {e}")
    finally:
        excel.Quit()

# Function 2: excel2img
def excel2img(excel_file_path, sheet_name, cell_ranges, visible=False, base_path=None, output_image_path=None):
    if base_path is None:
        base_path = os.getcwd()

    try:
        logger.info("Starting Excel to Image conversion...")

        # Get the Excel file name (without extension) for default image naming
        excel_file_name = os.path.splitext(os.path.basename(excel_file_path))[0]

        # Open Excel
        excel = win32.Dispatch("Excel.Application")
        excel.Visible = visible  # Control Excel visibility

        # Open the workbook
        logger.debug(f"Opening workbook: {excel_file_path}")
        workbook = excel.Workbooks.Open(excel_file_path)
        sheet = workbook.Sheets(sheet_name)

        # Handle single or multiple ranges
        if isinstance(cell_ranges, str):
            cell_ranges = [cell_ranges]  # Convert to list if a single range is passed

        # Loop through the ranges and copy them as a picture
        for index, cell_range in enumerate(cell_ranges):
            logger.debug(f"Copying range {cell_range} from sheet {sheet_name}")
            range_to_copy = sheet.Range(cell_range)
            range_to_copy.CopyPicture(Format=win32.constants.xlBitmap)

            # Grab the image from the clipboard using PIL
            image = ImageGrab.grabclipboard()

            # Save the image if it exists in the clipboard
            if isinstance(image, ImageGrab.Image.Image):
                # Set default output image path if not provided
                if output_image_path is None:
                    output_image_name = f"{excel_file_name}_{cell_range.replace(':', '_')}.png"
                else:
                    output_image_name = output_image_path
                    if len(cell_ranges) > 1:  # Modify the name if processing multiple ranges
                        output_image_name = f"{os.path.splitext(output_image_path)[0]}_{cell_range.replace(':', '_')}.png"

                output_image_full_path = os.path.join(base_path, output_image_name)
                image.save(output_image_full_path, 'PNG')
                logger.info(f"Image saved to {output_image_full_path}")
            else:
                logger.error("No image found in the clipboard. Ensure the range was copied correctly.")

        # Clean up
        workbook.Close(SaveChanges=False)
        excel.Quit()

    except Exception as e:
        logger.exception(f"An error occurred while converting Excel to image: {e}")
        raise  # Reraise the exception for the user to handle if needed


#excel2ppt

#excel2word

#pandas2excel

#excel2excel

#excel2smtp

#excel2excel

# excel2pdf