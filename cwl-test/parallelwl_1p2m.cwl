#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: Workflow
inputs:
  input_filesize: int
  file_path: string
  newstr: string
outputs:
  final_file:
    type: file
    outputSource: 
    - T8/a5
    - T7/a4
steps:
  T1:
    run: create.py
    in:
      y: file_path
      x: input_filesize
    out:
    - file
  T2:
    run: partition.py
    in:
      x: T1/file
    out:
    - a3
    - a2
    - a1
  T3:
    run: read&print.py
    in: 
      x: T2/a1
    out: 
    - answer
  T4:
    run: read&print.py
    in: 
      x: T2/a2
    out: 
    - answer 
  T5:
    run: read&print.py
    in: 
      x: T2/a3
    out: 
    - answer 
  T6:
    run: addstr2f.py
    in: 
      y: newstr
      x: T3/answer
    out:
    - a1_new
  T7:
    run: merge.py
    in:
      y: T2/a2
      x: T3/a3
    out: 
    - a4
  T8:
    run: merge.py
    in:
      y: T6/a1_new
      x: T7/a4
    out: 
    - a5
