# Editing and rebuilding

This is the editable HyperFrames source for Follow the request, 1280x720/30 fps, 30 seconds. All visible content is from the supplied synthetic purchase request. assets/purchase-request.svg and assets/purchase_request.xlsx are copied from the repository, without changing their content. assets/gsap.min.js is the bundled GSAP 3.15.0 runtime from HyperFrames 0.9.72.

The camera's stationary dwell/pan pattern adapts the official pan-stations component retained in compositions/components/. Its placeholder graphics are not used: the actual SVG provides the complete diagram and original labels. Overlays copy exact task boxes and connection paths. Captions are editable in compositions/journey.html. To regenerate from workbook/SVG geometry, edit build_scene.py and run it with the repository Python environment; this overwrites index.html, compositions/journey.html and beats.json.

Run CLI operations through the installed skill launcher in this folder:

```powershell
node C:/Users/User/.agents/skills/hyperframes/scripts/plugin-cli.mjs preview --background --port 3017
node C:/Users/User/.agents/skills/hyperframes/scripts/plugin-cli.mjs check --json
node C:/Users/User/.agents/skills/hyperframes/scripts/plugin-cli.mjs render --fps 30 --workers 1 --quality looks --output renders/follow-request.mp4
```

Dependencies, caches and temporary renders are ignored. Delivered files are in ../../docs/assets/. No cloud rendering or audio is used. A new shell may be needed after installing FFmpeg, or refresh PATH from the machine/user environment.
