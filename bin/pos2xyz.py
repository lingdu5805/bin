#! E:/work_tools/Python39/python 
# -*- coding: utf-8 -*-
#
#transformed from POSCAR to xyz format
#The code is created by XuHongbin-TCCL

#####################################################
# POSCAR format, the first number is the line number:
    #  1  system_name
    #  2     1.000
    #  3     17.7485999999999997    0.0000000000000000    0.0000000000000000
    #  4      0.0000000000000000   19.4893999999999998    0.0000000000000000
    #  5      0.0000000000000000    0.0000000000000000   35.0000000000000000
    #  6     O    Ti   Ru
    #  7    222  108   22
    #  8  Selective Dynamics
    #  9  Direct
    # 10      0.4543554874520194  0.4858016603938680  0.4689137492863409    T  T  T             O1
    # 11      0.3533085214322111  0.3199713896855128  0.4576832718358865    T  T  T             O2 
    # ...
#####################################################
# xyz format:
    # 352
    # [17.74860,0.00000,0.00000,0.00000,19.48940,0.00000,0.00000,0.00000,35.00000]
    # O   8.0641738045910  9.4679828800800  16.411981225022
    # O   6.2707316234920  6.2360504021370  16.018914514256
    # ...
#####################################################
# The code reads the POSCAR file and extracts the system name, scale, cell vectors, element types, element counts, and fractional coordinates.
# The code then converts the fractional coordinates to cartesian coordinates using the cell vectors and scale.
# The code sorts the cartesian coordinates by z-axis in descending order.
# Finally, the code writes the xyz file with the system name, cell vectors, and element symbols and coordinates.

import numpy as np

# Read the POSCAR file
def read_poscar(POSCAR_file):
    with open(POSCAR_file, 'r') as f:
        system_name = f.readline().strip()   # 1
        scale = float(f.readline().strip()) # 2
        cell_vectors = []
        #.strip().split() delete the space first and split the line by space
        #strip means delete the space at the beginning and end of the line
        #split means split the line by space
        for i in range(3): # 3-5
            line = f.readline().strip().split()
            cell_vectors.append([float(n) for n in line])
        cell_vectors = np.array(cell_vectors)
        element_types = f.readline().split() # 6
        #element_types_num = len(element_types)  
        element_counts = [int(n) for n in f.readline().split()] # 7
        #sum_counts = sum(element_counts)
        # skip 2 line
        f.readline() # 8 Selective dynamics
        f.readline() # 9 Direct
        frac_coords = []
        for i in range(len(element_types)):
            frac_coords.append([])
            for j in range(element_counts[i]):
                line = f.readline().strip().split()[0:3]
                if len(line) >= 3:
                    frac_coords[i].append(line)
        return system_name, scale, cell_vectors, element_types, element_counts, frac_coords

# sort coords by z-axis
def sort_coords_decending_z(coords):
    for i in range(len(coords)):
        coords[i] = sorted(coords[i],key = lambda x:float(x[2]),reverse=True)
    return coords

# Convert the fractional coordinates to cartesian coordinates
def frac2cart(frac_coords, cell_vectors, scale=1.0):
    cart_coords = []
    for i in range(len(frac_coords)):
        cart_coords.append([])
        for j in range(len(frac_coords[i])):
            frac_coord = np.array(frac_coords[i][j], dtype=float)
            cart_coord = scale * (frac_coord @ cell_vectors)
            cart_coords[i].append(cart_coord)
    return cart_coords

# Write the xyz file
def write_xyz(filename, cell_vectors, element_types, element_counts, cart_coords):
    with open(filename, 'w') as f:
        # sum of element counts
        f.write(str(sum(element_counts)) + '\n')
        # box size, 3x3 matrix, 5 decimal places
        flat_vector = cell_vectors.flatten()
        formatted_list = [f'{value:.5f}' for value in flat_vector]
        f.write("["+','.join(formatted_list)+"]"+ '\n') 
        # element symbols and coordinates
        for i in range(len(element_types)):
            element_type = element_types[i].ljust(2)  # occupy 2 characters, left-aligned
            for j in range(len(cart_coords[i])):
                # Formats coordinates as floating-point numbers with 15 decimal places and left justified to 18 characters
                # If the number has less 15 decimal point, right-pad it with zeros to the right
                formatted_coords = '   '.join(
                    (f'{n:.15f}').ljust(18, '0' if '.' in str(n) else ' ') for n in cart_coords[i][j]
                )
                f.write(element_type + '   ' + formatted_coords + '\n')  # write to file

def __main__():
    filemane_input = 'F:/Desktop/POSCAR'
    filemane_output = 'F:/Desktop/shuchu/POSCAR.xyz'
    system_name, scale, cell_vectors, element_types, element_counts, frac_coords = read_poscar(filemane_input)
    cart_coords = frac2cart(frac_coords, cell_vectors, scale)
    cart_coords = sort_coords_decending_z(cart_coords)
    write_xyz(filemane_output, cell_vectors, element_types, element_counts, cart_coords)
    print('pos2xyz.py: ' + system_name + ' Done!')

if __name__ == '__main__':
    __main__()
        
