
echo Potential | gmx_mpi energy -f step6.0_minimization.edr -o step6.0_potential.xvg

echo Temperature | gmx_mpi energy -f step6.1_equilibration.edr -o step6.1_temperature.xvg
echo Potential | gmx_mpi energy -f step6.1_equilibration.edr -o step6.1_potential.xvg
echo Total-Energy | gmx_mpi energy -f step6.1_equilibration.edr -o step6.1_energy.xvg

echo Temperature | gmx_mpi energy -f step6.2_equilibration.edr -o step6.2_temperature.xvg
echo Potential | gmx_mpi energy -f step6.2_equilibration.edr -o step6.2_potential.xvg
echo Total-Energy | gmx_mpi energy -f step6.2_equilibration.edr -o step6.2_energy.xvg

echo Temperature | gmx_mpi energy -f step6.3_equilibration.edr -o step6.3_temperature.xvg
echo Pressure | gmx_mpi energy -f step6.3_equilibration.edr -o step6.3_pressure.xvg
echo Density | gmx_mpi energy -f step6.3_equilibration.edr -o step6.3_density.xvg
echo Potential | gmx_mpi energy -f step6.3_equilibration.edr -o step6.3_potential.xvg
echo Total-Energy | gmx_mpi energy -f step6.3_equilibration.edr -o step6.3_energy.xvg

echo Temperature | gmx_mpi energy -f step6.4_equilibration.edr -o step6.4_temperature.xvg
echo Pressure | gmx_mpi energy -f step6.4_equilibration.edr -o step6.4_pressure.xvg
echo Density | gmx_mpi energy -f step6.4_equilibration.edr -o step6.4_density.xvg
echo Potential | gmx_mpi energy -f step6.4_equilibration.edr -o step6.4_potential.xvg
echo Total-Energy | gmx_mpi energy -f step6.4_equilibration.edr -o step6.4_energy.xvg

echo Temperature | gmx_mpi energy -f step6.5_equilibration.edr -o step6.5_temperature.xvg
echo Pressure | gmx_mpi energy -f step6.5_equilibration.edr -o step6.5_pressure.xvg
echo Density | gmx_mpi energy -f step6.5_equilibration.edr -o step6.5_density.xvg
echo Potential | gmx_mpi energy -f step6.5_equilibration.edr -o step6.5_potential.xvg
echo Total-Energy | gmx_mpi energy -f step6.5_equilibration.edr -o step6.5_energy.xvg

echo Temperature | gmx_mpi energy -f step6.6_equilibration.edr -o step6.6_temperature.xvg
echo Pressure | gmx_mpi energy -f step6.6_equilibration.edr -o step6.6_pressure.xvg
echo Density | gmx_mpi energy -f step6.6_equilibration.edr -o step6.6_density.xvg
echo Potential | gmx_mpi energy -f step6.6_equilibration.edr -o step6.6_potential.xvg
echo Total-Energy | gmx_mpi energy -f step6.6_equilibration.edr -o step6.6_energy.xvg
