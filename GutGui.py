from GutGuiModules.constants import *
from GutGuiModules.utility import *
from GutGuiModules.absorption_spec import AbsorptionSpec
from GutGuiModules.analysis_and_form import AnalysisAndForm
from GutGuiModules.diagram import Diagram
from GutGuiModules.histogram import Histogram
from GutGuiModules.new_colour import NewColour
from GutGuiModules.original_colour import OGColour
from GutGuiModules.source_and_output import SourceAndOutput
from GutGuiModules.save import Save

def main():
    window = init()

    # source and output
    (source_and_output_frame, sno_label) = frame_and_label(window, "Source & Output",
                                                           PASTEL_BLUE_RGB, SMALL_W, SMALL_H, 0, 0, 1, 1)
    source_and_output_module = SourceAndOutput(source_and_output_frame)

    # analysis and form
    (analysis_and_form_frame, anf_label) = frame_and_label(window, "Analysis & Form",
                                                           PASTEL_ORANGE_RGB, SMALL_W, BIG_H, 1, 0, 2, 1)
    analysis_and_form_module = AnalysisAndForm(analysis_and_form_frame)

    # save
    (save_frame, s_label) = frame_and_label(window, "Save",
                                            PASTEL_PINK_RGB, SMALL_W, SMALL_H, 3, 0, 1, 1)
    save_module = Save(save_frame)
    
    # original colour
    (og_color_frame, ogc_label) = frame_and_label(window, "Original Colour-Coded Image",
                                                  PASTEL_PINK_RGB, BIG_W, BIG_H, 0, 1, 2, 2)
    
    # recreated colour
    (recreated_color_frame, recreated_color_label) = frame_and_label(window, "Recreated Color-Coded Image",
                                                                     PASTEL_BLUE_RGB, SMALL_W, BIG_H, 2, 1, 2, 1)
    
    # new colour
    (new_color_frame, new_color_label) = frame_and_label(window, "New Color-Coded Image",
                                                         PASTEL_ORANGE_RGB, SMALL_W, BIG_H, 2, 2, 2, 1)
    
    # diagram
    (diagram_frame, diagram_label) = frame_and_label(window, "Diagram Image",
                                                     PASTEL_ORANGE_RGB, BIG_W, SMALL_H, 0, 3, 1, 2)
    
    # histogram
    (histogram_frame, histogram_label) = frame_and_label(window, "Histogram",
                                                         PASTEL_BLUE_RGB, BIG_W, BIG_H, 1, 3, 1, 2)
    
    # absorption
    (absorption_spec_frame, absorption_spec_label) = frame_and_label(window, "Absorption Spectrum",
                                                                     PASTEL_PINK_RGB, BIG_W, BIG_H, 2, 3, 2, 2)

    window.mainloop()

if __name__ == '__main__':
    main()