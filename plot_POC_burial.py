import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from mycolorpy import colorlist as mcp

sim_ages = [0, 2.5, 4.5, 7.5, 10, 12.5, 15]

POC_export = pd.read_excel('POC_export.xlsx', skiprows=[0], usecols=range(2, 9))
POC_export = POC_export.div(POC_export.sum(axis=0), axis=1)*100
col = mcp.gen_color(cmap="tab20", n=20)[0:18]*2

fig, ax = plt.subplots()
stacks = ax.stackplot(sim_ages, POC_export, labels=['PEQD',
'CAMR+PNEC',
'CARB',
'BENG+SATL+BRAZ',
'ETRA+GUIN',
'GUIA+WTRA',
'CHIL',
'MEDI+NASE+NASW+NATR+CNRY',
'NWCS',
'SARC+NECS',
'NADR+GFST',
'ARCT',
'SSTC',
'AUSW',
'EAFR+ISSG',
'MONS+INDE+INDW+REDS+ARAB',
'ALSK+PSAE+CCAL',
'BPLR',
'SANT+FKLD',
'NEWZ',
'AUSE+ARCH+SPSG+TASM',
'WARM+SUND',
'NPSW+NPTG',
'CHIN',
'KURO+NPPF',
'BERS+PSAW',
'ANTA+APLR',
],
colors=col)
ax.margins(x=0, y=0)
ax.legend(loc='right', reverse=True, labelspacing=0.74, fontsize=11, bbox_to_anchor=(1.31, 0.5))
ax.set_title(label='Provincial OC burial contribution (no burial scheme)', fontsize=20, pad=12)
ax.set_ylabel(ylabel='OC burial contribution (%)', fontsize=18)
ax.set_xlabel(xlabel='Age (Ma)', fontsize=18)
plt.gca().invert_xaxis()

# hatches = ['', '...']*20
# for stack, hatch in zip(stacks, hatches):
    # stack.set_hatch(hatch)

plt.show()

# Dunne et al. 2007
# Bulk ocean salinity scaling
# ~o.pgclann.nc