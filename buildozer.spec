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
accept_sdk_license = True

[android]
android.api = 31
android.minapi = 21
android.ndk = 25b
android.sdk_path = /home/runner/android-sdk
android.build_tools_version = 30.0.3
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.debug = 1
android.logcat_filters = *:S python:D
android.enable_androidx = 1
android.use_android_native_api = 0
android.packaging.exclude_patterns = *.pyc, __pycache__
android.additional_features = androidx
android.allow_backup = 1
