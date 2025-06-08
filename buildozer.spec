[app]
title = MyApp
package.name = myapp
package.domain = org.example
version = 0.1

source.include_exts = py,png,jpg,kv,json,ttf
source.include_patterns = *

requirements = python3,kivy,firebase-admin,requests
android.permissions = INTERNET

[buildozer]
log_level = 2
warn_on_root = 0

[android]
android.api = 31
android.ndk = 25b
android.ndk_path = /root/.buildozer/android/platform/android-ndk-r25b
android.sdk_path = /root/.buildozer/android/platform/android-sdk
android.minapi = 21

[python]
# (optional) if you need specific version
