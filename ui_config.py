class UI_Config():
    width = 800
    height = 600

    min_zoom = 65
    dpi_zoom = min_zoom
    max_zoom = 140

    header_spacing = 15

    current_page_number = 1
    max_page_number = 1

    current_directory = ""

    def update_zoom_lim(screenSize):
        UI_Config.min_zoom = int(screenSize.height() // 13)
        UI_Config.max_zoom = int(screenSize.height() // 7)
        UI_Config.dpi_zoom = UI_Config.min_zoom

#setdpi as the "zoom method"