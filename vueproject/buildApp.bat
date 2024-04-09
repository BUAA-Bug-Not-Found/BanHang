@echo on
echo start building..
call npm run build
del /S /Q banhangApp\www\*.*
xcopy /E /I dist\* banhangApp\www
cd banhangApp 
call cordova build android
cd ..
copy banhangApp\platforms\android\app\build\outputs\apk\debug\app-debug.apk .\
