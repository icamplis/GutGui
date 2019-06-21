from GutGuiModules import *

def main():
    window = init()

    listener = ModuleListener()

    # source and output
    (source_and_output_frame, sno_label) = frame_and_label(window, "Source & Output", PASTEL_BLUE_RGB, 0, 0, 4, 1, 2)
    source_and_output_module = SourceAndOutput(source_and_output_frame, listener)

    # analysis and form
    (analysis_and_form_frame, anf_label) = frame_and_label(window, "Analysis & Form", PASTEL_ORANGE_RGB, 4, 0, 8, 1, 8)
    analysis_and_form_module = AnalysisAndForm(analysis_and_form_frame, listener)

    # save
    (save_frame, s_label) = frame_and_label(window, "Save",PASTEL_PINK_RGB, 12, 0, 2, 1)
    save_module = Save(save_frame, listener)

    # original colour
    (og_color_frame, ogc_label) = frame_and_label(window, "Original Colour-Coded Image", PASTEL_PINK_RGB, 0, 1, 7, 2)

    # recreated colour
    (recreated_color_frame, recreated_color_label) = frame_and_label(window, "Recreated Color Image",
                                                                     PASTEL_BLUE_RGB, 7, 1, 7, 1, labelspan=5)
    recreated_color_module = RecColour(recreated_color_frame, listener)

    # new colour
    (new_color_frame, new_color_label) = frame_and_label(window, "New Color-Coded Image", PASTEL_ORANGE_RGB,
                                                         7, 2, 7, 1, labelspan=5)
    new_color_module = NewColour(new_color_frame, listener)

    # diagram
    (diagram_frame, diagram_label) = frame_and_label(window, "Diagram",PASTEL_ORANGE_RGB, 0, 3, 2, 2, 4)
    diagram_module = Diagram(diagram_frame, listener)

    # histogram
    (histogram_frame, histogram_label) = frame_and_label(window, "Histogram", PASTEL_BLUE_RGB, 2, 3, 6, 2, 5)
    histogram_module = Histogram(histogram_frame, listener)

    # absorption
    (absorption_spec_frame, absorption_spec_label) = frame_and_label(window, "Absorption Spectrum", PASTEL_PINK_RGB, 8, 3, 6, 2, 5)
    absorption_module = AbsorptionSpec(absorption_spec_frame, listener)

    window.mainloop()

if __name__ == '__main__':
    main()