import itk


def registration(fixed_name, moving_name, output):
    PixelType = itk.ctype('float')
    fixed = itk.imread(fixed_name, PixelType)
    moving = itk.imread(moving_name, PixelType)

    Dimension = fixed.GetImageDimension()
    FixedType = itk.Image[PixelType, Dimension]
    MovingType = itk.Image[PixelType, Dimension]

    TransformType = itk.TranslationTransform[itk.D, Dimension]
    initialTransform = TransformType.New()

    optimizer = itk.RegularStepGradientDescentOptimizerv4.New(
        LearningRate=4,
        MinimumStepLength=0.001,
        RelaxationFactor=0.5,
        NumberOfIterations=200)

    metric = itk.MeanSquaresImageToImageMetricv4[
        FixedType, MovingType].New()

    registration = itk.ImageRegistrationMethodv4.New(FixedImage=fixed,
                                                     MovingImage=moving,
                                                     Metric=metric,
                                                     Optimizer=optimizer,
                                                     InitialTransform=initialTransform)

    movingInitialTransform = TransformType.New()
    initialParameters = movingInitialTransform.GetParameters()
    initialParameters[0] = 0
    initialParameters[1] = 0
    movingInitialTransform.SetParameters(initialParameters)
    registration.SetMovingInitialTransform(movingInitialTransform)

    identityTransform = TransformType.New()
    identityTransform.SetIdentity()
    registration.SetFixedInitialTransform(identityTransform)

    registration.SetNumberOfLevels(1)
    registration.SetSmoothingSigmasPerLevel([0])
    registration.SetShrinkFactorsPerLevel([1])

    registration.Update()

    transform = registration.GetTransform()

    finalParameters = transform.GetParameters()
    translationAlongX = finalParameters.GetElement(0)
    translationAlongY = finalParameters.GetElement(1)

    numberOfIterations = optimizer.GetCurrentIteration()

    bestValue = optimizer.GetValue()

    print("Result = ")
    print(" Translation X = " + str(translationAlongX))
    print(" Translation Y = " + str(translationAlongY))
    print(" Iterations    = " + str(numberOfIterations))
    print(" Metric value  = " + str(bestValue))

    CompositeTransformType = itk.CompositeTransform[itk.D, Dimension]
    outputCompositeTransform = CompositeTransformType.New()
    outputCompositeTransform.AddTransform(movingInitialTransform)
    outputCompositeTransform.AddTransform(registration.GetModifiableTransform())

    resampler = itk.ResampleImageFilter.New(Input=moving,
                                            Transform=outputCompositeTransform,
                                            UseReferenceImage=True,
                                            ReferenceImage=fixed)
    resampler.SetDefaultPixelValue(100)

    OutputPixelType = itk.ctype('unsigned char')
    OutputImageType = itk.Image[OutputPixelType, Dimension]

    caster = itk.CastImageFilter[FixedType,
                                 OutputImageType].New(Input=resampler)

    writer = itk.ImageFileWriter.New(Input=caster, FileName=output + "output.jpg")
    writer.SetFileName(output + "output.jpg")
    writer.Update()
