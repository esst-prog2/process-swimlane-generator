# Process Swimlane Generator

A Python tool that converts a structured process-mapping table into a swimlane diagram showing the sequence of tasks, responsible departments, process areas, and annual task frequency.

## 1. The demo

I open a terminal and run `process-map examples/purchase_request.csv`. The program validates 12 sequential tasks belonging to four departments and creates `output/purchase_request_swimlane.svg`. I open the SVG and see four department swimlanes, with every task placed in the lane of its responsible department. Arrows show the process moving from the first task to the final task in one linear sequence, while each task displays its task number, description, process area, and annual frequency where provided. I then run the program with a non-linear example file, and it reports that the input cannot be processed because the first version supports only linear workflows.

## 2. The shape

```text
in           a CSV process-mapping table containing one row per task,
             with a task ID, process section or area, task description,
             responsible department, optional annual frequency, and the
             ID of the next task

out          an SVG swimlane diagram and a validation summary describing
             any problems found in the input

in between   validate that the input represents one complete linear
             process; arrange departments as swimlanes; place each task
             in the lane of its responsible department; connect every
             task to its next task; and render the resulting diagram
```

The initial CSV format will contain the following columns:

| Column             | Description                                                  | Required                       |
| ------------------ | ------------------------------------------------------------ | ------------------------------ |
| `task_id`          | A unique identifier for the task                             | Yes                            |
| `section`          | The process section or area to which the task belongs        | Yes                            |
| `task`             | A description of the task                                    | Yes                            |
| `department`       | The department or function responsible for the task          | Yes                            |
| `annual_frequency` | The estimated number of times the task is performed per year | No                             |
| `next_task_id`     | The ID of the task that follows the current task             | Yes, except for the final task |

Because the first useful version supports only linear processes, each task can have a maximum of one `next_task_id`. The final task has an empty `next_task_id`.

## 3. The size

### First useful version

* Read a linear process mapping from a documented CSV format.
* Validate that all required columns are present and that every task has a unique task ID.
* Validate that every `next_task_id` refers to an existing task.
* Validate that the input contains one connected linear process with one starting task, one ending task, no branches, and no loops.
* Create one swimlane for each department and place every task in the lane of its responsible department.
* Display the task ID, task description, process section, and annual frequency where it is provided.
* Connect the tasks with arrows according to their specified sequence.
* Export the completed swimlane diagram as an SVG file.
* Provide a documented command for generating the diagram.
* Include small synthetic valid and invalid example files that can be used to demonstrate and test the project.

### Not part of the committed project scope this term

* Processes containing branches, merges, or multiple successor tasks.
* XOR, OR, or parallel workflow gateways.
* Connections that loop back to an earlier task.
* Full Business Process Model and Notation (BPMN) compliance.
* Editing tasks through a graphical user interface.
* Dragging or repositioning tasks manually.
* Direct integration with SAP or other company systems.
* Automatically comparing a current process with a proposed process side by side.
* Collaborative editing, user accounts, or online deployment. 
* Guaranteeing an ideal layout for every possible large workflow.

Branches, decision gateways, and loops are not required for the project to be considered complete. If the linear version is successfully implemented, tested, documented, and released ahead of schedule, I may investigate support for more advanced workflow structures as an optional extension toward the end of the project. The linear version will remain the required and independently useful final product.

## 4. How we would know it works

* Given an input file that is missing the `department` column, the program stops and reports an error that specifically names the missing column.
* Given an input containing multiple successors or a connection that returns to an earlier task, the program stops and explains that the input is not a valid linear workflow.
* Given the valid example file containing 12 sequential tasks in four departments, the output contains all 12 tasks, four department swimlanes, and the 11 connections required to form the complete sequence.

## 5. What could stop this

* Automatically arranging tasks across multiple department lanes may produce crossing or difficult-to-read arrows, even when the underlying process is linear.
* The rules defining a valid linear process must be precise enough for the program to identify disconnected tasks, multiple starting or ending tasks, branches, and loops.
* I have not yet selected and tested the visualization library that will produce the final swimlane layout.
* Long task descriptions or processes containing many tasks may make the generated diagram too large or difficult to read.
* Supporting Excel files directly could introduce additional problems caused by formatting, formulas, merged cells, or differences between workbook structures.
* The original version of this idea was developed by myself in a workplace context using Excel VBA, so the public project must remain separate from confidential company code, data, and internal process information.

### Data

The project idea comes from a real process-mapping need identified during workplace digitalization initiatives. Colleagues currently prepare the input mapping because they have the necessary knowledge about their own tasks, responsibilities, departments, and process sequence.

The existing internal workbook, VBA code, company process mappings, and company data will not be published or used in the classroom demonstration. The repository will instead contain a small synthetic process-mapping file with invented tasks, departments, process areas, annual frequencies, and workflow connections.

The synthetic file will include a valid linear process for demonstrating the generated swimlane diagram. It will also include small invalid examples, such as a file with a missing required column and a file containing a branch or loop. These examples will allow the program and its tests to run without access to confidential workplace data.
