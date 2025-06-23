[app]

title = Subscriber App
package.name = techapp
package.domain = org.billingko

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,ttf,txt,otf

version = 0.1
android.version_code = 1

requirements = kivy==2.3.1, \
    kivymd@https://github.com/kivymd/KivyMD/archive/master.zip, \
    asyncgui, \
    asynckivy, \
    filetype, \
    materialyoucolor, \
    pillow, \
    requests, \
    urllib3, \
    idna, \
    certifi, \
    charset_normalizer, \
    kivy-garden, \
    kivy-garden.mapview


orientation = portrait
icon.filename = assets/app_logo.png
presplash.filename = assets/splash.png
android.presplash_color = #352F44

android.api = 34
android.minapi = 28
android.ndk = 25b
android.accept_sdk_license = True

android.archs = arm64-v8a, armeabi-v7a

android.permissions = INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,READ_EXTERNAL_STORAGE,READ_MEDIA_IMAGES,READ_MEDIA_VIDEO,READ_MEDIA_AUDIO

p4a.branch = master
p4a.python_version = 3.10

log_level = 2
android.logcat_filters = *:S python:D

[buildozer]
log_level = 2
warn_on_root = 0
