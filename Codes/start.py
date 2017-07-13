from subprocess import call
call(['amixer cset numid=3 1'], shell=True)
call(['timidity -iA -B8,8 -Os -EFreverb=0'], shell=True)
