[app]

title = VerbMaster
package.name = verbmaster
package.domain = org.verbmaster

source.dir = .
source.include_exts = py,kv,json,otf,png,jpg,jpeg

version = 1.0.0

requirements = python3,kivy

orientation = portrait
fullscreen = 0

android.entrypoint = org.kivy.android.PythonActivity
android.archs = arm64-v8a
android.allow_backup = True
android.permissions = VIBRATE

[buildozer]

log_level = 2
warn_on_root = 1
