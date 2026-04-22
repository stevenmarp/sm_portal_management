import base64
import mimetypes

from odoo import api, fields, models


class PortalDocument(models.Model):
    _name = 'sm.portal.document'
    _inherit = ['mail.thread', 'portal.mixin']
    _description = 'Portal Document'
    _order = 'create_date desc'

    name = fields.Char(required=True, tracking=True)
    directory_id = fields.Many2one(
        'sm.portal.directory', string='Directory',
        required=True, ondelete='cascade', index=True)
    file = fields.Binary(required=True, attachment=True)
    filename = fields.Char()
    file_size = fields.Float(
        compute='_compute_file_size', store=True,
        string='File Size (KB)')
    mimetype = fields.Char(
        compute='_compute_mimetype', store=True)
    description = fields.Text()
    user_id = fields.Many2one(
        'res.users', string='Uploaded By',
        default=lambda self: self.env.user)

    @api.depends('file')
    def _compute_file_size(self):
        for rec in self:
            if rec.file:
                rec.file_size = round(len(base64.b64decode(rec.file)) / 1024, 2)
            else:
                rec.file_size = 0

    @api.depends('filename')
    def _compute_mimetype(self):
        for rec in self:
            if rec.filename:
                rec.mimetype = mimetypes.guess_type(rec.filename)[0] or 'application/octet-stream'
            else:
                rec.mimetype = 'application/octet-stream'

    def _compute_access_url(self):
        super()._compute_access_url()
        for rec in self:
            rec.access_url = '/my/documents/%s' % rec.id

    def _get_file_icon(self):
        """Return font-awesome icon class based on mimetype."""
        self.ensure_one()
        mime = self.mimetype or ''
        if 'image' in mime:
            return 'fa-file-image-o'
        elif 'pdf' in mime:
            return 'fa-file-pdf-o'
        elif 'word' in mime or 'document' in mime:
            return 'fa-file-word-o'
        elif 'excel' in mime or 'spreadsheet' in mime:
            return 'fa-file-excel-o'
        elif 'powerpoint' in mime or 'presentation' in mime:
            return 'fa-file-powerpoint-o'
        elif 'text' in mime:
            return 'fa-file-text-o'
        elif 'zip' in mime or 'compressed' in mime or 'archive' in mime:
            return 'fa-file-archive-o'
        elif 'video' in mime:
            return 'fa-file-video-o'
        elif 'audio' in mime:
            return 'fa-file-audio-o'
        elif 'code' in mime or 'javascript' in mime or 'json' in mime or 'xml' in mime:
            return 'fa-file-code-o'
        return 'fa-file-o'
