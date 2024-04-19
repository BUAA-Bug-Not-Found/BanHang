后端部署

1. 安装库

   ```
   pip install fastapi
   pip install peewee
   pip install uvicorn
   pip install pyjwt
   ```

2. 运行服务

   ```powershell
   cd backend/fastapi
   python main.py
   ```

前端部署
!!!路径中不要包含中文
1. 安装Android Studio

2. 安装SDK(在Android Studio的SDK Manager里面)

   - SDK Platforms = Android 13.0  API Level=33
   - android sdk build-tools=33.0.2

3. 安装gradle

4. 安装vue和cordova

   ```
   npm install --global vue-cli
   npm install -g cordova
   npm install -g plugman
   ```
5. 添加安卓平台
   ```
   cd banhangApp
   cordova add platform android
   ```
6.  生成apk
   ```powershell
   cd vueproject
   buildapp.bat
   ```

   
