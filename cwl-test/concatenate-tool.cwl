cwlVersion: v1.0
class: CommandLineTool
baseCommand: [cat]
inputs:
  file1:
    type: File
    inputBinding:
      position: 1
  file2:
    type: File
    inputBinding:
      position: 2
outputs:
  concatenated_file:
    type: File
    outputBinding:
      glob: concatenated.txt
stdout: concatenated.txt
