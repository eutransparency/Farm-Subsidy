from django.template.loader import select_template

def country_template(path, country):
    """
    Wrapper function for select_template.
    
    Given a path, split on '/', prefix the last part (the file name) with 
    __country__, pass it to select_template and return a string for use with 
    render_to_response.
    
    For Example:
        country_template('locations/all_locations.html', 'GB')
    Will look for:
        locations/GB_all_locations.html
    Then:
        locations/all_locations.html

    """
    
    # First parse the path
    path = path.split('/')
    filename = path[-1]
    names_to_try = ["%s_%s" % (country, filename), filename]
    return select_template(names_to_try).name
