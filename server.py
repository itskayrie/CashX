from flask_app import app

from flask_app.controller import employee_controller
from flask_app.controller import owner_controller
from flask_app.controller import article_controller
from flask_app.controller import recipes_controller
from flask_app.controller import purchase_controller
from flask_app.controller import ticket_controller
from flask_app.controller import pointing_controller



# -------------------------------------------
if __name__=="__main__":   # Ensure this file is being run directly and not from a different module    
    app.run(debug=True)    # Run the app in debug mode.

