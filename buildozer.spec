[app]
title = ClassScheduleApp
package.name = classschedule
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,json
version = 1.0
requirements = python3,kivy,requests,firebase-admin
orientation = portrait
osx.kivy_version = 2.1.0

[buildozer]
log_level = 2
warn_on_root = 0

[android]
android.api = 31
android.minapi = 21
android.ndk = 25b
android.permissions = INTERNET

