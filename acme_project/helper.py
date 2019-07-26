from magic import *


def get_file_mime_type(file_obj_or_name):

    """
    Returns the mime type of the uploaded file using magic library
    """
    mime_type = magic.from_buffer(file_obj_or_name.read(), mime=True)
    return mime_type
