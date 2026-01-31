# Deployment Guide - Engine Health Monitoring System

## 🚀 Deploy to Vercel

### Option 1: Deploy via Vercel Dashboard (Recommended)

1. **Push your code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Go to Vercel Dashboard**
   - Visit [vercel.com](https://vercel.com)
   - Sign in with GitHub
   - Click "New Project"
   - Import your repository

3. **Configure Project Settings**
   - Framework Preset: **Next.js** (auto-detected)
   - Root Directory: `./` (root)
   - Build Command: `npm run build` (default)
   - Output Directory: `.next` (default)

4. **Set Environment Variables**
   - Go to Project Settings → Environment Variables
   - Add: `NEXT_PUBLIC_API_URL` = `https://your-backend-api.vercel.app`
   - Or use your backend URL if deployed separately

5. **Deploy!**
   - Click "Deploy"
   - Wait for build to complete
   - Your app will be live at `https://your-project.vercel.app`

### Option 2: Deploy via Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
vercel

# Follow the prompts:
# - Set up and deploy? Yes
# - Which scope? Your account
# - Link to existing project? No
# - Project name? engine-health-monitoring
# - Directory? ./
# - Override settings? No

# For production deployment
vercel --prod
```

## 🔧 Backend Deployment (FastAPI)

### Deploy Backend to Vercel (Serverless Functions)

Create `api/index.py`:

```python
from api import app

# Vercel serverless function handler
handler = app
```

Update `vercel.json`:

```json
{
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    },
    {
      "src": "package.json",
      "use": "@vercel/next"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "api/index.py"
    },
    {
      "src": "/(.*)",
      "dest": "$1"
    }
  ]
}
```

### Alternative: Deploy Backend Separately

1. **Deploy FastAPI to Railway/Render/Heroku**
   - Railway: [railway.app](https://railway.app)
   - Render: [render.com](https://render.com)
   - Heroku: [heroku.com](https://heroku.com)

2. **Update Frontend Environment Variable**
   - Set `NEXT_PUBLIC_API_URL` to your backend URL

## 📝 Environment Variables

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Production (Vercel Dashboard)
```
NEXT_PUBLIC_API_URL=https://your-backend-api.vercel.app
```

## 🧪 Testing Deployment

1. **Test Frontend Locally**
   ```bash
   npm run dev
   # Visit http://localhost:3000
   ```

2. **Test Backend Locally**
   ```bash
   python main.py
   # API at http://localhost:8000
   ```

3. **Test Production Build**
   ```bash
   npm run build
   npm start
   ```

## 🔍 Troubleshooting

### CORS Issues
- Ensure backend CORS allows your frontend domain
- Check `api.py` CORS middleware configuration

### API Connection Issues
- Verify `NEXT_PUBLIC_API_URL` is set correctly
- Check backend is running and accessible
- Test API endpoints directly in browser

### Build Errors
- Run `npm install` to ensure dependencies are installed
- Check Node.js version (requires 18+)
- Clear `.next` folder and rebuild

## 📦 Project Structure for Deployment

```
engine/
├── app/                    # Next.js app directory
├── components/             # React components
├── api.py                  # FastAPI backend
├── package.json           # Frontend dependencies
├── requirements.txt       # Backend dependencies
├── vercel.json            # Vercel configuration
└── engine_telemetry.csv   # Data file (include in deployment)
```

## ✅ Post-Deployment Checklist

- [ ] Frontend deployed and accessible
- [ ] Backend API deployed and accessible
- [ ] Environment variables configured
- [ ] CORS configured correctly
- [ ] API endpoints responding
- [ ] Data file accessible to backend
- [ ] Health check endpoint working

## 🌐 Custom Domain (Optional)

1. Go to Vercel Project Settings → Domains
2. Add your custom domain
3. Configure DNS records as instructed
4. SSL certificate auto-provisioned

---

**Need Help?** Check Vercel docs: https://vercel.com/docs


