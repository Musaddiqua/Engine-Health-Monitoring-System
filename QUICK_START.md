# 🚀 Quick Start Guide

## Running the Complete System

### Step 1: Start the Backend API

Open a terminal and run:
```bash
python main.py
```

The API will start at: **http://localhost:8000**

### Step 2: Start the Frontend

Open another terminal and run:
```bash
npm run dev
```

The frontend will start at: **http://localhost:3000**

### Step 3: Open in Browser

Visit: **http://localhost:3000**

You'll see a beautiful dashboard with:
- ✅ Vehicle selection
- ✅ Real-time engine health metrics
- ✅ Visual health score
- ✅ AI-powered explanations
- ✅ Auto-refresh every 5 seconds

---

## 🎨 Features

### Dashboard Components

1. **Health Score Card**
   - Large circular progress indicator
   - Color-coded (Green/Yellow/Red)
   - Real-time score (0-100)

2. **Metric Cards**
   - RPM, Temperature, Oil Pressure, Vibration
   - Current vs Expected values
   - Deviation percentage
   - Status badges (Normal/Warning/Critical)

3. **AI Explanation**
   - Human-readable explanations
   - Actionable recommendations
   - Context-aware insights

4. **Vehicle Selector**
   - Easy vehicle switching
   - Visual selection indicator
   - Real-time updates

---

## 📦 Deployment to Vercel

### Quick Deploy

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push
   ```

2. **Deploy to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Import your GitHub repository
   - Set environment variable: `NEXT_PUBLIC_API_URL`
   - Deploy!

### Or use CLI:
```bash
npm i -g vercel
vercel
```

---

## 🔧 Configuration

### Environment Variables

Create `.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

For production, set in Vercel dashboard.

---

## 🐛 Troubleshooting

### Frontend can't connect to API
- Ensure backend is running on port 8000
- Check `NEXT_PUBLIC_API_URL` is set correctly
- Verify CORS is enabled in backend

### Build errors
- Run `npm install` to install dependencies
- Clear `.next` folder: `rm -rf .next`
- Rebuild: `npm run build`

### Port already in use
- Change port: `npm run dev -- -p 3001`
- Or stop the process using port 3000

---

## 📱 Access Points

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

---

**Enjoy your Engine Health Monitoring System! 🚗💨**


