@echo off
echo ========================================
echo  Vercel Deployment Script
echo ========================================
echo.

echo Step 1: Checking Vercel CLI...
vercel --version
if %errorlevel% neq 0 (
    echo ERROR: Vercel CLI not found. Installing...
    npm install -g vercel
)

echo.
echo Step 2: Deploying to Vercel...
echo.
echo NOTE: You may need to login first with: vercel login
echo.

vercel

echo.
echo ========================================
echo  Deployment Complete!
echo ========================================
echo.
echo To deploy to production, run: vercel --prod
echo.

pause

