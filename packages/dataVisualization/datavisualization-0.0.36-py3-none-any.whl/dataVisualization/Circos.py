from pycirclize import Circos

sectors = {"Environmental": 100, "Social": 100, "Governance": 100, "Other":100, "Nestle":100, "Unileaver":100, "Essity":100}
sector_colors = {"Environmental": '#8DC63F', "Social": '#E2E41E', "Governance": '#00B4AA', "Other": '#414042',
                 "Nestle":'#ebab34', "Unileaver":'#3461eb', "Essity":'#eb347a'}
circos = Circos(sectors, space=5)

for sector in circos.sectors:
    track = sector.add_track((95, 100))
    track.axis(fc=sector_colors[sector.name])
    track.text(sector.name, color="white", size=12)
    track.xticks_by_interval(10)

circos.link(("Nestle", 0, 25), ("Environmental", 0, 33), allow_twist=False, direction=1, color='#ebab34', alpha=0.5)
circos.link(("Nestle", 25, 50), ("Social", 0, 33), allow_twist=False, direction=1, color='#ebab34', alpha=0.5)
circos.link(("Nestle", 50, 75), ("Governance", 0, 12), allow_twist=False, direction=1, color='#ebab34', alpha=0.5)
circos.link(("Nestle", 75, 100), ("Other", 0, 20), allow_twist=False, direction=1, color='#ebab34', alpha=0.5)

circos.link(("Unileaver", 0, 15), ("Environmental", 33, 66), allow_twist=False, direction=1, color='#3461eb', alpha=0.5)
circos.link(("Unileaver", 15, 50), ("Social", 33, 66), allow_twist=False, direction=1, color='#3461eb', alpha=0.5)
circos.link(("Unileaver", 50, 75), ("Governance", 12, 40), allow_twist=False, direction=1, color='#3461eb', alpha=0.5)
circos.link(("Unileaver", 75, 100), ("Other", 20, 35), allow_twist=False, direction=1, color='#3461eb', alpha=0.5)

circos.link(("Essity", 0, 25), ("Environmental", 66, 99), allow_twist=False, direction=1, color='#eb347a', alpha=0.5)
circos.link(("Essity", 25, 40), ("Social", 33, 66), allow_twist=False, direction=1, color='#eb347a', alpha=0.5)
circos.link(("Essity", 40, 80), ("Governance", 40, 80), allow_twist=False, direction=1, color='#eb347a', alpha=0.5)
circos.link(("Essity", 80, 100), ("Other", 35, 55), allow_twist=False, direction=1, color='#eb347a', alpha=0.5)

circos.savefig("result.png")