# Follow the request

GOAL: A newcomer follows who takes responsibility next in an Excel-defined purchase request.
OUTPUT: HyperFrames, 1280x720, 30 fps; silent H.264/yuv420p MP4 with faststart, under 15 MB target; JPEG poster.
TIME: 30 seconds = 900 frames.
LOOK: Existing generated SVG intact, white diagram; page green #183e33 and background #f5f3eb. Inter 48px bold main captions, 30px department labels, 22px provenance. No shadows, glow or texture. Caption margins 128px.
OBJECTS: Real purchase_request.xlsx, byte-identical generated purchase-request.svg, exact task coordinates and connectors from that SVG. Overlaid dark-green outline and traced connector show current focus; animation is explicitly identified as a video overlay.
MOTION: One continuous camera with power2.inOut 0.55s moves between task centres, 2x zoom (26px diagram text), stationary holds after arrival. Opening starts on the actual 002-to-003 connection at 1.28x, then reaches 003 by 1.2s. No live-tracking claim.
SHOTS (frames, inclusive):
0-89: Who handles it next? Requesting -> Purchasing, actual 002->003 handoff visible immediately; focus 003 by frame 36.
90-179: Check the budget; 004 Finance.
180-254: Ask for quotations; 005 Purchasing.
255-329: Choose a quotation; 006 Purchasing.
330-419: Approve the spend; 007 Finance.
420-509: Issue the order; 008 Purchasing.
510-599: Receive the supplies; 009 Receiving.
600-689: Check the quantities; 010 Receiving.
690-779: Confirm the supplies; 011 Requesting.
780-899: Complete the request; 012 Purchasing, with the product name and Excel-to-SVG/offline-HTML explanation held for the final four seconds.
All labels are factual summaries; complete original descriptions remain visible in diagram crops. Hold each large caption 2.5-4s; ending product name and output explanation hold 4s. Persistent note: Animated highlights on the generated diagram.
BANNED: whole-map shrink-to-fit, unreadable caption scale, invented task steps, live execution implication, floating/glowing cards, particles, decorative logos, moving text during reading, stock/generated media, audio-dependent explanation.
QA: inspect 0, 3, 10, 20, 29s and each camera move at start/mid/end; verify opening connection, exact labels, no blank frames, crop containment and 900 successfully decoded frames. Browser and mobile player responsive. Manual user viewing remains pending.
