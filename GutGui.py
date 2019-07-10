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
    (og_color_frame, ogc_label) = frame_and_label(image_diagram, "Original Image", PASTEL_PINK_RGB, 0, 0, 7, 5, labelspan=8)
    og_color_module = OGColour(og_color_frame, listener)
    listener.attach_module(ORIGINAL_COLOUR, og_color_module)

    # original colour data
    (og_color_data_frame, ogc_data_label) = frame_and_label(image_diagram, "Original Image Data", PASTEL_PINK_RGB, 2, 12, 3, 2, labelspan=1)
    og_color_data_module = OGColourData(og_color_data_frame, listener)
    listener.attach_module(ORIGINAL_COLOUR_DATA, og_color_data_module)
    ogc_data_label.grid(padx=15, pady=(15, 10))

    # recreated colour
    (recreated_color_frame, recreated_color_label) = frame_and_label(image_diagram, "Recreated Image", PASTEL_BLUE_RGB, 7, 0, 7, 3, labelspan=5)
    recreated_color_module = RecColour(recreated_color_frame, listener)
    listener.attach_module(RECREATED_COLOUR, recreated_color_module)

    # recreated colour data
    (rec_color_data_frame, rec_data_label) = frame_and_label(image_diagram, "Recreated Image Data", PASTEL_ORANGE_RGB, 5, 12, 3, 2, labelspan=1)
    rec_color_data_module = RecreatedColourData(rec_color_data_frame, listener)
    listener.attach_module(RECREATED_COLOUR_DATA, rec_color_data_module)
    rec_data_label.grid(padx=15, pady=(15, 10))

    # new colour
    (new_color_frame, new_color_label) = frame_and_label(image_diagram, "New Image", PASTEL_ORANGE_RGB, 7, 3, 7, 3, labelspan=5)
    new_color_module = NewColour(new_color_frame, listener)
    listener.attach_module(NEW_COLOUR, new_color_module)

    # new colour data
    (new_color_data_frame, new_data_label) = frame_and_label(image_diagram, "New Image Data", PASTEL_BLUE_RGB, 8, 12, 3, 2, labelspan=1)
    new_color_data_module = NewColourData(new_color_data_frame, listener)
    listener.attach_module(NEW_COLOUR_DATA, new_color_data_module)
    new_data_label.grid(padx=15, pady=(15, 10))

    # diagram
    (diagram_frame, diagram_label) = frame_and_label(image_diagram, "Diagram",PASTEL_ORANGE_RGB, 0, 12, 2, 2, labelspan=1)
    diagram_module = Diagram(diagram_frame, listener)
    listener.attach_module(DIAGRAM, diagram_module)

    # histogram
    (histogram_frame, histogram_label) = frame_and_label(image_diagram, "Histogram", PASTEL_BLUE_RGB, 0, 5, 7, 7, labelspan=5)
    histogram_module = Histogram(histogram_frame, listener)
    listener.attach_module(HISTOGRAM, histogram_module)

    # absorption
    (absorption_spec_frame, absorption_spec_label) = frame_and_label(image_diagram, "Absorption Spectrum", PASTEL_PINK_RGB, 7, 6, 7, 6, labelspan=5)
    absorption_module = AbsorptionSpec(absorption_spec_frame, listener)
    listener.attach_module(ABSORPTION_SPEC, absorption_module)

    # colourbar
    colour_frame = frame_and_label(image_diagram, "Colour", PASTEL_PINK_RGB, 11, 12, 3, 2, labelspan=5, label=False)
    colour_module = Colour(colour_frame, listener)

    window.mainloop()

if __name__ == '__main__':
    main()
