import pkg_resources

from tutor import hooks

from .__about__ import __version__


################# Configuration
config = {
    # Add here your new settings
    "defaults": {
        "VERSION": __version__,
        "WELCOME_MESSAGE": "The place for all your online learning",
        "PRIMARY_COLOR": "#3b85ff",  # cool blue
        # Footer links are dictionaries with a "title" and "url"
        # To remove all links, run:
        # tutor config save --set XNETZ_FOOTER_NAV_LINKS=[] --set XNETZ_FOOTER_LEGAL_LINKS=[]
        "FOOTER_NAV_LINKS": [
            {"title": "About", "url": "/about"},
            {"title": "Contact", "url": "/contact"},
        ],
        "FOOTER_LEGAL_LINKS": [
            {"title": "Terms of service", "url": "/tos"},
            {
                "title": "Xnetz Indigo theme for Open edX",
                "url": "https://github.com/blend-ed/tutor-indigo-xnetz",
            },
        ],
    },
    "unique": {},
    "overrides": {},
}

# Theme templates
hooks.Filters.ENV_TEMPLATE_ROOTS.add_item(
    pkg_resources.resource_filename("tutorxnetz", "templates")
)
# This is where the theme is rendered in the openedx build directory
hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    [
        ("xnetz", "build/openedx/themes"),
    ],
)

# Force the rendering of scss files, even though they are included in a "partials" directory
hooks.Filters.ENV_PATTERNS_INCLUDE.add_item(
    r"xnetz/lms/static/sass/partials/lms/theme/"
)

# Load all configuration entries
hooks.Filters.CONFIG_DEFAULTS.add_items(
    [(f"XNETZ_{key}", value) for key, value in config["defaults"].items()]
)
hooks.Filters.CONFIG_UNIQUE.add_items(
    [(f"XNETZ_{key}", value) for key, value in config["unique"].items()]
)
hooks.Filters.CONFIG_OVERRIDES.add_items(list(config["overrides"].items()))


hooks.Filters.ENV_PATCHES.add_items(
    [
        (
            "mfe-dockerfile-post-npm-install-learning",
            """
RUN npm install '@edx/brand@git+https://github.com/blend-ed/brand-openedx-xnetz.git'
RUN npm install '@edx/frontend-component-header@npm:@edly-io/indigo-frontend-component-header@^1.0.0'
RUN npm install '@edx/frontend-component-footer@git+https://github.com/blend-ed/frontend-component-footer-xnetz.git'
""",
        ),
        (
            "mfe-dockerfile-post-npm-install-authn",
            """
RUN npm install '@edx/brand@git+https://github.com/blend-ed/brand-openedx-xnetz.git'
""",
        ),
        # Tutor-Indigo v2.1 targets the styling updations in discussions and learner-dashboard MFE
        # brand-openedx is related to styling updates while others are for header and footer updates
        (
            "mfe-dockerfile-post-npm-install-discussions",
            """
RUN npm install '@edx/brand@git+https://github.com/blend-ed/brand-openedx-xnetz.git'
RUN npm install '@edx/frontend-component-header@npm:@edly-io/indigo-frontend-component-header@^1.0.0'
RUN npm install '@edx/frontend-component-footer@git+https://github.com/blend-ed/frontend-component-footer-xnetz.git'
""",
        ),
        (
            "mfe-dockerfile-post-npm-install-learner-dashboard",
            """
RUN npm install '@edx/brand@git+https://github.com/blend-ed/brand-openedx-xnetz.git'
RUN npm install '@edx/frontend-component-footer@git+https://github.com/blend-ed/frontend-component-footer-xnetz.git'
""",
        ),
    ]
)
