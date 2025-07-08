# 🚀 QUICK START GUIDE FOR YOUR BROTHER

## Super Simple Setup (5 minutes)

### 1. Get Spotify API Access (One-time setup)
1. Go to: https://developer.spotify.com/dashboard
2. Log in with Spotify (or create free account)
3. Click "Create App"
4. Fill in:
   - Name: "ISRC Matcher"
   - Description: "Match ISRCs with track info"
   - Redirect URI: `https://localhost:8888/callback`
5. Click Save
6. **Copy your Client ID and Client Secret** (keep these private!)

### 2. Download & Setup
1. **Download this project** from GitHub (click green "Code" button → "Download ZIP")
2. **Extract** to a folder like `C:\spotify-isrc-project`
3. **Double-click** `setup.bat` in the folder
4. **Enter your Spotify credentials** when prompted

### 3. Run the Program
1. **Double-click** `run_program.bat`
2. **Follow the prompts**:
   - Enter path to your Excel file
   - Enter ISRC column name (usually just "ISRC")
   - Choose output file name
3. **Done!** Results saved as Excel file

## 📁 Your Excel File Should Look Like:

| ISRC          | Song Title    | Artist      |
|---------------|---------------|-------------|
| USUG11904257  | Blinding Lights | The Weeknd |
| GBUM71029604  | Someone Like You | Adele     |
| USUM71703861  | Shape of You  | Ed Sheeran  |

## 📊 You'll Get Back:

Excel file with:
- ✅ **Track names, artists, albums, release years**
- ❌ **Clear error messages for invalid ISRCs**
- 📈 **Statistics and summaries**
- 🎨 **Color-coded results (green = success, red = failed)**

## 🆘 If Something Goes Wrong:

1. **"Python not found"** → Install Python from python.org (check "Add to PATH")
2. **"Invalid credentials"** → Double-check your Client ID/Secret
3. **"No ISRCs found"** → Check your column name (case-sensitive)
4. **Still stuck?** → Run `setup.bat` again

## 💡 Pro Tips:

- Keep your `config.json` file private (has your API keys)
- Works with any Excel file format (.xlsx, .xls)
- Can handle thousands of ISRCs (just takes longer)
- Rate-limited to be respectful to Spotify's API

**That's it! Happy ISRC matching! 🎵**
