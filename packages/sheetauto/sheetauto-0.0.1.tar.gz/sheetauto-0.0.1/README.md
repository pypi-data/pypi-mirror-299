
# Sheet Automation Tool

The **Sheet Automation Tool** is a Python package that allows users to automate the process of extracting data from multiple sources (CSV, SQL, Excel, JSON, etc.) and inserting them into specific cell ranges of an Excel workbook. This tool is designed to handle complex data workflows and provides flexible configuration options to adapt to various input types.

## Key Features

- **Support for Multiple Input Formats**: CSV, SQL databases, Excel sheets, and JSON files.
- **Customizable Parameters**: Set CSV delimiters, select specific Excel sheets, and define SQL queries.
- **Flexible Data Mapping**: Assign data to specific Excel cell ranges for easier reporting.
- **Automated Excel Output**: Consolidate data from various sources into a single Excel workbook with minimal effort.

## Requirements

- Python 3.7 or higher
- Pandas
- os
- shutil
- pywin32
- Pillow
- logging

## Installation

To install the package, you need to clone the repository and install the dependencies.

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/sheetauto.git
```

### Step 2: Navigate to the Project Directory

```bash
cd sheetauto
```

### Step 3: Install Dependencies

The package relies on Pandas for data processing and Openpyxl or Xlwings for Excel manipulation. To install the dependencies, use:

```bash
pip install -r requirements.txt
```

Alternatively, you can install them manually:

```bash
pip install pandas os shutil pandas pywin32 Pillow logging
```

### Step 4: Import and Use the Package

Once installed, you can use the package in your Python scripts.

## Usage

The **Sheet Automation Tool** is designed to be highly configurable. The main idea is to specify input sources, their parameters, and the ranges where data should be placed in an Excel file.

Here's a full example demonstrating how to use the tool:

```python
from sheetauto import SheetAutomation

# Define your input files and their mapping to Excel ranges
config = {
    'sources': [
        {'type': 'csv', 'filepath': 'data1.csv', 'separator': ',', 'range': 'A1:C10'},
        {'type': 'json', 'filepath': 'data2.json', 'range': 'D1:F10'},
        {'type': 'sql', 'query': 'SELECT * FROM employees', 'range': 'G1:H10'}
    ],
    'destination': 'output.xlsx'
}

# Create a SheetAutomation object with the configuration
sheet_automation = SheetAutomation(config)

# Process files and generate the output Excel sheet
sheet_automation.process_files()
```

### Input Types and Parameters

1. **CSV**: For CSV files, you can specify the file path and the separator used in the file.
   ```python
   {'type': 'csv', 'filepath': 'data.csv', 'separator': ',', 'range': 'A1:C10'}
   ```
   - `filepath`: Path to the CSV file.
   - `separator`: Optional, defaults to `,`.

2. **SQL**: For SQL data, you can specify the query and the database connection.
   ```python
   {'type': 'sql', 'query': 'SELECT * FROM table', 'connection': 'mysql://user:pass@localhost/db', 'range': 'D1:F10'}
   ```
   - `query`: SQL query to fetch the data.
   - `connection`: Connection string for the database.

3. **Excel**: You can load data from another Excel file by specifying the file path and the sheet.
   ```python
   {'type': 'excel', 'filepath': 'data.xlsx', 'sheet_name': 'Sheet1', 'range': 'G1:H10'}
   ```
   - `filepath`: Path to the Excel file.
   - `sheet_name`: The sheet from which data should be loaded.

4. **JSON**: For JSON files, specify the file path and the target range.
   ```python
   {'type': 'json', 'filepath': 'data.json', 'range': 'I1:J10'}
   ```

### Configuration Options

Each input type has specific configuration options. The key option is the **range**, which specifies where the data should be placed in the Excel file.

Example Configuration:

```python
config = {
    'sources': [
        {'type': 'csv', 'filepath': 'data1.csv', 'separator': ',', 'range': 'A1:C10'},
        {'type': 'sql', 'query': 'SELECT * FROM my_table', 'range': 'D1:F10'},
        {'type': 'excel', 'filepath': 'data2.xlsx', 'sheet_name': 'Sheet1', 'range': 'G1:I10'}
    ],
    'destination': 'output.xlsx'
}
```

In this configuration:
- CSV data from `data1.csv` is placed into `A1:C10`.
- SQL query results are written into `D1:F10`.
- Excel data from `data2.xlsx` is inserted into `G1:I10`.

## Error Handling and Troubleshooting

If an error occurs during the data processing, the tool provides meaningful error messages that help identify the issue. For example:

- **File not found**: If a file cannot be found at the specified path, the tool will raise a `FileNotFoundError`.
- **Database connection error**: If there's an issue connecting to a database, an appropriate connection error will be shown.
- **Excel range conflict**: If data exceeds the specified range, a warning is raised.

### Common Errors

1. **FileNotFoundError**: Make sure all input file paths are correct and accessible.
2. **Invalid SQL Query**: Ensure your SQL query syntax is correct and valid for your database.
3. **Excel File Not Writable**: Check if the destination Excel file is open in another program.

## Advanced Features

### Processing Large Data Files

For processing large datasets, it’s recommended to use a combination of **SQL** input types and **pandas** for memory-efficient handling.

### Mapping Multiple Sheets

You can specify the destination Excel workbook to contain multiple sheets. Just add `sheet_name` to your configuration for the destination.

```python
{
    'sources': [{'type': 'csv', 'filepath': 'data.csv', 'separator': ',', 'range': 'A1:C10'}],
    'destination': {'filepath': 'output.xlsx', 'sheet_name': 'Sheet1'}
}
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue on GitHub.

### How to Contribute

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## MIT License

```markdown
MIT License

Copyright (c) 2024 Lingga Aji Andika

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
