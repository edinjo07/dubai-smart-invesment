# How to Add Custom Images to Your Dubai Real Estate Website

## 📁 **Folder Structure**

Your website now has a `static` folder for all images, CSS, and JavaScript files:

```
DUBAI REAL ESTATE/
├── static/
│   ├── images/          ← Put your images here
│   ├── css/             ← Put custom CSS files here
│   └── js/              ← Put custom JavaScript files here
├── index.html
├── admin.html
├── login.html
└── app.py
```

---

## 🖼️ **Method 1: Add Images to static/images Folder**

### **Step 1: Copy Your Images**
Place your images in the `static/images/` folder:

```
static/
  └── images/
      ├── logo.png
      ├── building.jpg
      ├── apartment-1.jpg
      ├── apartment-2.jpg
      ├── background.jpg
      └── banner.jpg
```

### **Step 2: Use Images in HTML**

In your HTML files (index.html, admin.html, login.html), reference images like this:

```html
<!-- Logo -->
<img src="/static/images/logo.png" alt="Le Blanc Dubai Logo">

<!-- Building Photo -->
<img src="/static/images/building.jpg" alt="Le Blanc Building">

<!-- Background Image -->
<div style="background-image: url('/static/images/background.jpg');">
    Content here
</div>

<!-- Multiple Images -->
<img src="/static/images/apartment-1.jpg" alt="Apartment 1">
<img src="/static/images/apartment-2.jpg" alt="Apartment 2">
```

### **Step 3: Example - Add Logo to Header**

Open `index.html` and add:

```html
<header>
    <img src="/static/images/logo.png" alt="Le Blanc Dubai" style="width: 200px;">
    <h1>Le Blanc Dubai Real Estate</h1>
</header>
```

### **Step 4: Example - Add Background Image**

In your HTML file, add to the style section:

```html
<style>
    body {
        background-image: url('/static/images/background.jpg');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
</style>
```

---

## 🎨 **Method 2: Using CSS for Images**

### **Create a custom CSS file:**

**File:** `static/css/custom.css`

```css
/* Logo */
.logo {
    background-image: url('/static/images/logo.png');
    width: 200px;
    height: 100px;
    background-size: contain;
    background-repeat: no-repeat;
}

/* Hero Section Background */
.hero {
    background-image: url('/static/images/banner.jpg');
    background-size: cover;
    background-position: center;
    height: 500px;
}

/* Property Images */
.property-card {
    background-image: url('/static/images/apartment-1.jpg');
    background-size: cover;
    width: 300px;
    height: 200px;
}
```

### **Link CSS in HTML:**

Add to the `<head>` section of your HTML files:

```html
<link rel="stylesheet" href="/static/css/custom.css">
```

---

## 📷 **Method 3: Image Gallery Example**

Here's a complete example for adding property images:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Le Blanc Dubai - Gallery</title>
    <style>
        .gallery {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            padding: 20px;
        }
        
        .gallery-item {
            overflow: hidden;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .gallery-item img {
            width: 100%;
            height: 250px;
            object-fit: cover;
            transition: transform 0.3s;
        }
        
        .gallery-item img:hover {
            transform: scale(1.05);
        }
    </style>
</head>
<body>
    <div class="gallery">
        <div class="gallery-item">
            <img src="/static/images/apartment-1.jpg" alt="Studio Apartment">
        </div>
        <div class="gallery-item">
            <img src="/static/images/apartment-2.jpg" alt="1 Bedroom">
        </div>
        <div class="gallery-item">
            <img src="/static/images/apartment-3.jpg" alt="2 Bedroom">
        </div>
    </div>
</body>
</html>
```

---

## 🏢 **Example: Update Login Page with Logo**

Add your company logo to the login page:

```html
<!-- In login.html, inside .logo section -->
<div class="logo">
    <img src="/static/images/logo.png" alt="Le Blanc Dubai" style="width: 120px; margin-bottom: 20px;">
    <h1>🏢 Le Blanc Dubai</h1>
    <p>Admin Dashboard Login</p>
</div>
```

---

## 📝 **Example: Update Admin Dashboard Header**

Add a background or logo to the admin dashboard:

```html
<!-- In admin.html, update header -->
<div class="header" style="background-image: url('/static/images/header-bg.jpg'); background-size: cover;">
    <button class="logout-btn" onclick="logout()">🚪 Logout</button>
    <img src="/static/images/logo-white.png" alt="Logo" style="width: 100px; margin-bottom: 10px;">
    <h1>Le Blanc Dubai</h1>
    <p>Admin Dashboard - Lead Management System</p>
</div>
```

---

## 🖼️ **Supported Image Formats**

Your website supports all common image formats:
- **JPG/JPEG** - Best for photographs
- **PNG** - Best for logos (supports transparency)
- **GIF** - For simple animations
- **SVG** - Scalable vector graphics (best for logos)
- **WebP** - Modern format (smaller file size)

---

## 💡 **Image Optimization Tips**

### **1. Resize Images Before Upload**
- Desktop images: 1920px width max
- Mobile images: 800px width max
- Thumbnails: 300px width max

### **2. Compress Images**
Use tools like:
- **TinyPNG** (https://tinypng.com)
- **Squoosh** (https://squoosh.app)
- **ImageOptim** (desktop app)

### **3. Recommended Image Sizes**
```
Logo:           200x100 pixels (PNG with transparency)
Background:     1920x1080 pixels (JPG)
Property Card:  800x600 pixels (JPG)
Gallery:        1200x800 pixels (JPG)
Thumbnails:     300x200 pixels (JPG)
```

---

## 🚀 **Quick Start Examples**

### **Example 1: Add Logo to All Pages**

1. Save your logo as: `static/images/logo.png`

2. Add to `index.html`, `admin.html`, `login.html`:
```html
<img src="/static/images/logo.png" alt="Le Blanc Dubai" style="max-width: 200px;">
```

### **Example 2: Add Property Photos**

1. Save images as:
   - `static/images/property-1.jpg`
   - `static/images/property-2.jpg`
   - `static/images/property-3.jpg`

2. Create a section in `index.html`:
```html
<section class="properties">
    <h2>Featured Properties</h2>
    <div class="property-grid">
        <div class="property">
            <img src="/static/images/property-1.jpg" alt="Studio">
            <h3>Studio Apartment</h3>
        </div>
        <div class="property">
            <img src="/static/images/property-2.jpg" alt="1BR">
            <h3>1 Bedroom</h3>
        </div>
        <div class="property">
            <img src="/static/images/property-3.jpg" alt="2BR">
            <h3>2 Bedroom</h3>
        </div>
    </div>
</section>
```

### **Example 3: Add Background Image**

1. Save background as: `static/images/dubai-skyline.jpg`

2. Add to your HTML `<style>` section:
```html
<style>
    body {
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)),
                    url('/static/images/dubai-skyline.jpg');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
