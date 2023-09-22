from flask_app import app
from flask_app.controllers import posting_controller, user_controller
from datetime import datetime

@app.template_filter('format_datetime')
def format_datetime(value, format='%B %d, %Y %I:%M %p'):
    """Convert a datetime to a different format."""
    if isinstance(value, str):
        value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    return value.strftime(format)

if __name__=="__main__":
    app.run(debug=True)
