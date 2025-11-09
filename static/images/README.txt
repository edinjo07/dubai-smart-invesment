<!-- 
    QUICK START: How to Add Images to Your Website
    ================================================
-->

1. FOLDER STRUCTURE
   ================
   DUBAI REAL ESTATE/
   └── static/
       └── images/          ← PUT YOUR IMAGES HERE
           ├── logo.png
           ├── hero-background.jpg
           ├── apartment-1.jpg
           ├── apartment-2.jpg
           └── gallery-1.jpg


2. HOW TO USE IMAGES IN HTML
   ==========================
   
   Simple Image:
   <img src="/static/images/logo.png" alt="Le Blanc Dubai">
   
   Background Image:
   <div style="background-image: url('/static/images/background.jpg');"></div>
   
   In CSS:
   background-image: url('/static/images/hero.jpg');


3. EXAMPLES
   ========
   
   Logo in Header:
   <img src="/static/images/logo.png" alt="Logo" style="width: 200px;">
   
   Property Card:
   <div class="card">
       <img src="/static/images/apartment-1.jpg" alt="Apartment">
       <h3>Luxury Apartment</h3>
   </div>
   
   Background:
   <style>
       body {
           background-image: url('/static/images/dubai-skyline.jpg');
           background-size: cover;
       }
   </style>


4. IMAGE SIZES (RECOMMENDED)
   ==========================
   Logo:           200x100 pixels (PNG)
   Hero/Banner:    1920x1080 pixels (JPG)
   Property Card:  800x600 pixels (JPG)
   Gallery:        1200x800 pixels (JPG)
   Thumbnails:     300x200 pixels (JPG)


5. WHERE TO GET IMAGES
   ===================
   • Your own photos of Le Blanc Dubai
   • Professional photographer
   • Stock photos: Unsplash, Pexels (free)
   • Developer website/marketing materials


6. TEST YOUR IMAGES
   =================
   1. Copy image to: static/images/
   2. Start server: python app.py
   3. Visit: http://localhost:5000/image-examples.html
   4. Check if images appear correctly


7. COMMON ISSUES
   =============
   Image not showing?
   • Check file path: /static/images/filename.jpg
   • Verify file exists in folder
   • Check spelling (case-sensitive)
   • Clear browser cache (Ctrl+F5)


8. QUICK TEST
   ===========
   Visit this page to see examples:
   http://localhost:5000/image-examples.html
