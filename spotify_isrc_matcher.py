import requests
import json
import time
from base64 import b64encode
from typing import List, Dict, Optional
from dataclasses import dataclass
import logging
from pathlib import Path
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class TrackInfo:
    isrc: str
    release_year: Optional[str]
    track_name: Optional[str]
    artist_name: Optional[str]
    album_name: Optional[str]
    error: Optional[str] = None

class SpotifyISRCMatcher:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.token_expires_at = 0
        self.session = requests.Session()
        
    def get_access_token(self) -> str:
        """Get or refresh the Spotify access token"""
        if self.access_token and time.time() < self.token_expires_at:
            return self.access_token
            
        auth_str = f"{self.client_id}:{self.client_secret}"
        auth_bytes = auth_str.encode('utf-8')
        auth_b64 = b64encode(auth_bytes).decode('utf-8')
        
        headers = {
            "Authorization": f"Basic {auth_b64}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data = {"grant_type": "client_credentials"}
        
        try:
            response = self.session.post(
                "https://accounts.spotify.com/api/token",
                headers=headers,
                data=data,
                timeout=10
            )
            response.raise_for_status()
            
            token_data = response.json()
            self.access_token = token_data["access_token"]
            # Set expiry time (subtract 60 seconds for safety)
            self.token_expires_at = time.time() + token_data.get("expires_in", 3600) - 60
            
            logger.info("Successfully obtained access token")
            return self.access_token
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get access token: {e}")
            raise
            
    def get_track_info(self, isrc: str) -> TrackInfo:
        """Get track information from ISRC"""
        try:
            token = self.get_access_token()
            
            url = "https://api.spotify.com/v1/search"
            headers = {"Authorization": f"Bearer {token}"}
            params = {
                "q": f"isrc:{isrc}",
                "type": "track",
                "limit": 1
            }
            
            response = self.session.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if not data.get('tracks', {}).get('items'):
                return TrackInfo(
                    isrc=isrc,
                    release_year=None,
                    track_name=None,
                    artist_name=None,
                    album_name=None,
                    error="Track not found"
                )
            
            track = data['tracks']['items'][0]
            album = track.get('album', {})
            artists = track.get('artists', [])
            
            # Extract release year from date (format: YYYY-MM-DD or YYYY)
            release_date = album.get('release_date', '')
            release_year = release_date[:4] if release_date else None
            
            return TrackInfo(
                isrc=isrc,
                release_year=release_year,
                track_name=track.get('name'),
                artist_name=artists[0].get('name') if artists else None,
                album_name=album.get('name'),
                error=None
            )
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed for ISRC {isrc}: {e}")
            return TrackInfo(
                isrc=isrc,
                release_year=None,
                track_name=None,
                artist_name=None,
                album_name=None,
                error=f"API Error: {str(e)}"
            )
        except (KeyError, IndexError, ValueError) as e:
            logger.error(f"Data parsing error for ISRC {isrc}: {e}")
            return TrackInfo(
                isrc=isrc,
                release_year=None,
                track_name=None,
                artist_name=None,
                album_name=None,
                error=f"Data Error: {str(e)}"
            )
    
    def process_isrc_list(self, isrc_list: List[str], delay: float = 0.1) -> List[TrackInfo]:
        """Process a list of ISRCs with rate limiting"""
        results = []
        total = len(isrc_list)
        
        logger.info(f"Processing {total} ISRCs...")
        
        for i, isrc in enumerate(isrc_list, 1):
            logger.info(f"Processing {i}/{total}: {isrc}")
            
            track_info = self.get_track_info(isrc)
            results.append(track_info)
            
            # Rate limiting - be respectful to Spotify's API
            if i < total:
                time.sleep(delay)
        
        return results
    
    def save_results_to_csv(self, results: List[TrackInfo], filename: str = "spotify_isrc_results.csv"):
        """Save results to CSV file"""
        import csv
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['isrc', 'release_year', 'track_name', 'artist_name', 'album_name', 'error']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for track_info in results:
                writer.writerow({
                    'isrc': track_info.isrc,
                    'release_year': track_info.release_year,
                    'track_name': track_info.track_name,
                    'artist_name': track_info.artist_name,
                    'album_name': track_info.album_name,
                    'error': track_info.error
                })
        
        logger.info(f"Results saved to {filename}")
    
    def save_results_to_json(self, results: List[TrackInfo], filename: str = "spotify_isrc_results.json"):
        """Save results to JSON file"""
        data = []
        for track_info in results:
            data.append({
                'isrc': track_info.isrc,
                'release_year': track_info.release_year,
                'track_name': track_info.track_name,
                'artist_name': track_info.artist_name,
                'album_name': track_info.album_name,
                'error': track_info.error
            })
        
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=2, ensure_ascii=False)
        
        logger.info(f"Results saved to {filename}")

    def save_results_to_excel(self, results: List[TrackInfo], filename: str = "spotify_isrc_results.xlsx"):
        """Save results to Excel file with formatting"""
        try:
            # Prepare data
            data = []
            for track_info in results:
                row = {
                    'ISRC': track_info.isrc,
                    'Release Year': track_info.release_year,
                    'Track Name': track_info.track_name,
                    'Artist Name': track_info.artist_name,
                    'Album Name': track_info.album_name,
                    'Status': 'Success' if track_info.error is None else 'Failed',
                    'Error': track_info.error if track_info.error else ''
                }
                data.append(row)
            
            # Create DataFrame and save
            df = pd.DataFrame(data)
            
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Results', index=False)
                
                # Format the sheet
                workbook = writer.book
                worksheet = writer.sheets['Results']
                
                # Auto-adjust column widths
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
            
            logger.info(f"Results saved to Excel file: {filename}")
            
        except ImportError:
            logger.warning("pandas/openpyxl not installed. Install with: pip install pandas openpyxl")
            logger.info("Falling back to CSV format...")
            self.save_results_to_csv(results, filename.replace('.xlsx', '.csv'))
        except Exception as e:
            logger.error(f"Error saving Excel file: {e}")
            raise

