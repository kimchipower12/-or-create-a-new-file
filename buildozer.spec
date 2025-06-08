[app]
title = ClassScheduleApp
package.name = classschedule
package.domain = org.example
source.dir = .
version = 0.1
requirements = python3,kivy,requests,firebase-admin
orientation = portrait
osx.kivy_version = 2.1.0
fullscreen = 1

[buildozer]
log_level = 2
warn_on_root = 0

[android]
android.api = 31
android.minapi = 21
android.ndk = 25b
android.build_tools_version = 30.0.2
android.permissions = INTERNET

# 이미지, 폰트 포함
source.include_exts = py,png,jpg,kv,json,ttf
