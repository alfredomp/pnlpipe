from pnlpipe_pipelines._pnl import *


def make_pipeline(caseid,
                  inputDicomKey='dicom',
                  inputDwiKey='dwi',
                  inputDwimaskKey='dwimask',
                  bet_threshold=bet_threshold,
                  ukfparams=ukfparams,
                  BRAINSTools_hash=BRAINSTools_hash,
                  UKFTractography_hash=UKFTractography_hash,
                  dcm2niix_hash=dcm2niix_hash):
    """Diffusion PNL pipeline.

    dwi:           input DWI
    dwixc:         Aligned, centered DWI
    dwied:         Eddy current corrected DWI
    dwimask:       input mask, otherwise uses FSL bet
    ukf:           UKF Tractograpy vtk file

    """
    params = locals()

    tags = {}

    if inputDwiKey:
        tags['dwi'] = InputPathFromKey([inputDwiKey, caseid])
    else:
        tags['dicom'] = InputPathFromKey([inputDicomKey, caseid])
        tags['dwi'] = DicomNhdr(params, deps=[tags['dicom']])


    tags['dwixc'] = DwiXc(params, deps=[tags['dwi']])

    tags['dwied'] = DwiEd(params, deps=[tags['dwixc']])

    if inputDwimaskKey:
        tags['dwimask'] = InputPathFromKey(params=[inputDwimaskKey, caseid])
    else:
        tags['dwimask'] = DwiMaskBet(params, deps=[tags['dwied']])


    tags['ukf'] = Ukf(params, deps=[tags['dwied'],
                                    tags['dwimask']])


    return tags

DEFAULT_TARGET = 'ukf'

