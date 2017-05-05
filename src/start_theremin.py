from subprocess import call
call(['espeak "Starting Thea re min. Please wait few seconds..." 2>/dev/null'], shell=True)
call(['timidity -iA -B8,8 -Os -EFreverb=0'], shell=True)
