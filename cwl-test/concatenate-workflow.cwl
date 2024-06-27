cwlVersion: v1.0
class: Workflow
inputs:
  input_file1:
    type: File
  input_file2:
    type: File
outputs:
  concatenated_output:
    type: File
    outputSource: concatenate/concatenated_file
steps:
  concatenate:
    run: concatenate-tool.cwl
    in:
      file1: input_file1
      file2: input_file2
    out: [concatenated_file]