def main():
    # Load configuration
    config = load_config()
    
    # Example ISRCs - replace with your actual list
    isrc_list = [
        "USUG11904257",  # Blinding Lights - The Weeknd
        "GBUM71029604",  # Someone Like You - Adele
        "USUM71703861",  # Shape of You - Ed Sheeran
        "INVALID_ISRC",  # Test invalid ISRC
    ]
    
    # Initialize matcher
    matcher = SpotifyISRCMatcher(config['client_id'], config['client_secret'])
    
    # Process ISRCs
    results = matcher.process_isrc_list(isrc_list)
    
    # Display results
    print("\n" + "="*80)
    print("RESULTS")
    print("="*80)
    
    for track_info in results:
        if track_info.error:
            print(f"❌ {track_info.isrc}: {track_info.error}")
        else:
            print(f"✅ {track_info.isrc}: {track_info.release_year}")
            print(f"   Track: {track_info.track_name}")
            print(f"   Artist: {track_info.artist_name}")
            print(f"   Album: {track_info.album_name}")
        print("-" * 40)
    
    # Save results
    matcher.save_results_to_csv(results)
    matcher.save_results_to_json(results)
    matcher.save_results_to_excel(results)  # Add Excel output
    
    # Statistics
    successful = sum(1 for r in results if r.error is None)
    failed = len(results) - successful
    print(f"\n📊 Statistics:")
    print(f"   Successful: {successful}")
    print(f"   Failed: {failed}")
    print(f"   Total: {len(results)}")

def load_config() -> Dict[str, str]:
    """Load configuration from config.json or environment variables"""
    config_file = Path("config.json")
    
    if config_file.exists():
        with open(config_file, 'r') as f:
            config = json.load(f)
            return config
    
    # Fallback to environment variables
    import os
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        raise ValueError(
            "Spotify credentials not found. Please create a config.json file "
            "or set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET environment variables."
        )
    
    return {
        'client_id': client_id,
        'client_secret': client_secret
    }

if __name__ == "__main__":
    main()
