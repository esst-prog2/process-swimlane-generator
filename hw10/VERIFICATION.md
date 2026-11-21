# HW10 setup and local rendering verification - 2026-11-21

Official instructions consulted: https://github.com/heygen-com/hyperframes (current README), then installed release-matched skills at C:/Users/User/.agents/skills/hyperframes/SKILL.md and hyperframes-cli/SKILL.md, including story, explainer, format, installation, scaffold, check and render references.

## Versions and installation

- Windows x64, Node v24.21.0; npm.cmd and npx.cmd 11.19.0.
- HyperFrames 0.9.72, installed locally in hw10 with npm.cmd install and package-lock.json; zero audit vulnerabilities. npm warned of an unapproved esbuild postinstall; checks and rendering succeeded without enabling it.
- npx.cmd hyperframes skills update installed six v0.9.72 core skills under the user-level .agents/skills directory (also linked/copied for other detected agents). Actual skills were read, not merely installed.
- FFmpeg and FFprobe 9.1-full_build-www.gyan.dev installed through the command recommended by HyperFrames doctor:
  winget install --id Gyan.FFmpeg -e --accept-source-agreements --accept-package-agreements --silent
- Existing system Chrome was detected. Render reported Browser: download and used hardware AMD/ANGLE Direct3D11 with drawElement capture, so the encoding run was not assumed to use system Chrome.
- Local rendering; no HeyGen/cloud render, paid media or generated assets. HyperFrames fetched/cached Inter font faces as part of compilation. Diagram asset is byte-identical to docs/purchase-request.svg (SHA256 8B8704F4661E2896A5D47914030A28B5172C7EB149ED6C46CA9F0FF331B00B1E).

## Commands and results

Run from hw10/smoke in PowerShell. Refresh PATH in the current shell after winget installation:

```powershell
$env:Path = [Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [Environment]::GetEnvironmentVariable('Path','User')
node C:/Users/User/.agents/skills/hyperframes/scripts/plugin-cli.mjs check --json
node C:/Users/User/.agents/skills/hyperframes/scripts/plugin-cli.mjs snapshot --at 0.5,1.5 --no-end --output renders/snapshots --json
node C:/Users/User/.agents/skills/hyperframes/scripts/plugin-cli.mjs render --quality draft --fps 24 --workers 1 --output renders/smoke.mp4
ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=codec_name,width,height,pix_fmt,r_frame_rate,nb_read_frames,duration -show_entries format=size,duration -of json renders/smoke.mp4
ffmpeg -v error -xerror -i renders/smoke.mp4 -f null NUL
ffmpeg -v error -i renders/smoke.mp4 -vf "select=eq(n\,12)+eq(n\,36)" -fps_mode vfr renders/decoded-%02d.png
ffmpeg -v error -i renders/smoke.mp4 -f framemd5 renders/frames.md5
```

Check: ok=true, browserSkipped=false, zero errors. Reviewed warnings: duplicated image source and two nested-root scene structures; two one-second text holds shorter than film reading recommendations. Accepted for this deliberately tiny technical test only; not a final-video structure or readability acceptance. No-audio info is expected. Snapshot contact sheet showed both timed states and the existing diagram.

Render: exit 0, 10.9 seconds reported render time. A small-frame warning was resolved by HyperFrames recapture/self-verification (PSNR infinity); decoded images independently show nonblank frames.

MP4: H.264, yuv420p, 640x360, 24/1 fps, 2.000000 seconds, 48 decoded frames, 9852 bytes. Full FFmpeg decode completed with no errors. Inspected decoded frames 12 and 36: title, diagram, and respective A/B labels are visible, confirming the timed change survives encoding. Diagram text is intentionally tiny in this infrastructure test; final video must use readable crops. This is decode/frame inspection, not a claim of manual media-player playback.

Evidence is committed under evidence/: smoke.mp4, decoded-01.png, decoded-02.png, frames.md5 and check.json. MP4 SHA256: 673076E2FF46116B52509B11A54C14C744E50E1A1E99336F4B851CD1EFFE7D22.

## Resolved execution failures

- Initial `ffmpeg -version`: CommandNotFoundException, "The term 'ffmpeg' is not recognized". Fixed by winget installation and PATH refresh.
- Initial `npx.cmd --yes hyperframes@latest --version`: npm EACCES fetching https://registry.npmjs.org/hyperframes and writing npm-cache logs in sandbox. Same command with approved elevated execution returned 0.9.72.
- `git add -- PROCESS.md PLANNING_LOG.md` and following commit initially failed: "Unable to create .../.git/index.lock: Permission denied". Approved elevated Git execution succeeded; no reset or unrelated staging.
- `.\.venv\Scripts\python.exe -c ...` reading the workbook initially failed because Python313/python.exe was denied by sandbox; approved elevated read succeeded and printed all 12 actual rows.

No unresolved installation or rendering failure. Optional transcription, voice, music and Docker dependencies were not needed for the silent local test. No final concept video has been built.
