"""
Simple Excel-focused script for Spotify ISRC matching
Perfect for users who just want to process Excel files quickly
"""

import json
import logging
from pathlib import Path
from excel_processor import ExcelISRCProcessor, create_sample_excel

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Main function for Excel processing"""
    
    print("🎵 Spotify ISRC Excel Processor 🎵")
    print("=" * 50)
    
    # Load configuration
    config_path = Path("config.json")
    if not config_path.exists():
        print("❌ config.json not found!")
        print("Please create config.json with your Spotify API credentials:")
        print("""
{
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET"
}
        """)
        return
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        return
    
    # Check if credentials are set
    if config.get('client_id') == 'YOUR_CLIENT_ID' or config.get('client_secret') == 'YOUR_CLIENT_SECRET':
        print("❌ Please update config.json with your actual Spotify API credentials")
        return
    
    # Get input file
    input_file = input("\n📁 Enter path to Excel file with ISRCs (or press Enter for sample): ").strip()
    
    if not input_file:
        # Create and use sample file
        print("Creating sample Excel file...")
        input_file = create_sample_excel()
        print(f"✅ Sample file created: {input_file}")
    
    # Check if file exists
    if not Path(input_file).exists():
        print(f"❌ File not found: {input_file}")
        return
    
    # Get column name
    column_name = input("📋 Enter ISRC column name (or press Enter for 'ISRC'): ").strip()
    if not column_name:
        column_name = 'ISRC'
    
    # Get header row
    header_row_input = input("🔢 Enter header row number (or press Enter for row 1): ").strip()
    if not header_row_input:
        header_row = 0  # Row 1 in Excel = index 0 in pandas
    else:
        try:
            header_row = int(header_row_input) - 1  # Convert to 0-indexed
            if header_row < 0:
                header_row = 0
        except ValueError:
            print("Invalid row number, using row 1")
            header_row = 0
    
    # Get output file
    output_file = input("💾 Enter output file name (or press Enter for auto-generated): ").strip()
    if not output_file:
        input_path = Path(input_file)
        output_file = str(input_path.parent / f"{input_path.stem}_spotify_results.xlsx")
    
    # Get sheet name
    sheet_name = input("📄 Enter sheet name (or press Enter for first sheet): ").strip()
    if not sheet_name:
        sheet_name = None
    
    print(f"\n🔄 Processing...")
    print(f"   Input: {input_file}")
    print(f"   Output: {output_file}")
    print(f"   Column: {column_name}")
    print(f"   Header Row: {header_row + 1}")
    print(f"   Sheet: {sheet_name or 'First sheet'}")
    
    try:
        # Initialize processor
        processor = ExcelISRCProcessor(config['client_id'], config['client_secret'])
        
        # Process the file
        results = processor.process_excel_file(
            input_path=input_file,
            output_path=output_file,
            sheet_name=sheet_name,
            isrc_column=column_name,
            header_row=header_row,
            delay=0.1  # 100ms delay between requests
        )
        
        # Show results
        successful = sum(1 for r in results if r.error is None)
        failed = len(results) - successful
        
        print(f"\n✅ Processing Complete!")
        print(f"📊 Results:")
        print(f"   Total ISRCs: {len(results)}")
        print(f"   Successful: {successful}")
        print(f"   Failed: {failed}")
        print(f"   Success rate: {(successful / len(results) * 100):.1f}%")
        print(f"   Output saved to: {output_file}")
        
        # Show some examples
        if successful > 0:
            print(f"\n🎯 Sample successful results:")
            count = 0
            for result in results:
                if result.error is None and count < 3:
                    print(f"   {result.isrc} → {result.release_year} - {result.track_name} by {result.artist_name}")
                    count += 1
        
        if failed > 0:
            print(f"\n❌ Sample failed results:")
            count = 0
            for result in results:
                if result.error is not None and count < 3:
                    print(f"   {result.isrc} → {result.error}")
                    count += 1
    
    except Exception as e:
        print(f"❌ Error during processing: {e}")
        logger.error(f"Processing error: {e}")

if __name__ == "__main__":
    main()
