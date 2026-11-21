# HW10 concepts - awaiting selection

Assumptions proposed by Codex: 28-32 seconds, 1920x1080 landscape, completely silent; all meaning carried by readable text and visuals. Existing synthetic workbook, SVG and offline viewer are the factual sources; no paid media or generated assets. No concept is selected or implemented.

One takeaway: an Excel task list becomes a map of who handles each step and where responsibility changes departments.

## 1. Follow the request (recommended)

In the first three seconds, a supplies request leaves Requesting for Purchasing under the question "Who handles it next?" A continuous camera move follows a highlighted path through enlarged portions of the actual purchase-request diagram, including Finance checks, the return to Purchasing and delivery to Receiving, before pulling back to reveal the Excel-to-diagram connection. Unlike reading the page, the viewer experiences the order and departmental handoffs as one journey.

Device/form: one request carried through a continuous diagram journey.
Beats: supplies needed -> first handoff -> budget/order/delivery handoffs -> actual full map -> Excel in, responsibility visible.
Look: existing diagram's soft section colours and dark green highlights; large sans-serif labels, light ground.
Sound: none; on-screen question, department names and short captions carry the story.

## 2. Rows become a route

The first three seconds show the actual 002 row pointing to 003 while its department changes from Requesting to Purchasing. In a single frame that rebuilds itself, selected workbook rows move into department lanes, next-task IDs become arrows, and a short real command/output insert connects the explanation to the actual generated viewer. Beyond the page, this teaches how to read the input and why each task lands in its lane, with later Purchasing-to-Finance and Purchasing-to-Receiving examples.

Device/form: a worked input-to-output transformation in one rebuilding frame.
Beats: 002 links to 003 -> department becomes lane -> successor becomes arrow -> run generator -> real viewer.
Look: factual workbook excerpt evolving into existing SVG geometry; restrained green highlight tracks the same IDs throughout.
Sound: none; labels explicitly explain "Department = lane" and "Next ID = arrow".

## 3. Find the next owner

The first three seconds freeze a completed request description beside "Who checks this next?" and the four real department names. This silent mini-challenge briefly lets viewers search the workbook, then reveals task 003 in Purchasing on the diagram; two further quick reveals follow the budget check in Finance and supplies arriving in Receiving, ending on the full offline viewer. Beyond the page, viewers practise answering a concrete ownership question and see how lane labels and arrows help them orient themselves.

Device/form: a question-and-reveal challenge, with deliberate holds and hard cuts between workbook detail and diagram evidence; no interactive clicking required.
Beats: ownership question -> inspect row -> reveal Purchasing -> Finance reveal -> Receiving reveal -> explore your own process.
Look: large dark-green question typography on the page's light ground, tight crops of real evidence, one accent per revealed answer.
Sound: none; every question and answer is printed and held for reading.

## Source checks and boundaries

Read README.md, docs/index.html, tests/build_examples.py, src/process_swimlane/{cli,validation,render,viewer}.py, and actual examples/purchase_request.xlsx through openpyxl. The workbook has 12 tasks, four departments and 11 successor links. 002 -> 003 transfers Requesting to Purchasing; 003 -> 004 transfers to Finance; 008 -> 009 transfers Purchasing to Receiving. The full route returns to earlier departments; do not flatten it into four sequential department blocks.

The generator is a Windows Python command-line tool, not a workflow execution or live tracking system. Any moving highlight is an explanatory video overlay. Input is one connected linear process, output is SVG plus optional offline HTML; branching and automated comparison are not supported. Use the promo page as factual background, not as a scrolling-page video.

Alternative directions considered before narrowing: reverse the journey from delivery back to the request; a side-by-side scrolling race; the three retained above. Rejected the reverse journey as harder for beginners and the race because no measured speed benefit is established.
