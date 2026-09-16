#!/usr/bin/env python3
from pathlib import Path
import subprocess, shutil
out=Path(__file__).resolve().parent/'media'
if out.exists(): raise SystemExit('media already exists; move it before regenerating')
if not shutil.which('ffmpeg'): raise SystemExit('Install ffmpeg first')
out.mkdir()
subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','testsrc2=size=640x360:rate=24:duration=8','-c:v','libx264','-pix_fmt','yuv420p','-g','8',str(out/'full.mp4')],check=True)
for i in range(2):
    subprocess.run(['ffmpeg','-v','error','-i',str(out/'full.mp4'),'-ss',str(i*4),'-t','4','-an','-c:v','libx264','-g','8','-pix_fmt','yuv420p','-movflags','+faststart',str(out/f'leg{i}.mp4')],check=True)
    subprocess.run(['ffmpeg','-v','error','-i',str(out/f'leg{i}.mp4'),'-frames:v','1',str(out/f'poster{i}.png')],check=True)
print('Created two 4-second diagnostic clips')
