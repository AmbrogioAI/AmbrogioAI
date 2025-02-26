
def getClasses():
    
    # get the absolute path of the "utilities" folder
    import os
    utilities_path = os.path.dirname(os.path.abspath(__file__))
    # get the absolute path of the "utilities" folder
    utilities_path = os.path.dirname(utilities_path)
    try:    
        # Get the classes from the file
        with open(utilities_path+'/utilities/classes.txt', 'r') as file:
            classes = file.readlines()
        # Remove the newline characters
        classes = [x.strip() for x in classes]
        return classes
    except Exception as e:
        raise e