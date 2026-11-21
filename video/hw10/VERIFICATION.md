# Final HW10 verification - 2026-11-21

## Delivered media

- docs/assets/follow-the-request.mp4: 1,263,314 bytes (1.26 MB), comfortably below the 15 MB target.
- H.264, yuv420p, 1280x720, 30/1 fps, exactly 30.000000 seconds and 900 decoded frames; no audio track.
- docs/assets/follow-the-request-poster.jpg: 1280x720 JPEG, 67,770 bytes, taken from the encoded opening frame with the question and real 002-to-003 handoff.
- HyperFrames 0.9.72 local render with Node 24.21.0, FFmpeg/FFprobe 9.1; one worker, looks quality. CLI reported 29.2 seconds rendering time and successful validation.
- MP4 remuxed without recompression with `ffmpeg -v error -i video/hw10/renders/follow-request.mp4 -c copy -movflags +faststart docs/assets/follow-the-request.mp4`. The moov atom precedes mdat, enabling progressive browser playback.

## Media checks

`ffprobe -v error -count_frames -show_entries stream=codec_name,width,height,pix_fmt,r_frame_rate,nb_read_frames,duration -show_entries format=duration,size -of json docs/assets/follow-the-request.mp4` reported the values above.

`ffmpeg -v error -xerror -i docs/assets/follow-the-request.mp4 -f null NUL` completed with exit 0: all 900 frames decoded, no errors.

Inspected decoded frames 0, 36, 83, 90, 173, 248, 300, 323, 413, 495, 593, 600, 675, 773 and 870, covering 0/3/10/20/29 seconds and every main transition. Also reviewed full-size HyperFrames snapshots and review/phone sheets. Opening immediately contains 002 -> 003 and Requesting -> Purchasing; 003 is enlarged by 1.2s. At 3s Finance task 004 is centered; 10s Purchasing task 006; 20s Receiving task 010; 29s Purchasing task 012. Other arrival snapshots verify tasks 005, 007, 008, 009 and 011 against actual workbook descriptions and departments.

New task captions coincide with camera arrivals. During a move the outgoing caption stays as context while the connection leads into the next task. Long vertical handoffs widen for 0.85 seconds, preserving the route, then restore 2x detail; the entire map is never shrunk to fit. Large captions remain stationary for 2.5-4 seconds. The movie states that highlights animate an existing generated diagram. No task execution, live status, or real company data is implied.

`final-check.json` records HyperFrames ok=true, browserSkipped=false, zero lint/runtime/layout/contrast errors. Only film_silent is retained deliberately. Original source files match their repository originals by SHA256. The editable scene is under video/hw10; only final media is under docs/assets; temporary renders, preview thumbnails, caches and dependencies are ignored.

## Browser and page

Chrome/157.0.8103.80, automated with installed Puppeteer 25.18.1, successfully played the actual MP4 and sought to 3 seconds at 1280x900 and 390x900. Both returned readyState=4, error=null, played=true, duration=30 and native dimensions 1280x720. Player widths were 1177.59px and 358.80px respectively, contained within each viewport with a 16:9 aspect ratio. Inspected both screenshots. Full original diagram detail is small in phone-width inline playback; the large captions carry the story and native fullscreen is available.

Verified native controls, playsinline, preload=metadata, relative poster/source paths and successful HTTP delivery of MP4/poster. No page JavaScript errors. Existing favicon.ico returns 404; it is unrelated and unchanged. Only one section and its scoped CSS were added to the promo page.

The first browser helper import used an obsolete Puppeteer lib/esm path and failed ERR_MODULE_NOT_FOUND; fixed using the installed package export path. Initial Python http.server preview supported playback but seeking reset to zero; replaced with local-only serve_preview.py with byte-range support, then repeated playback, seek and responsive checks successfully. These were verification/setup issues; final video decoding succeeded on the first render.

Local review URL: http://127.0.0.1:8771/#follow-the-request
Editable HyperFrames preview: http://localhost:3017/#project/hw10

User viewing feedback and permission to push remain pending. No push performed.
