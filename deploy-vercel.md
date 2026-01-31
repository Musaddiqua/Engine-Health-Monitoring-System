# 🚀 Deploy to Vercel - Step by Step Guide

## Quick Deploy (Recommended)

### Step 1: Login to Vercel

Open terminal and run:
```bash
vercel login
```

This will:
- Open your browser
- Ask you to authenticate with GitHub/Google/Email
- Complete authentication

### Step 2: Deploy

Run this command in your project directory:
```bash
vercel
```

Follow the prompts:
- **Set up and deploy?** → Type `Y` and press Enter
- **Which scope?** → Select your account
- **Link to existing project?** → Type `N` (first time) or `Y` (if updating)
- **Project name?** → Press Enter for default or type custom name
- **Directory?** → Press Enter (uses current directory)
- **Override settings?** → Type `N`

### Step 3: Production Deploy

After preview deployment works, deploy to production:
```bash
vercel --prod
```

---

## Alternative: Deploy via Vercel Dashboard

1. **Push to GitHub** (if not already):
   ```bash
   git init
   git add .
   git commit -m "Ready for Vercel deployment"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Go to Vercel Dashboard**:
   - Visit https://vercel.com
   - Sign in with GitHub
   - Click "Add New Project"
   - Import your repository

3. **Configure Project**:
   - Framework: **Next.js** (auto-detected)
   - Root Directory: `./`
   - Build Command: `npm run build` (default)
   - Output Directory: `.next` (default)

4. **Environment Variables** (Optional):
   - If using external backend: `NEXT_PUBLIC_API_URL`
   - For integrated backend: Not needed (uses `/api` routes)

5. **Deploy!**
   - Click "Deploy"
   - Wait for build
   - Your app will be live!

---

## Project Structure for Vercel

```
engine/
├── api/
│   └── index.py          # Vercel serverless function (FastAPI)
├── app/                   # Next.js frontend
├── components/            # React components
├── engine_telemetry.csv   # Data file (included in deployment)
├── vercel.json           # Vercel configuration
├── package.json          # Frontend dependencies
└── requirements.txt      # Backend dependencies
```

---

## How It Works

### Frontend (Next.js)
- Deployed as static site with server-side rendering
- Served from Vercel's CDN
- Auto-scales globally

### Backend (FastAPI)
- Deployed as serverless function
- Located at `/api/*` routes
- Uses Mangum adapter for ASGI compatibility
- Includes `engine_telemetry.csv` file

### API Routes
- `/api/vehicles` → Backend API
- `/api/engine-status` → Backend API
- `/api/health` → Backend API
- All other routes → Next.js frontend

---

## Troubleshooting

### Build Fails
- Check `requirements.txt` has all dependencies
- Ensure `mangum` is included
- Verify Python version (3.9+)

### API Not Working
- Check `api/index.py` exists
- Verify `vercel.json` routes configuration
- Check function logs in Vercel dashboard

### CSV File Not Found
- Ensure `engine_telemetry.csv` is in root directory
- Check `vercel.json` includes it in `functions.includeFiles`

### CORS Issues
- Backend CORS is already configured for `*`
- Should work automatically

---

## After Deployment

Your app will be available at:
- **Production:** `https://your-project.vercel.app`
- **Preview:** `https://your-project-git-branch.vercel.app`

### Test Your Deployment

1. Visit your Vercel URL
2. Check if frontend loads
3. Select a vehicle
4. Verify engine health data displays
5. Check browser console for errors

---

## Environment Variables (Optional)

If you want to use an external backend:

1. Go to Vercel Dashboard → Project → Settings → Environment Variables
2. Add: `NEXT_PUBLIC_API_URL` = `https://your-backend-url.com`
3. Redeploy

---

**Ready to deploy? Run `vercel` in your terminal!** 🚀

