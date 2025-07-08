# Spotify ISRC Matcher 🎵

A simple tool to match ISRCs (International Standard Recording Codes) with Spotify track information and extract release years, track names, artist names, and album names.

## 🎯 What This Tool Does

- **Input**: Excel file with ISRCs
- **Output**: Excel file with track details (release year, track name, artist, album)
- **Handles**: Invalid ISRCs gracefully with error messages
- **Formats**: Beautiful Excel output with color-coded results

## 📋 Prerequisites

- **Windows 10/11** (works on Mac/Linux too)
- **Python 3.8+** (we'll help you install this)
- **Spotify Developer Account** (free - we'll show you how)

## 🚀 Quick Start (5 minutes)

### Step 1: Get Spotify API Credentials
1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Log in with your Spotify account (or create one - it's free)
3. Click "Create App"
4. Fill in:
   - **App Name**: "ISRC Matcher"
   - **Description**: "Tool to match ISRCs with track info"
   - **Redirect URI**: `https://localhost:8888/callback`
5. Click "Save"
6. Copy your **Client ID** and **Client Secret** (keep these private!)

### Step 2: Download and Setup
1. **Download this project**:
   - Click the green "Code" button above
   - Choose "Download ZIP"
   - Extract to a folder like `C:\spotify-isrc-project`

2. **Run the setup script**:
   - Open the extracted folder
   - Double-click `setup.bat`
   - Follow the prompts to enter your Spotify credentials

### Step 3: Run the Tool
1. **Double-click** `run_program.bat`
2. **Follow the prompts**:
   - Enter path to your Excel file with ISRCs
   - Enter the column name containing ISRCs (usually "ISRC")
   - Choose output file name
3. **Done!** Your results will be saved as an Excel file

## 📁 Excel File Format

Your Excel file should have ISRCs in a column. Example:

| ISRC          | Song Title    | Artist      |
|---------------|---------------|-------------|
| USUG11904257  | Blinding Lights | The Weeknd |
| GBUM71029604  | Someone Like You | Adele     |
| USUM71703861  | Shape of You  | Ed Sheeran  |

## 📊 Output

The tool creates an Excel file with:
- **Results Sheet**: All track details with color-coded success/failure
- **Metadata Sheet**: Processing statistics and error summaries
- **Summary Sheets**: Year distribution and top artists

## 🛠️ Advanced Usage

If you're comfortable with command line:
```bash
# Activate virtual environment
.venv\Scripts\activate

# Run the interactive program
python excel_runner.py

# Or run with specific parameters
python excel_processor.py
```

## 🆘 Troubleshooting

### "Python not found"
- Install Python from [python.org](https://www.python.org/downloads/)
- Make sure to check "Add Python to PATH" during installation

### "Module not found"
- Run `setup.bat` again to install dependencies

### "Invalid credentials"
- Check your `config.json` file has the correct Client ID and Secret
- Make sure there are no extra spaces or quotes

### "No ISRCs found"
- Check your column name is correct (case-sensitive)
- Make sure your Excel file has the right format

## 📞 Support

If you need help:
1. Check the error messages in the terminal
2. Look at the log files created in the project folder
3. Make sure your Spotify credentials are correct

## 🔧 Technical Details

- **Language**: Python 3.8+
- **Dependencies**: requests, pandas, openpyxl
- **API**: Spotify Web API (Client Credentials Flow)
- **Rate Limiting**: 100ms delay between requests
- **Output Formats**: Excel (.xlsx), CSV, JSON

## 📝 License

This project is for personal/educational use. Please respect Spotify's API terms of service.

---

**Happy ISRC matching! 🎵**

1. **Get Spotify API Credentials**:
   - Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
   - Create a new app
   - Copy your Client ID and Client Secret

2. **Configure Credentials**:
   - Edit `config.json` with your credentials:
   ```json
   {
     "client_id": "your_actual_client_id",
     "client_secret": "your_actual_client_secret"
   }
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Option 1: Excel Processing (Recommended)
For the easiest Excel workflow:
```bash
python excel_runner.py
```

### Option 2: Advanced Excel Processing
```python
from excel_processor import ExcelISRCProcessor

# Process Excel file
processor = ExcelISRCProcessor(client_id, client_secret)
results = processor.process_excel_file('your_isrcs.xlsx', 'output_results.xlsx')
```

### Option 3: Basic Script
```bash
python spotify_isrc_matcher.py
```

## Features

- **Excel Integration**: Read ISRCs from Excel files and save formatted results
- **Robust Error Handling**: Handles API errors, network issues, and invalid ISRCs
- **Rate Limiting**: Respects Spotify's API rate limits
- **Token Management**: Automatically refreshes access tokens
- **Multiple Output Formats**: Saves results to CSV, JSON, and Excel with formatting
- **Detailed Logging**: Comprehensive logging for debugging
- **Rich Data**: Returns track name, artist, album, and release year
- **Configuration Management**: Supports config files and environment variables

## Improvements Over Basic Version

1. **Object-Oriented Design**: Cleaner, more maintainable code
2. **Proper Error Handling**: Catches and handles various error types
3. **Rate Limiting**: Prevents API abuse
4. **Token Management**: Handles token expiration automatically
5. **Data Validation**: Validates responses and handles edge cases
6. **Output Options**: Multiple file formats for results
7. **Logging**: Proper logging for monitoring and debugging
8. **Configuration**: Flexible configuration management
9. **Rich Data**: Returns additional track information
10. **Type Hints**: Better code documentation and IDE support

## Example Output

```
Processing 4 ISRCs...
Processing 1/4: USUG11904257
Processing 2/4: GBUM71029604
Processing 3/4: USUM71703861
Processing 4/4: INVALID_ISRC

================================================================================
RESULTS
================================================================================
✅ USUG11904257: 2019
   Track: Blinding Lights
   Artist: The Weeknd
   Album: After Hours
----------------------------------------
✅ GBUM71029604: 2011
   Track: Someone Like You
   Artist: Adele
   Album: 21
----------------------------------------
✅ USUM71703861: 2017
   Track: Shape of You
   Artist: Ed Sheeran
   Album: ÷ (Deluxe)
----------------------------------------
❌ INVALID_ISRC: Track not found
----------------------------------------

📊 Statistics:
   Successful: 3
   Failed: 1
   Total: 4
```

## Excel File Format

Your input Excel file should have a column containing ISRCs. The script will automatically detect columns named:
- `ISRC`
- `isrc`
- `ISRC_CODE`
- `Code`

Example Excel structure:
```
| ISRC          | Song Title      | Artist        | Notes           |
|---------------|-----------------|---------------|-----------------|
| USUG11904257  | Blinding Lights | The Weeknd    | Popular hit     |
| GBUM71029604  | Someone Like You| Adele         | Classic ballad  |
| USUM71703861  | Shape of You    | Ed Sheeran    | Chart topper    |
```

## Output Excel Format

The output Excel file contains multiple sheets:
1. **Results**: Main data with ISRC, release year, track info, and status
2. **Year Distribution**: Breakdown of tracks by release year
3. **Top Artists**: Most frequent artists in your dataset
4. **Metadata**: Processing information and error summary

## File Structure

```
spotify-isrc-project/
├── spotify_isrc_matcher.py      # Main script
├── excel_processor.py           # Excel-specific functionality
├── excel_runner.py              # Simple Excel workflow
├── example_file_processing.py   # Example for various file formats
├── config.json                  # Configuration file
├── requirements.txt             # Python dependencies
├── README.md                   # This file
├── sample_isrcs.xlsx            # Sample Excel file (generated)
├── spotify_results.xlsx         # Excel output (generated)
├── spotify_isrc_results.csv    # CSV output (generated)
└── spotify_isrc_results.json   # JSON output (generated)
```

## Environment Variables

Instead of using `config.json`, you can set environment variables:
- `SPOTIFY_CLIENT_ID`
- `SPOTIFY_CLIENT_SECRET`

## Notes

- The script includes rate limiting (100ms delay between requests by default)
- Results are saved to both CSV and JSON formats
- Invalid ISRCs are handled gracefully
- The script uses session management for better performance
- Token refresh is handled automatically
