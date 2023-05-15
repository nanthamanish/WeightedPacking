# Weighted Packing

Dataset Source: http://people.brunel.ac.uk/~mastjjb/jeb/orlib/conloadinfo.html

#### Command to Create input files from `wtpack/`:
    python make_inputs.py <wtpackX>

#### Command to Run packer on one input file:
    python main.py <wtpackX_Y> <output_file>

#### Command to Run packer on all input files:
    python test_all.py <wpackX> <output_file>

### Visualisation
The file `wtpack/wtpack_demo.txt` is a smaller input file for demonstration and visualisation

#### Command to create the input file for demo and run Packer:
    python make_input_demo.py wtpack_demo
    python main.py wtpack_demo <output_file>
#### Command to Run Visualiser:
    python visualiser.py <json_file_name>


