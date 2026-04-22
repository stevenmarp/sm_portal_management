{
    'name': 'Portal Documents Management',
    'version': '17.0.1.0.0',
    'category': 'Portal',
    'summary': 'Share documents and directories with portal users. '
               'Create directories, upload files, and manage access via followers.',
    'description': """
Portal Documents Management
===========================
Allow portal users to browse, upload, and download documents organized
in a directory structure. Access is controlled through the follower mechanism:
only followers of a directory can see its content in the portal.

Key Features:
- Create directories and sub-directories from portal
- Upload and download documents from portal
- Follower-based access control
- Portal users can create directories and upload files (if allowed)
- Backend kanban, list, and form views
- Dynamic file type icons
    """,
    'author': 'Steven Marp',
    'depends': ['portal', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/ir_rules.xml',
        'views/actions.xml',
        'views/portal_directory_views.xml',
        'views/portal_document_views.xml',
        'views/portal_templates.xml',
        'views/menu.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'sm_portal_document/static/src/scss/portal.scss',
        ],
    },
    'images': ['static/description/banner.gif'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'OPL-1',
    'price': 35.66,
    'currency': 'USD',
}
