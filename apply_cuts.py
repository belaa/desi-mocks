import os
from desitarget import cuts
from desitarget import desi_mask, bgs_mask

from astropy.io import fits
from astropy.table import Table, vstack


# Get paths to all .fits files in a given set of directories
def get_file_paths(dirs, verbose=False):
        all_paths = []
        for i, dir in enumerate(dirs):
                if verbose:
                        print('Looking at directory {:s}'.format(dir))
                files = os.listdir(os.path.join(os.environ['DESI_DR2'], 'tractor', dir))
                files = [fi for fi in files if fi.endswith('.fits')]
                if verbose:
                        print('Returned {:d} files'.format(len(files)))
                for j, file in enumerate(files):
                        all_paths.append(os.path.join(os.environ['DESI_DR2'], 'tractor', dir, file))
        return all_paths


path = get_file_paths(['034'])

all_lrgs = Table()
all_elgs = Table()
all_qsos = Table()
all_bgs = Table()

for i in range(len(path)):
        desi_target, bgs_target, mws_target = cuts.apply_cuts(path[i])
        t = Table.read(path[i])

        lrgs = t[(desi_target & desi_mask.LRG).astype(bool)]
        elgs = t[(desi_target & desi_mask.ELG).astype(bool)]
        qsos = t[(desi_target & desi_mask.QSO).astype(bool)]
        bgs = t[(bgs_target & bgs_mask.BGS_BRIGHT).astype(bool)]

        all_lrgs = vstack([all_lrgs,lrgs])
        all_elgs = vstack([all_elgs,elgs])
        all_qsos = vstack([all_qsos, qsos])
        all_bgs = vstack([all_bgs, bgs])

all_lrgs.write('lrg_cuts034.fits', format='fits')
all_elgs.write('elg_cuts034.fits', format='fits')
all_qsos.write('qso_cuts034.fits', format='fits')
all_bgs.write('bgs_cuts034.fits', format='fits')
