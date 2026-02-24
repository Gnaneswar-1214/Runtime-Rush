# How to Add Your Actual Logo Images

## Current Status
✅ Logo placeholders are showing (circles with text)
❌ Need to replace with your actual logo images

## Steps to Add Your Logos

### Option 1: Manual Copy (Easiest)
1. **Save the two logo images** you shared in the chat to your computer
   - JNTU logo (the one with rose and gear)
   - ITYUKTA 2K26 logo (the one with robot hand and globe)

2. **Rename them**:
   - JNTU logo → `logo-jntu.png` (or `.jpg`)
   - ITYUKTA logo → `logo-ityukta.png` (or `.jpg`)

3. **Copy to the public folder**:
   - Navigate to: `D:\RuntimeRush\frontend\public\`
   - Paste both logo files there
   - **Replace** the existing `.svg` files

4. **Update file extensions in code** (if using PNG/JPG):
   - Open these files and change `.svg` to `.png` (or `.jpg`):
     - `frontend/src/components/Login.tsx`
     - `frontend/src/components/Register.tsx`
     - `frontend/src/components/AdminDashboard.tsx`
     - `frontend/src/components/DragDropChallenge.tsx`
     - `frontend/src/components/Header.tsx`

5. **Refresh browser**: Press Ctrl+Shift+R to see your logos

### Option 2: Using Command Line
```bash
# Navigate to the public folder
cd D:\RuntimeRush\frontend\public

# Copy your logo files here
# Then rename them to logo-jntu.png and logo-ityukta.png
```

### Option 3: I Can Help You Convert
If you can provide the logo images again, I can:
1. Create proper image files
2. Save them in the correct location
3. Update all the code references

## What Format Should I Use?

**Recommended**: PNG with transparent background
- Best quality
- Works well on any background color
- File size is reasonable

**Alternative**: JPG
- Smaller file size
- No transparency (will have white/colored background)

**Current**: SVG (placeholder)
- Vector format
- Scalable without quality loss
- But currently just showing text placeholders

## File Locations to Update

If using PNG/JPG instead of SVG, change these lines:

### 1. Login.tsx (Line 33-34)
```typescript
// Change from:
<img src="/logo-jntu.svg" alt="JNTU Logo" className="auth-logo auth-logo-left" />
<img src="/logo-ityukta.svg" alt="ITYUKTA 2K26 Logo" className="auth-logo auth-logo-right" />

// To:
<img src="/logo-jntu.png" alt="JNTU Logo" className="auth-logo auth-logo-left" />
<img src="/logo-ityukta.png" alt="ITYUKTA 2K26 Logo" className="auth-logo auth-logo-right" />
```

### 2. Register.tsx (Line 46-47)
```typescript
// Same changes as Login.tsx
```

### 3. AdminDashboard.tsx (Line 150 & 160)
```typescript
// Change from:
<img src="/logo-jntu.svg" alt="JNTU Logo" className="admin-logo admin-logo-left" />
<img src="/logo-ityukta.svg" alt="ITYUKTA 2K26 Logo" className="admin-logo admin-logo-right" />

// To:
<img src="/logo-jntu.png" alt="JNTU Logo" className="admin-logo admin-logo-left" />
<img src="/logo-ityukta.png" alt="ITYUKTA 2K26 Logo" className="admin-logo admin-logo-right" />
```

### 4. DragDropChallenge.tsx (Line 202 & 212)
```typescript
// Same changes
```

### 5. Header.tsx (Line 13 & 19)
```typescript
// Same changes
```

## Quick Test
After adding your logos:
1. Open http://localhost:3000
2. You should see your actual logos instead of the placeholder circles
3. If not, press Ctrl+Shift+R to hard refresh

## Need Help?
If you're having trouble, you can:
1. Share the logo images again in the chat
2. Tell me the file format (PNG, JPG, SVG)
3. I'll help you get them set up correctly
