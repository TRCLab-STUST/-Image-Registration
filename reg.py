import SimpleITK as sitk
from math import pi


def command_iteration(method, debug):
    if not debug:
        return

    if method.GetOptimizerIteration() == 0:
        print("Scales: ", method.GetOptimizerScales())
    print("{0:3} = {1:7.5f} : {2}".format(method.GetOptimizerIteration(),
                                          method.GetMetricValue(),
                                          method.GetOptimizerPosition()))


def registration(fixed_name, moving_name, tfm_name, times, debug):
    fixed = sitk.ReadImage(fixed_name, sitk.sitkFloat32)
    fixed = sitk.Normalize(fixed)
    fixed = sitk.DiscreteGaussian(fixed, 2.0)

    moving = sitk.ReadImage(moving_name, sitk.sitkFloat32)
    moving = sitk.Normalize(moving)
    moving = sitk.DiscreteGaussian(moving, 2.0)

    R = sitk.ImageRegistrationMethod()

    R.SetMetricAsJointHistogramMutualInformation()

    R.SetOptimizerAsGradientDescentLineSearch(learningRate=1.0,
                                              numberOfIterations=times,
                                              convergenceMinimumValue=1e-5,
                                              convergenceWindowSize=5)

    R.SetInitialTransform(sitk.TranslationTransform(fixed.GetDimension()))

    R.SetInterpolator(sitk.sitkLinear)

    R.AddCommand(sitk.sitkIterationEvent, lambda: command_iteration(R, debug))

    outTx = R.Execute(fixed, moving)

    print("-------")
    print(outTx)
    print("Optimizer stop condition: {0}".format(R.GetOptimizerStopConditionDescription()))
    print(" Iteration: {0}".format(R.GetOptimizerIteration()))
    print(" Metric value: {0}".format(R.GetMetricValue()))

    sitk.WriteTransform(outTx, tfm_name)

    # fixed = sitk.ReadImage(fixed_name, sitk.sitkFloat32)
    # moving = sitk.ReadImage(moving_name, sitk.sitkFloat32)
    #
    # R = sitk.ImageRegistrationMethod()
    #
    # R.SetMetricAsMattesMutualInformation(numberOfHistogramBins=50)
    #
    # sample_per_axis = times
    #
    # if fixed.GetDimension() == 2:
    #     tx = sitk.Euler2DTransform()
    #     R.SetOptimizerAsExhaustive([sample_per_axis//2, 0, 0])
    #     R.SetOptimizerScales([2.0*pi/sample_per_axis, 1.0, 1.0])
    # elif fixed.GetDimension() == 3:
    #     tx = sitk.Euler3DTransform()
    #     R.SetOptimizerAsExhaustive([sample_per_axis // 2, sample_per_axis // 2, sample_per_axis // 4, 0, 0, 0])
    #     R.SetOptimizerScales(
    #         [2.0 * pi / sample_per_axis, 2.0 * pi / sample_per_axis, 2.0 * pi / sample_per_axis, 1.0, 1.0, 1.0])
    #
    # tx = sitk.CenteredTransformInitializer(fixed, moving, tx)
    #
    # R.SetInitialTransform(tx)
    #
    # R.SetInterpolator(sitk.sitkLinear)
    #
    # R.AddCommand(sitk.sitkIterationEvent, lambda: command_iteration(R, debug))
    #
    # outTx = R.Execute(fixed, moving)
    #
    # print("-------")
    # print(outTx)
    # print("Optimizer stop condition: {0}".format(R.GetOptimizerStopConditionDescription()))
    # print(" Iteration: {0}".format(R.GetOptimizerIteration()))
    # print(" Metric value: {0}".format(R.GetMetricValue()))
    #
    # sitk.WriteTransform(outTx, tfm_name)
