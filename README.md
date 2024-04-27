后端部署

1. 安装库
   
   `python` 版本要求 `>=3.9`

   使用 `conda`
   ```
   conda create -n Banhang python=3.9
   conda activate Banhang
   pip install -r requirements.txt
   ```

   使用 `pythonenv`
   ```
   python -m venv Banhang
   Banhang\Scripts\activate
   pip install -r requirements.txt
   ```

2. 运行服务

   ```powershell
   cd backend/fastapi
   python main.py
   ```

前端部署

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

5.  生成apk

   ```powershell
   cd vueproject
   buildapp.bat
   ```