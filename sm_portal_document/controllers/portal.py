import base64

from odoo import _, http
from odoo.exceptions import AccessError, MissingError
from odoo.http import content_disposition, request

from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.portal.controllers.portal import pager as portal_pager


class PortalDocument(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'directory_count' in counters:
            Directory = request.env['sm.portal.directory']
            values['directory_count'] = Directory.search_count([]) \
                if Directory.has_access('read') else 0
        return values

    # ------------------------------------------------------------------
    # Directory list
    # ------------------------------------------------------------------
    @http.route(
        ['/my/directories', '/my/directories/page/<int:page>'],
        type='http', auth='user', website=True)
    def portal_my_directories(self, page=1, sortby=None, search=None, **kw):
        Directory = request.env['sm.portal.directory']
        values = self._prepare_portal_layout_values()

        domain = [('parent_id', '=', False)]  # root directories only
        if search:
            domain += [('name', 'ilike', search)]

        searchbar_sortings = {
            'name': {'label': _('Name'), 'order': 'name asc'},
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
        }
        if not sortby:
            sortby = 'name'
        sort_order = searchbar_sortings[sortby]['order']

        directory_count = Directory.search_count(domain)
        pager = portal_pager(
            url='/my/directories',
            total=directory_count,
            page=page,
            step=self._items_per_page,
            url_args={'sortby': sortby, 'search': search},
        )
        directories = Directory.search(
            domain, order=sort_order,
            limit=self._items_per_page, offset=pager['offset'])

        values.update({
            'directories': directories,
            'page_name': 'directories',
            'pager': pager,
            'default_url': '/my/directories',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'search': search or '',
        })
        return request.render('sm_portal_document.portal_my_directories', values)

    # ------------------------------------------------------------------
    # Directory detail (subdirectories + documents)
    # ------------------------------------------------------------------
    @http.route(
        '/my/directories/<int:directory_id>',
        type='http', auth='user', website=True)
    def portal_directory_detail(self, directory_id, **kw):
        try:
            directory = self._document_check_access(
                'sm.portal.directory', directory_id)
        except (AccessError, MissingError):
            return request.redirect('/my/directories')

        values = self._prepare_portal_layout_values()
        values.update({
            'directory': directory,
            'child_dirs': directory.child_ids,
            'documents': directory.document_ids,
            'page_name': 'directory_detail',
        })
        return request.render('sm_portal_document.portal_directory_detail', values)

    # ------------------------------------------------------------------
    # Create sub-directory from portal
    # ------------------------------------------------------------------
    @http.route(
        '/my/directories/<int:directory_id>/create',
        type='http', auth='user', website=True, methods=['POST'])
    def portal_create_directory(self, directory_id, **post):
        try:
            parent = self._document_check_access(
                'sm.portal.directory', directory_id)
        except (AccessError, MissingError):
            return request.redirect('/my/directories')

        if not parent.allow_portal_upload:
            return request.redirect('/my/directories/%s' % directory_id)

        name = post.get('name', '').strip()
        if name:
            new_dir = request.env['sm.portal.directory'].sudo().create({
                'name': name,
                'parent_id': parent.id,
                'user_id': request.env.user.id,
            })
            # Add current user as follower
            new_dir.message_subscribe(
                partner_ids=[request.env.user.partner_id.id])
            # Copy parent followers
            new_dir.message_subscribe(
                partner_ids=parent.message_partner_ids.ids)

        return request.redirect('/my/directories/%s' % directory_id)

    # ------------------------------------------------------------------
    # Create root directory from portal
    # ------------------------------------------------------------------
    @http.route(
        '/my/directories/create',
        type='http', auth='user', website=True, methods=['POST'])
    def portal_create_root_directory(self, **post):
        name = post.get('name', '').strip()
        if name:
            new_dir = request.env['sm.portal.directory'].sudo().create({
                'name': name,
                'user_id': request.env.user.id,
                'allow_portal_upload': True,
            })
            new_dir.message_subscribe(
                partner_ids=[request.env.user.partner_id.id])
        return request.redirect('/my/directories')

    # ------------------------------------------------------------------
    # Upload document from portal
    # ------------------------------------------------------------------
    @http.route(
        '/my/directories/<int:directory_id>/upload',
        type='http', auth='user', website=True, methods=['POST'],
        csrf=True)
    def portal_upload_document(self, directory_id, **post):
        try:
            directory = self._document_check_access(
                'sm.portal.directory', directory_id)
        except (AccessError, MissingError):
            return request.redirect('/my/directories')

        if not directory.allow_portal_upload:
            return request.redirect('/my/directories/%s' % directory_id)

        upload_file = post.get('file')
        if upload_file:
            filename = upload_file.filename
            file_data = base64.b64encode(upload_file.read())
            doc = request.env['sm.portal.document'].sudo().create({
                'name': filename,
                'directory_id': directory.id,
                'file': file_data,
                'filename': filename,
                'user_id': request.env.user.id,
            })
            doc.message_subscribe(
                partner_ids=directory.message_partner_ids.ids)

        return request.redirect('/my/directories/%s' % directory_id)

    # ------------------------------------------------------------------
    # Download document
    # ------------------------------------------------------------------
    @http.route(
        '/my/documents/<int:document_id>/download',
        type='http', auth='user', website=True)
    def portal_download_document(self, document_id, **kw):
        try:
            document = self._document_check_access(
                'sm.portal.document', document_id)
        except (AccessError, MissingError):
            return request.redirect('/my/directories')

        if not document.file:
            return request.redirect('/my/directories/%s' % document.directory_id.id)

        file_content = base64.b64decode(document.file)
        return request.make_response(
            file_content,
            headers=[
                ('Content-Type', document.mimetype or 'application/octet-stream'),
                ('Content-Disposition', content_disposition(document.filename or document.name)),
            ])

    # _document_check_access is inherited from CustomerPortal
