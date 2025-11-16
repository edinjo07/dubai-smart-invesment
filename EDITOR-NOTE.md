# Editor Page - Known Issue

## Current Status
The editor page (`editor.html`) allows you to make changes through a visual interface, but these changes are **NOT automatically reflected** on the main website.

## Why This Happens
The editor saves changes to:
1. A backend API endpoint (`/api/website/update`)
2. Which stores data in `website_config.json`

However, the main website (`index.html`) is a **static HTML file** that doesn't read from this config file.

## Solutions

### Option 1: Manual Updates (Current)
Make changes directly to:
- `index.html` - Main website file
- `public_site/index.html` - Public site version

This is what we've been doing (adding logo, removing phone numbers, etc.)

### Option 2: Template System (Recommended for Dynamic Updates)
To make the editor functional, you would need to:

1. **Convert to Template Engine**
   - Use Jinja2 templates (Flask's template engine)
   - Move `index.html` to `templates/index.html`
   - Replace static content with variables: `{{ site.title }}`, `{{ site.email }}`, etc.

2. **Update Flask Routes**
   ```python
   @app.route('/')
   def index():
       config = load_website_config()  # Load from website_config.json
       return render_template('index.html', config=config)
   ```

3. **Update Editor**
   - Changes saved via editor → `website_config.json`
   - Flask reads config → renders template with new values
   - Website updates automatically

### Option 3: Static Site Generator
Use a build process that generates HTML from the config file:
- Editor saves to `website_config.json`
- Run a build script that generates `index.html` from template + config
- Deploy the generated HTML

## Current Workaround
For now, to update the website:
1. Make changes directly in the HTML files
2. Commit and push to GitHub
3. Render will automatically deploy

## Files to Edit Directly
- **Main site**: `c:\My Web Sites\dubai-smart-invest\index.html`
- **Public site**: `c:\My Web Sites\dubai-smart-invest\public_site\index.html`
- **Styles**: Inline in `<style>` tags within HTML files
- **Content**: HTML content within the files

## Note
The editor page is useful for:
- Previewing potential changes
- Testing design variations
- Planning updates

But actual implementation requires manual HTML edits or implementing one of the solutions above.
