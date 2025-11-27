# Adding the MATCH Logo

## Quick Setup

1. **Save the logo image** as `match_logo.png` in the project root directory:
   ```
   homelessness_hackathon/
   ├── match_logo.png  ← Save logo here
   ├── app_voice.py
   ├── ...
   ```

2. **Restart the app**:
   ```bash
   streamlit run app_voice.py
   ```

3. The logo will appear centered below the GOV.UK header!

## Alternative: Use a URL

If you have the logo hosted online, you can use a URL instead:

Edit `app_voice.py` and replace the logo loading section with:

```python
# Add MATCH logo below header
st.markdown("""
<div style="text-align: center; padding: 1rem 0;">
    <img src="YOUR_LOGO_URL_HERE" alt="MATCH Logo" style="max-width: 400px; width: 100%;">
</div>
""", unsafe_allow_html=True)
```

## Fallback

If the logo file is not found, the app will display a text-based fallback:
- 🏠 MATCH
- Matching Accommodation to Community Households

## Logo Specifications

For best results:
- **Format**: PNG with transparent background
- **Size**: 800-1200px wide recommended
- **Aspect ratio**: Maintain original (approximately 3:1)
- **File size**: < 500KB for fast loading

## Current Implementation

The app currently:
1. Tries to load `match_logo.png` from the project root
2. Displays it centered below the GOV.UK header
3. Falls back to text if the file is not found
4. Scales responsively to fit the page width
