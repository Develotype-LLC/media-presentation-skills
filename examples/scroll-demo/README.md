# Synthetic scroll interaction demo

Requires Python 3 and FFmpeg with libx264. From the repository root:

```sh
python3 examples/scroll-demo/make_media.py
python3 -m http.server 8765 --bind 127.0.0.1
```

Open http://127.0.0.1:8765/examples/scroll-demo/ in your browser. Scroll forward, stop, and reverse. Use the route controls and resize the window. The continuous test pattern is split into two clips so the seam can be checked in both directions.

The pattern is synthetic diagnostic video, not generated artwork or a finished marketing example. Replace clips and copy with your reviewed story. The runtime imports the bundled engine from the skills folder; copy that engine and its license beside a standalone exported project and update the script path.

Generated files are ignored by git. The generator refuses to overwrite an existing media directory. Delete only your generated demo folder if you deliberately want to regenerate it.
