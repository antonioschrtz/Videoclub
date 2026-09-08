{
    "name": "Video Club",
    "summary": """
        Short summary of the module's purpose.
    """,
    "technical_description": """
        A simple module to manage a video club.
    """,
    "author": "Antonio",
    "website": "http://www.aserti.es",
    "license": "LGPL-3",
    "category": "Sales",
    "version": "15.0.1.0.1",
    "application": True,
    "depends": ["base"],
    "data": [
        "security/videoclub_groups.xml",
        "security/ir.model.access.csv",
        "views/menu.xml",
        "views/movie.xml",
        "views/tape.xml",
        "views/director.xml",
        "wizard/movie_wizard.xml",
        "views/templates.xml",
    ],
    "installable": True,
    "demo": [
        "demo/demo.xml",
    ],
}
