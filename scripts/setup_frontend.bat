@echo off

REM Create frontend directories
md ..\frontend\web_react\public
md ..\frontend\web_react\src\assets
md ..\frontend\mobile_react_native\android\app\src\main\res\mipmap-xxxhdpi
md ..\frontend\mobile_react_native\ios\AcademyOpenAI\Images.xcassets\AppIcon.appiconset

REM Copy favicon files for web
copy ..\AcademyOpenAI\docs\favicon.ico ..\frontend\web_react\public\
copy ..\AcademyOpenAI\docs\favicon-16x16.png ..\frontend\web_react\public\
copy ..\AcademyOpenAI\docs\favicon-32x32.png ..\frontend\web_react\public\
copy ..\AcademyOpenAI\docs\android-chrome-192x192.png ..\frontend\web_react\public\
copy ..\AcademyOpenAI\docs\android-chrome-512x512.png ..\frontend\web_react\public\
copy ..\AcademyOpenAI\docs\apple-touch-icon.png ..\frontend\web_react\public\
copy ..\AcademyOpenAI\docs\site.webmanifest ..\frontend\web_react\public\

REM Copy icons for mobile
copy ..\AcademyOpenAI\docs\android-chrome-512x512.png ..\frontend\mobile_react_native\android\app\src\main\res\mipmap-xxxhdpi\ic_launcher.png
copy ..\AcademyOpenAI\docs\apple-touch-icon.png ..\frontend\mobile_react_native\ios\AcademyOpenAI\Images.xcassets\AppIcon.appiconset\