</style>
```

---

## 🔗 **Image URL Patterns**

When referencing images in your HTML/CSS, use these patterns:

```
From HTML files in root:         /static/images/filename.jpg
From CSS in static/css:          ../images/filename.jpg
From JavaScript:                 '/static/images/filename.jpg'
Inline CSS in HTML:              url('/static/images/filename.jpg')
```

---

## ✅ **Testing Your Images**

After adding images, test them:

1. Start the server: `python app.py`
2. Open browser: `http://localhost:5000`
3. Check browser console (F12) for any image errors
4. Verify images load correctly on different screen sizes

---

## 📱 **Responsive Images for Mobile**

Use responsive images that adapt to screen size:

```html
<!-- Using srcset for different sizes -->
<img src="/static/images/property-small.jpg"
     srcset="/static/images/property-small.jpg 400w,
             /static/images/property-medium.jpg 800w,
             /static/images/property-large.jpg 1200w"
     sizes="(max-width: 600px) 400px,
            (max-width: 1200px) 800px,
            1200px"
     alt="Property">

<!-- Using CSS for responsive backgrounds -->
<style>
    .hero {
        background-image: url('/static/images/bg-mobile.jpg');
    }
    
    @media (min-width: 768px) {
        .hero {
            background-image: url('/static/images/bg-desktop.jpg');
        }
    }
</style>
```

---

## 🎯 **Common Use Cases**

### **Logo in Header**
```html
<img src="/static/images/logo.png" alt="Le Blanc Dubai" class="logo">
```

### **Hero Section**
```html
<div class="hero" style="background-image: url('/static/images/hero.jpg');">
    <h1>Welcome to Le Blanc Dubai</h1>
</div>
```

### **Property Cards**
```html
<div class="card">
    <img src="/static/images/apartment.jpg" alt="Apartment">
    <h3>Luxury Apartment</h3>
    <p>AED 1,200,000</p>
</div>
```

### **Profile/Avatar**
```html
<img src="/static/images/agent-photo.jpg" alt="Agent" class="avatar">
```

---

## 🛠️ **Troubleshooting**

### **Image Not Showing?**
1. Check file path is correct: `/static/images/filename.jpg`
2. Verify file exists in `static/images/` folder
3. Check file name matches exactly (case-sensitive)
4. Clear browser cache (Ctrl+F5)
5. Check browser console for 404 errors

### **Image Too Large?**
Compress images before uploading using TinyPNG or similar tools.

### **Wrong Aspect Ratio?**
Use CSS to control image display:
```css
img {
    width: 100%;
    height: 300px;
    object-fit: cover; /* or contain */
}
```

---

## 📦 **Ready-to-Use Image Placeholder**

If you don't have images yet, use placeholder services:

```html
<!-- Placeholder.com -->
<img src="https://via.placeholder.com/800x600/667eea/ffffff?text=Le+Blanc+Dubai" alt="Placeholder">

<!-- Unsplash (Real photos) -->
<img src="https://source.unsplash.com/800x600/?dubai,apartment" alt="Dubai Apartment">
```

Replace these with your actual images once ready!

---

**Your images folder is ready at:** `static/images/`

Just copy your image files there and reference them using `/static/images/filename.jpg`!