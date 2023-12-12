#!/work/chem-xuhb/apps/deepmd-kit/bin/python
from scipy import constants

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
#HARTREE = 4.3597447222071e-18
#hartree = 51.42206747632595
def convert_xyz_to_raw(xyz_file, raw_file):
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

convert_xyz_to_raw('MD_FORCES.xyz-frc-1.xyz', 'force.raw')
convert_xyz_to_raw('MD_TRAJECTORY.xyz-pos-1.xyz', 'coord.raw')

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

convert_energy_to_raw("MD_ENERGY-1.ener","energy.raw")
