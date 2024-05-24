#! E:/work_tools/Python39/python 
# -*- coding: utf-8 -*-
#
import os
import numpy
# Get box size from xyz file or use the default box size parameter
def get_box_info(input_file_name):
    with open(input_file_name) as f:
        load_lines = f.readlines()
        #di 2 hang [a,0.000,0.000,0.000,b,0.000,0.000,0.000,c]
        try:
            box_size_parameter = (((load_lines[1].split('['))[1].split(']'))[0]).split(',')
            box_size_parameter = list(map(float, box_size_parameter))
        # If box info is not correct, use default box parameters
        except:
            box_size_parameter = default_box_size
        # If box info is missing, use default box parameters
        if not len(box_size_parameter) ==  9:
            box_size_parameter = default_box_size
    return box_size_parameter

# Extract molecule structure from xyz file
def get_molecule_structure(input_file_name):
    molecule_structure = []
    with open(input_file_name) as f:
        load_lines = f.readlines()
        for i in range(2,int(load_lines[0])+2):
            line = load_lines[i].split()
            no_space_line = []
            # Remove space and tab from list
            for object in line:
                if not len(object) == 0:
                    no_space_line.append(object)
            print(no_space_line)
            molecule_structure.append([no_space_line[0],float(no_space_line[1]),float(no_space_line[2]),float(no_space_line[3])])
    # Re-rank all atoms base on the elements
    #molecule_structure.sort(key = lambda x: x[0])
    return molecule_structure

# Calculate the molecule's center (average position of all atoms) and move it to the center of box
def recenter_molcecule(molecule_structure,box_size_parameter):
    recenter_molecule_structure = []
    molceule_x = 0
    molceule_y = 0
    molceule_z = 0
    # Calculate molecule's center by average position of all atoms
    for ele in molecule_structure:
        molceule_x += ele[1]
        molceule_y += ele[2]
        molceule_z += ele[3]
    molecule_number = len(molecule_structure)
    molecule_center = [molceule_x/molecule_number,molceule_y/molecule_number,molceule_z/molecule_number]
    # Calculate box's center
    box_center = [box_size_parameter[0]/2,box_size_parameter[4]/2,box_size_parameter[8]/2]
    # Calculate shift value and apply to all atoms
    x_shift = molecule_center[0] - box_center[0]
    y_shift = molecule_center[1] - box_center[1]
    z_shift = molecule_center[2] - box_center[2]
    for ele in molecule_structure:
        recenter_molecule_structure.append([ele[0],ele[1]-x_shift,ele[2]-y_shift,ele[3]-z_shift])
    return recenter_molecule_structure

# Find elements type and each type's number
def get_elements_and_number(molecule_structure):
    ele_list = []
    ele_non_repeat_list = []
    ele_number = []
    for atom in molecule_structure:
        ele_list.append(atom[0])
    # Remove repeated elements without change their rank
    ele_non_repeat_list = list({}.fromkeys(ele_list).keys())
    for ele in ele_non_repeat_list:
        ele_number.append(ele_list.count(ele))
    return [ele_non_repeat_list,ele_number]

# Write the info into POSCAR file
def write_POSCAR(input_file_name,box_size_parameter,recenter_molcecule_structure,elements_and_number):
    with open(input_file_name[:-5] + ".vasp","w") as f:
        f.write("Input file generated from " + input_file_name + "\n")
        f.write("1.0\n")
        f.write(" " + str(box_size_parameter[0]).ljust(8, '0') + " " + str(box_size_parameter[1]).ljust(8, '0') + " " + str(box_size_parameter[2]).ljust(8, '0') + "\n")
        f.write(" " + str(box_size_parameter[3]).ljust(8, '0') + " " + str(box_size_parameter[4]).ljust(8, '0') + " " + str(box_size_parameter[5]).ljust(8, '0') + "\n")
        f.write(" " + str(box_size_parameter[6]).ljust(8, '0') + " " + str(box_size_parameter[7]).ljust(8, '0') + " " + str(box_size_parameter[8]).ljust(8, '0') + "\n")
        for ele in elements_and_number[0]:
            f.write(" " + ele.ljust(4) )
        f.write("\n")
        for ele_num in elements_and_number[1]:
            f.write(" " + str(ele_num).ljust(4))
        f.write("\n")
        #f.write("Cartesian\n")
        f.write('Direct\n')
        for atom in recenter_molcecule_structure:
            a = atom[1]/box_size_parameter[0]
            b = atom[2]/box_size_parameter[4]
            c = atom[3]/box_size_parameter[8]
            f.write("  " + (f'{a:.15f}').ljust(18, '0' if '.' in str(a) else ' ') +
                    "  " + (f'{b:.15f}').ljust(18, '0' if '.' in str(b) else ' ') +
                    "  " + (f'{c:.15f}').ljust(18, '0' if '.' in str(c) else ' ') + "\n")



# Default parameters
default_box_size = [11.832400000000,0.000,0.000,0.000,12.992946000,0.000,0.000,0.000,27.27443600000000]

# Get xyz files' name in the same path with this script
#files = os.listdir(os.curdir)
xyz_files = []
#for single_file in files:
#    if single_file[-3:] == "xyz":
#        xyz_files.append(single_file)

filemane_input = 'F:/Desktop/opt-1.xyz0'
#filemane_output = 'F:/Desktop/opt-1.vasp'
xyz_files.append(filemane_input)
# Transfer all xyz file into POSCAR
def xyz_pos_center():
    for file in xyz_files:
        # Define File name
        input_file_name = file
        # Get molecule structure
        molecule_structure = get_molecule_structure(input_file_name)
        # Get box info
        box_size_parameter = get_box_info(input_file_name)
        # Recenter the molecule center with box center
        recenter_molcecule_structure = recenter_molcecule(molecule_structure,box_size_parameter)
        # Get elements' info, which is essential for make POSCAR
        elements_and_number = get_elements_and_number(recenter_molcecule_structure)
        # Write all info into POSCAR file
        write_POSCAR(input_file_name,box_size_parameter,recenter_molcecule_structure,elements_and_number)


def xyz_pos_origin():
    for file in xyz_files:
        # Define File name
        input_file_name = file
        # Get molecule structure
        molecule_structure = get_molecule_structure(input_file_name)
        # Get box info
        box_size_parameter = get_box_info(input_file_name)
        # Recenter the molecule center with box center
        #recenter_molcecule_structure = recenter_molcecule(molecule_structure,box_size_parameter)
        # Get elements' info, which is essential for make POSCAR
        elements_and_number = get_elements_and_number(molecule_structure)
        # Write all info into POSCAR file
        write_POSCAR(input_file_name,box_size_parameter,molecule_structure,elements_and_number)

if __name__ == "__main__":
    xyz_pos_origin()
