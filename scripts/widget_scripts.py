import ipywidgets as widgets

def get_checkboxes(list):

    return [widgets.Checkbox(description=item, value=False) for item in list]

def get_Hbox(checkboxes):

    return widgets.HBox(checkboxes)

def get_Hbox_from_list(list):

    checkbox_list = get_checkboxes(list)
    return get_Hbox(checkbox_list)

def get_gridbox(checkboxes):

    return widgets.GridBox(checkboxes, layout=widgets.Layout(grid_template_columns="repeat(4, 250px)"))

def get_gridbox_from_list(list):

    checkbox_list = get_checkboxes(list)
    return get_gridbox(checkbox_list)

def get_selected_checkboxes(container):

    return [w.description for w in container.children if w.value]
