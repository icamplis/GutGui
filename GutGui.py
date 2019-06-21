from GutGuiModules import *
from tkinter import *

def main():
    (window, input_output, image_diagram) = init()

    # source and output
    (source_and_output_frame, sno_label) = frame_and_label(input_output, "Source & Output", PASTEL_BLUE_RGB, 0, 0, 1, 1, labelspan=2)
    source_and_output_module = SourceAndOutput(source_and_output_frame)

    # analysis and form
    (analysis_and_form_frame, anf_label) = frame_and_label(input_output, "Analysis & Form", PASTEL_ORANGE_RGB, 0, 1, 2, 1, labelspan=8)
    analysis_and_form_module = AnalysisAndForm(analysis_and_form_frame)

    # save
    (save_frame, s_label) = frame_and_label(input_output, "Save",PASTEL_PINK_RGB, 1, 0, 1, 1, labelspan=2)
    s_label.grid(padx=(150, 0))
    save_module = Save(save_frame)

    # original colour
    (og_color_frame, ogc_label) = frame_and_label(image_diagram, "Original Image", PASTEL_PINK_RGB, 0, 0, 7, 2)

    # recreated colour
    (recreated_color_frame, recreated_color_label) = frame_and_label(image_diagram, "Recreated Image", PASTEL_BLUE_RGB, 7, 0, 7, 1, labelspan=5)
    recreated_color_module = RecColour(recreated_color_frame)

    # new colour
    (new_color_frame, new_color_label) = frame_and_label(image_diagram, "New Image", PASTEL_ORANGE_RGB, 7, 1, 7, 1, labelspan=5)
    new_color_module = NewColour(new_color_frame)

    # diagram
    # (diagram_frame, diagram_label) = frame_and_label(image_diagram, "Diagram",PASTEL_ORANGE_RGB, 13, 0, 1, 2, labelspan=2)
    # diagram_module = Diagram(diagram_frame)

    # histogram
    (histogram_frame, histogram_label) = frame_and_label(image_diagram, "Histogram", PASTEL_BLUE_RGB, 0, 2, 7, 2, labelspan=5)
    histogram_module = Histogram(histogram_frame)

    # absorption
    (absorption_spec_frame, absorption_spec_label) = frame_and_label(image_diagram, "Absorption Spectrum", PASTEL_PINK_RGB, 7, 2, 7, 2, labelspan=5)
    absorption_module = AbsorptionSpec(absorption_spec_frame)

    window.mainloop()

if __name__ == '__main__':
    main()