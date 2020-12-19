config_root = "config/"
content_root = "content/"
design_root = "design/"
templates_dir = "templates"
build_root = "build/"
build_profiles_file = "profiles.json"
deploy_command = 'rsync -e "/usr/bin/ssh" -av --exclude=/.well-known/ --delete'
