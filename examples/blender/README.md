# Editable Blender reveal

An original abstract geometry starter: a cover rises to reveal three internal blocks. It illustrates source packaging and controlled motion, not a technical system.

From this directory, with Blender on PATH:

```sh
blender --background --python reveal.py -- --out out
blender --background out/reveal.blend --render-frame 48
```

The script saves a scene, camera, and animation with no text. Render and inspect a proof before rendering all frames. Keep native overlays in your compositor. Run from a new output folder; the script refuses to overwrite a saved scene.
