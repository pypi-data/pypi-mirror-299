"""Take screenshot of stimulus"""

# The category determines the group for the plugin in the item toolbar
category = "Screenshot"
# Defines the GUI controls
controls = [
    {
        "type": "checkbox",
        "var": "verbose",
        "label": "Verbose mode",
        "name": "checkbox_verbose_mode",
        "tooltip": "Run in verbose mode"
    },  {
        "type": "checkbox",
        "var": "window_stim",
        "label": "Stimulus display",
        "name": "checkbox_window_stim",
        "tooltip": "Stimulus display"
    },  {
        "type": "checkbox",
        "var": "window_full",
        "label": "Composite of all displays",
        "name": "checkbox_window_full",
        "tooltip": "Composite of all displays"
    },  {
        "type": "line_edit",
        "var": "filename_screenshot",
        "label": "Filename",
        "name": "line_edit_filename_screenshot",
        "tooltip": "Filename"
    }, {
        "type": "text",
        "label": "<small>Screenshot version 0.1.1</small>"
    }
]
