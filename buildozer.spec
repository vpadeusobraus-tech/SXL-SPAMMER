[app]
title = SXL Spammer
package.name = sxlspammer
package.domain = org.sxl
source.dir = .
source.include_exts = py,png,jpg,kv,json
version = 0.1

requirements = python3,kivy==2.2.1,requests,cython==0.29.33
android.permissions = INTERNET

orientation = portrait
android.api = 31
android.minapi = 21
android.ndk_api = 21
android.bootstrap = sdl2
android.archs = arm64-v8a,armeabi-v7a
android.entrypoint = org.kivy.android.PythonActivity
android.apptheme = "@android:style/Theme.NoTitleBar"

android.copy_libs = 1
android.enable_androidx = 1

log_level = 2
warn_on_root = 0
