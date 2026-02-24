# Logo Setup Instructions

## Overview
The website now displays two logos on every page:
- **Left side**: JNTU Technological University logo
- **Right side**: ITYUKTA 2K26 logo

## Current Status
Placeholder SVG logos have been created at:
- `frontend/public/logo-jntu.svg`
- `frontend/public/logo-ityukta.svg`

## How to Replace with Your Actual Logos

### Option 1: Replace the SVG files
1. Save your JNTU logo as `frontend/public/logo-jntu.svg` (or `.png`)
2. Save your ITYUKTA logo as `frontend/public/logo-ityukta.svg` (or `.png`)
3. If using PNG format, update the file references in the components:
   - `frontend/src/components/Login.tsx`
   - `frontend/src/components/Register.tsx`
   - `frontend/src/components/AdminDashboard.tsx`
   - `frontend/src/components/DragDropChallenge.tsx`
   - Change `/logo-jntu.svg` to `/logo-jntu.png`
   - Change `/logo-ityukta.svg` to `/logo-ityukta.png`

### Option 2: Use Different File Names
If your logo files have different names:
1. Place your logo files in `frontend/public/` folder
2. Update the image sources in all components to match your file names

## Logo Placement

### Pages with Logos:
1. **Login Page** - Fixed position, top-left and top-right corners
2. **Register Page** - Fixed position, top-left and top-right corners
3. **Challenge List Page** - In the header with title
4. **Drag-Drop Challenge Page** - In the challenge header
5. **Admin Dashboard** - In the admin header

### Logo Sizes:
- **Auth pages (Login/Register)**: 100px × 100px (responsive: 70px on tablets, 50px on mobile)
- **Main header**: 80px × 80px (responsive: 60px on tablets, 50px on mobile)
- **Challenge header**: 60px × 60px (responsive: 50px on tablets, 40px on mobile)
- **Admin header**: 80px × 80px (responsive: 60px on tablets, 50px on mobile)

## Styling Features:
- Drop shadow effects for better visibility
- Hover animation (scales to 1.1x on hover)
- Fully responsive design for mobile devices
- Consistent placement across all pages

## Testing
After replacing the logos:
1. Restart the frontend server if it's running
2. Clear browser cache (Ctrl+Shift+R or Cmd+Shift+R)
3. Check all pages to ensure logos display correctly:
   - Login page
   - Register page
   - Challenge list page
   - Drag-drop challenge page
   - Admin dashboard

## Troubleshooting
- If logos don't appear, check the browser console for 404 errors
- Ensure logo files are in the `frontend/public/` folder
- Verify file names match exactly (case-sensitive)
- Try clearing browser cache
- Check that image files are valid and not corrupted
