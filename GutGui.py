from GutGuiModules import *
import logging

logging.basicConfig(level=logging.DEBUG)

def main():
    (window, input_output, image_diagram) = init()

    listener = ModuleListener()

    # source and output
    (source_and_output_frame, sno_label) = frame_and_label(input_output, "Source & Output", PASTEL_BLUE_RGB, 0, 0, 1, 1, labelspan=2)
    source_and_output_module = SourceAndOutput(source_and_output_frame, listener)
    listener.attach_module(SOURCE_AND_OUTPUT, source_and_output_module)

    # analysis and form
    (analysis_and_form_frame, anf_label) = frame_and_label(input_output, "Analysis & Form", PASTEL_ORANGE_RGB, 0, 1, 1, 1, labelspan=8)
    analysis_and_form_module = AnalysisAndForm(analysis_and_form_frame, listener)
    listener.attach_module(ANALYSIS_AND_FORM, analysis_and_form_module)

    # save
    (save_frame, s_label) = frame_and_label(input_output, "Save",PASTEL_PINK_RGB, 0, 2, 1, 1)
    save_module = Save(save_frame, listener)
    listener.attach_module(SAVE, save_module)

    # original colour
    (og_color_frame, ogc_label) = frame_and_label(image_diagram, "Original Image", PASTEL_PINK_RGB, 0, 0, 7, 2)
    og_color_module = OGColour(og_color_frame, listener)
    listener.attach_module(ORIGINAL_COLOUR, og_color_module)

    # recreated colour
    (recreated_color_frame, recreated_color_label) = frame_and_label(image_diagram, "Recreated Image", PASTEL_BLUE_RGB, 7, 0, 7, 1, labelspan=5)
    recreated_color_module = RecColour(recreated_color_frame, listener)
    listener.attach_module(RECREATED_COLOUR, recreated_color_module)

    # new colour
    (new_color_frame, new_color_label) = frame_and_label(image_diagram, "New Image", PASTEL_ORANGE_RGB, 7, 1, 7, 1, labelspan=5)
    new_color_module = NewColour(new_color_frame, listener)
    listener.attach_module(NEW_COLOUR, new_color_module)

    # diagram
    (diagram_frame, diagram_label) = frame_and_label(image_diagram, "Diagram",PASTEL_ORANGE_RGB, 0, 4, 14, 1, labelspan=1)
    diagram_module = Diagram(diagram_frame, listener)
    listener.attach_module(DIAGRAM, diagram_module)

    # histogram
    (histogram_frame, histogram_label) = frame_and_label(image_diagram, "Histogram", PASTEL_BLUE_RGB, 0, 2, 7, 2, labelspan=5)
    histogram_module = Histogram(histogram_frame, listener)
    listener.attach_module(HISTOGRAM, histogram_module)

    # absorption
    (absorption_spec_frame, absorption_spec_label) = frame_and_label(image_diagram, "Absorption Spectrum", PASTEL_PINK_RGB, 7, 2, 7, 2, labelspan=5)
    absorption_module = AbsorptionSpec(absorption_spec_frame, listener)
    listener.attach_module(ABSORPTION_SPEC, absorption_module)

    window.mainloop()

if __name__ == '__main__':
    main()
    