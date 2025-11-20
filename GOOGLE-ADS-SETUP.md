# Google Ads Conversion Tracking Setup

## Current Status
✅ Google Ads tracking code has been added to `index.html`
⚠️  You need to replace placeholder IDs with your actual Google Ads Conversion ID

## Where to Find Your Google Ads Conversion ID

### Step 1: Get Your Conversion ID
1. Go to Google Ads: https://ads.google.com
2. Click **Tools & Settings** (wrench icon) → **Measurement** → **Conversions**
3. Click **+ New Conversion Action**
4. Select **Website**
5. Choose **Contact form submission** or **Lead**
6. Fill in conversion details:
   - **Goal:** Generate leads
   - **Value:** Use the same value for each conversion (recommended)
   - **Count:** One (count only one conversion per click)
7. Click **Create and Continue**
8. Select **Use Google tag manager or add the tag manually**
9. Copy your Conversion ID and Label

Your conversion tracking will look like:
- **Conversion ID:** `AW-123456789`
- **Conversion Label:** `AbCdEfGhIjKlMnOp`

### Step 2: Update index.html

Find these two locations in `index.html` and replace the placeholders:

#### Location 1: Head section (around line 61-65)
```html
<!-- Replace AW-XXXXXXXXXX with your actual Conversion ID -->
<script async src="https://www.googletagmanager.com/gtag/js?id=AW-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'AW-XXXXXXXXXX'); <!-- Replace here -->
</script>
```

**Replace:**
- `AW-XXXXXXXXXX` with your actual Conversion ID (e.g., `AW-123456789`)

#### Location 2: Form submission (around line 2182-2187)
```javascript
gtag('event', 'conversion', {
    'send_to': 'AW-XXXXXXXXXX/YYYYYYYYYYYYYY', // Replace
    'value': 1.0,
    'currency': 'EUR'
});
```

**Replace:**
- `AW-XXXXXXXXXX/YYYYYYYYYYYYYY` with `AW-123456789/AbCdEfGhIjKlMnOp`
- Format: `ConversionID/ConversionLabel`

### Step 3: Test Your Conversion Tracking

1. **Install Google Tag Assistant Chrome Extension**
   - https://chrome.google.com/webstore (search "Tag Assistant")

2. **Test on your website:**
   - Visit https://dubaismartinvestment.com
   - Open Tag Assistant
   - Fill out and submit the contact form
   - Check if conversion fires in Tag Assistant

3. **Verify in Google Ads:**
   - Go to **Tools & Settings** → **Conversions**
   - Your conversion should show status: "Recording conversions"
   - Wait 24 hours to see data

## Example Configuration

If your Google Ads gave you:
- Conversion ID: `AW-987654321`
- Conversion Label: `Xz1a2B3c4D5e6F7g`

Your code should be:

```html
<!-- Head section -->
<script async src="https://www.googletagmanager.com/gtag/js?id=AW-987654321"></script>
<script>
  gtag('config', 'AW-987654321');
</script>

<!-- Form submission -->
gtag('event', 'conversion', {
    'send_to': 'AW-987654321/Xz1a2B3c4D5e6F7g',
    'value': 1.0,
    'currency': 'EUR'
});
```

## What Gets Tracked

✅ **Contact Form Submissions** - Every time someone submits the EOI form
✅ **Conversion Value** - Set to 1.0 EUR (you can adjust)
✅ **Lead Quality** - Google will optimize for quality leads

## Troubleshooting

### Conversion not showing in Google Ads?
1. Check Tag Assistant shows gtag firing
2. Wait 24 hours for data to appear
3. Verify Conversion ID and Label are correct
4. Make sure website is live (not localhost)

### Multiple conversions per user?
- Current setup counts ONE conversion per click
- User can only trigger conversion once per ad click

## After Setup

Once configured, you can:
- Track conversion rates in Google Ads
- Optimize campaigns for conversions
- Set up automated bidding strategies
- Create conversion-based audiences

## Need Help?

Contact Google Ads support or check:
- https://support.google.com/google-ads/answer/6331314
- https://support.google.com/tagmanager/answer/6107124
