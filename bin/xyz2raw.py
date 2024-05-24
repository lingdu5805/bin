#!/work/chem-lij/xuhb/apps/deepmd227/bin/python
import os
from scipy import constants
#dpdata v0.2.0 读取restart有误，此为修正代码
#dpdata v0.2.17 把cp2k里restart的输出修好了，可以不用此代码
#小数点后的误差是因为dpdata读取的是cp2k.log里的力
#这里读取的是另外输出的MD_FORCES.xyz-frc-1.xyz的力
#MD_FORCES.xyz-frc-1.xyz里的精度更高一点，所以第7 8 位会开始不一样
AVOGADRO = constants.Avogadro  # Avagadro constant
ELE_CHG = constants.elementary_charge  # Elementary Charge, in C
BOHR = constants.value("atomic unit of length")  # Bohr, in m
HARTREE = constants.value("atomic unit of energy")  # Hartree, in Jole
RYDBERG = constants.Rydberg * constants.h * constants.c  # Rydberg, in Jole

# energy conversions
econvs = {
    "eV": 1.0,
    "hartree": HARTREE / ELE_CHG,
    "kJ_mol": 1 / (ELE_CHG * AVOGADRO / 1000),
    "kcal_mol": 1 / (ELE_CHG * AVOGADRO / 1000 / 4.184),
    "rydberg": RYDBERG / ELE_CHG,
    "J": 1 / ELE_CHG,
    "kJ": 1000 / ELE_CHG,
}
# length conversions
lconvs = {
    "angstrom": 1.0,
    "bohr": BOHR * 1e10,
    "nm": 10.0,
    "m": 1e10,
}
hartree = HARTREE / ELE_CHG /  BOHR / 1e10

def convert_force_to_raw(xyz_file, raw_file):
    with open(xyz_file, 'r') as f_in, open(raw_file, 'w') as f_out:
        while True:
            line = f_in.readline()
            if not line:
                break  # EOF
            n_atoms = int(line.strip())
            f_in.readline()  # Skip the frame info line
            forces = []
            for _ in range(n_atoms):
                _, fx, fy, fz = f_in.readline().split()
                forces.extend([f'{float(fx) * hartree:.18e}', f'{float(fy) * hartree:.18e}', f'{float(fz) * hartree:.18e}'])
            f_out.write(' '.join(map(str, forces)) + '\n')

def convert_coord_to_raw(xyz_file, raw_file):
    with open(xyz_file, 'r') as f_in, open(raw_file, 'w') as f_out:
        while True:
            line = f_in.readline()
            if not line:
                break  # EOF
            n_atoms = int(line.strip())
            f_in.readline()  # Skip the frame info line
            forces = []
            for _ in range(n_atoms):
                _, fx, fy, fz = f_in.readline().split()
                forces.extend([f'{float(fx):.18e}', f'{float(fy):.18e}', f'{float(fz):.18e}'])
            f_out.write(' '.join(map(str, forces)) + '\n')

def convert_energy_to_raw(energy_file, raw_file):
    with open(energy_file, 'r') as f_in, open(raw_file, 'w') as f_out:
        while True:
            line = f_in.readline()
            if not line:
                break  # EOF
            if "Pot." in line:
                continue  # Skip the line
            ENERGY = float(line.split()[4]) * (HARTREE / ELE_CHG)
            f_out.write(f'{ENERGY:.18e}\n')

def main():
    os.system('mkdir raw_data-restart')
    convert_force_to_raw('MD_FORCES.xyz-frc-1.xyz', 'raw_data-restart/force.raw')
    convert_coord_to_raw('MD_TRAJECTORY.xyz-pos-1.xyz', 'raw_data-restart/coord.raw')
    convert_energy_to_raw('MD_ENERGY-1.ener','raw_data-restart/energy.raw')

if __name__ == "__main__":
    main()
