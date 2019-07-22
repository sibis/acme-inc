import os
from magic import *


def form_error_to_list(form_obj):
    """
    Simply putting every form errors into a list.
    Helpful to use with ajax based views
    """
    msgs = []
    if form_obj.errors:
        #For each field in form
        for field in form_obj:
            #For each error in field
            for error in field.errors:
                msgs.append("{} - {}".format(field.label,error))
                
    if form_obj.non_field_errors():
        for error in form_obj.non_field_errors():
            msgs.append(error)

    return msgs


def get_file_mime_type(file_obj_or_name):
    mime_type = magic.from_buffer(file_obj_or_name.read(),mime=True)
    return mime_type