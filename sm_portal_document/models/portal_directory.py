from odoo import api, fields, models


class PortalDirectory(models.Model):
    _name = 'sm.portal.directory'
    _inherit = ['mail.thread', 'portal.mixin']
    _description = 'Portal Directory'
    _order = 'name'

    name = fields.Char(required=True, tracking=True)
    parent_id = fields.Many2one(
        'sm.portal.directory', string='Parent Directory',
        ondelete='cascade', index=True)
    child_ids = fields.One2many(
        'sm.portal.directory', 'parent_id', string='Sub Directories')
    document_ids = fields.One2many(
        'sm.portal.document', 'directory_id', string='Documents')
    description = fields.Text()
    user_id = fields.Many2one(
        'res.users', string='Owner',
        default=lambda self: self.env.user, tracking=True)
    allow_portal_upload = fields.Boolean(
        string='Allow Portal Upload',
        help='Allow portal followers to upload documents and create sub-directories.')
    child_count = fields.Integer(compute='_compute_child_count')
    document_count = fields.Integer(compute='_compute_document_count')
    full_path = fields.Char(compute='_compute_full_path', store=True)
    icon = fields.Selection([
        ('folder', 'Folder'),
        ('folder-open', 'Folder Open'),
        ('archive', 'Archive'),
        ('briefcase', 'Briefcase'),
        ('book', 'Book'),
    ], default='folder')

    @api.depends('child_ids')
    def _compute_child_count(self):
        for rec in self:
            rec.child_count = len(rec.child_ids)

    @api.depends('document_ids')
    def _compute_document_count(self):
        for rec in self:
            rec.document_count = len(rec.document_ids)

    @api.depends('name', 'parent_id', 'parent_id.full_path')
    def _compute_full_path(self):
        for rec in self:
            parts = []
            current = rec
            while current:
                parts.append(current.name or '')
                current = current.parent_id
            rec.full_path = ' / '.join(reversed(parts))

    def _compute_access_url(self):
        super()._compute_access_url()
        for rec in self:
            rec.access_url = '/my/directories/%s' % rec.id
