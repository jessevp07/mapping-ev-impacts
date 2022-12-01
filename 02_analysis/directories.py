## Project File Directories ##
import os

home = os.path.join('C:','\\Users','Jesse Vega-Perkins','Documents','mapping_ev_impacts_public')
p_data = os.path.join(home,'01_data')
p_out = os.path.join(home,'03_output')
p_fig = os.path.join(p_out,'figures')
p_fig_data = os.path.join(p_out,'figure_data')
p_interim = os.path.join(home,'02_analysis','interim_data')
proj_gdb = os.path.join(home,'gis_thesis_ev','gis_thesis_ev.gdb')
output_gdb = os.path.join(p_out,'output.gdb')
cost = os.path.join(home,'02_analysis','lcoc-ldevs')
cost_data = os.path.join(home,'02_analysis','lcoc-ldevs','data')
cost_out = os.path.join(home,'02_analysis','lcoc-ldevs','outputs')