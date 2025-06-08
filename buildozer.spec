[app]
title = ScheduleApp
package.name = scheduleapp
package.domain = org.kivy
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,json

requirements = python3,kivy,firebase-admin,requests

android.permissions = INTERNET
fullscreen = 0
orientation = portrait

[buildozer]
log_level = 2
warn_on_root = 0
android.api = 31
android.ndk = 25b
android.minapi = 21
