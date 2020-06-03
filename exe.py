import SimpleITK as sitk

import config


def exe(fixed_name, moving_name, tfm_output, output_name):
    fixed = sitk.ReadImage(fixed_name, sitk.sitkFloat32)
    moving = sitk.ReadImage(moving_name, sitk.sitkFloat32)
    outTx = sitk.ReadTransform(tfm_output)

    resampler = sitk.ResampleImageFilter()
    resampler.SetReferenceImage(fixed)
    resampler.SetInterpolator(sitk.sitkLinear)
    resampler.SetDefaultPixelValue(1)
    resampler.SetTransform(outTx)

    out = resampler.Execute(moving)

    simg1 = sitk.Cast(sitk.RescaleIntensity(fixed), sitk.sitkUInt8)
    simg2 = sitk.Cast(sitk.RescaleIntensity(out), sitk.sitkUInt8)
    cimg = sitk.Compose(simg1, simg2, simg1 // 2. + simg2 // 2.)
    sitk.WriteImage(simg2, config.OUTPUT_DIR + "fixed.jpg")
    sitk.WriteImage(cimg, output_name)
