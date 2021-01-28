# -*- coding: utf-8 -*-

from odoo import http, _
from odoo.http import request
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.addons.website.controllers.main import Website
from odoo.exceptions import UserError
import json
from datetime import datetime
from odoo.addons.web.controllers.main import ensure_db, Home
from odoo.exceptions import AccessError, MissingError

from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.payment.controllers.portal import PaymentProcessing

import logging
import base64
_logger = logging.getLogger(__name__)


class ShopTree(http.Controller):







    def christmas_mail(self, email_to, mail_temp_id, dear_name, mail_msg, website_url, sign_up):
        msg_vals_manager = {
            'subject': 'Merry Christmas',
            'email_to': email_to,
            'body_html': """

                                    <div bgcolor="#eee" height="100%!important" marginheight="0" marginwidth="0" style="height:100%!important;margin:0;padding:0;width:100%!important;background-color:#eee;font-family:Arial,Helvetica,san-serif" width="100%!important">
                                    <center>
                                    <table bgcolor="#eee" border="0" cellpadding="0" cellspacing="0" style="background-color:#eee;max-width:520px" width="100%">
                                    <tbody>
                                    <tr>
                                    <td>
                                    <img src='shop/static/src/images/email-Christmas-2.jpg'/>

                                    <img src="data:image/png;base64,${mail_temp_id.template_img}" style="width: 150px;height: 80px;" />
                                    <img src="data:image/png;base64,iV/+OkI=" style="width: 150px;height: 80px;" />

                                    </td>
                                    </tr>

                                    <tr>
                                    <td bgcolor="#ffffff" colspan="3" style="padding:19px 40px;border-left:solid #bebebe 1px;border-right:solid #bebebe 1px;border-bottom:solid #bebebe 1px">
                                    <p style="margin-top:7px;margin-bottom:17px;font-family:Arial,Helvetica,san-serif;font-size:14px;color:#222222">

                                    Dear """ + str(dear_name) + """,

                                    </p>
                                    <p style="margin-top:7px;margin-bottom:7px;font-family:Arial,Helvetica,san-serif;font-size:14px;color:#222222">
                                    """ + str(mail_msg) + """
                                    </p>
                                    
                                    <div style="margin: 16px 0px 16px 0px;">
                                        <a href=" """ + str(sign_up) + """ "
                                        style="background-color: #875A7B; padding: 8px 16px 8px 16px; text-decoration: none; color: #fff; border-radius: 5px; font-size:13px;">
                                            Accept invitation
                                        </a>
                                    </div>
                                    
                                    Your Odoo domain is: <b><a href=' """ + str(website_url) + """ '>""" + str(
                website_url) + """</a></b><br />
                                    Your sign in email is: <b><a href="/web/login?login=""" + str(
                email_to) + """" target="_blank">""" + str(email_to) + """</a></b><br /><br />
                                    </td>
                                    </tr>
                                    <tr>
                                    </tr>
                                    </tbody></table>
                                    </center>
                                    </div> """
        }
        msg_id_managaer = request.env['mail.mail'].create(msg_vals_manager)
        msg_id_managaer.send()

























    @http.route('/get_country', auth='public', type='http', website=True, methods=['POST'], csrf=False)
    def get_country(self, **kw):

        country_ids = request.env['res.country'].sudo().search([])
        data = {}
        country_list = []
        for country in country_ids:
            country_list.append({'id': country.id, 'value': country.name})

        if country_list:
            data['countries'] = country_list
        return json.dumps(data)

    @http.route('/get_year', auth='public', type='http', website=True, methods=['POST'], csrf=False)
    def get_year(self, **kw):

        uid = http.request.env.context.get('uid')

        year_list = sorted([str(num) for num in range(1942, ((datetime.now().year) + 1))], reverse=True)
        month_list = ['January', 'Feburary', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                      'November', 'December']
        days_list = [x for x in range(1, 31)]

        data = {}
        data = {'year': year_list, 'months': month_list, 'days': days_list}

        return json.dumps(data)



    @http.route('/gift_a_tree', type="http", auth="public", website=True)
    def gift_a_tree(self, **kwargs):
        return http.request.render('shop.gift_tree', {})

    @http.route('/gift-data', auth='public', type='http', website=True)
    def gift_data(self,**post):

        index = post.get("active-slider")
        dear_name = post.get("dear_name")
        mail_msg = post.get("mail_msg")
        email = post.get("email")

        user_ob = request.env['res.users'].sudo().search([('login', '=', email)])

        mail_temp_id = request.env['mail.template'].sudo().search([('id', '=', index)])

        website_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')

        if not user_ob:

            new_user_id = request.env['res.users'].sudo().create({'name': dear_name, 'login': email})

            # user = request.env.user

            new_user_id.partner_id._compute_signup_url()
            # user.partner_id._compute_signup_url()

            sign_up = new_user_id.partner_id.signup_url
            # sign_up = user.partner_id.signup_url


            if post.get('tree_id'):
                sale_detail_obj = request.env['website.sale.detail'].sudo().search([('tree_id', '=', post.get('tree_id'))])

                sale_detail_obj.update({'res_partner_id': new_user_id.partner_id, 'is_gift': True,})


            template_list = mail_temp_id.name.split(" ")

            if 'Christmas' in template_list:

                self.christmas_mail(email, mail_temp_id, dear_name, mail_msg, website_url, sign_up)



            if 'Winter' in template_list:
                msg_vals_manager = {
                    'subject': 'Winter is Coming',
                    'email_to': email,
                    'body_html': """
    
                                            <div bgcolor="#eee" height="100%!important" marginheight="0" marginwidth="0" style="height:100%!important;margin:0;padding:0;width:100%!important;background-color:#eee;font-family:Arial,Helvetica,san-serif" width="100%!important">
                                            <center>
                                            <table bgcolor="#eee" border="0" cellpadding="0" cellspacing="0" style="background-color:#eee;max-width:520px" width="100%">
                                            <tbody>
                                            <tr>
                                            <td>
                                            <img src='/shop/static/src/images/email-Christmas-2.jpg'/>
    
                                            <img src="data:image/png;base64,""" + str(mail_temp_id.template_img) + """" " style="width: 150px;height: 80px;" />
    
                                            </td>
                                            </tr>
    
                                            <tr>
                                            <td bgcolor="#ffffff" colspan="3" style="padding:19px 40px;border-left:solid #bebebe 1px;border-right:solid #bebebe 1px;border-bottom:solid #bebebe 1px">
                                            <p style="margin-top:7px;margin-bottom:17px;font-family:Arial,Helvetica,san-serif;font-size:14px;color:#222222">
    
                                            Dear """ + str(dear_name) + """,
    
                                            </p>
                                            <p style="margin-top:7px;margin-bottom:7px;font-family:Arial,Helvetica,san-serif;font-size:14px;color:#222222">
                                            """ + str(mail_msg) + """
                                            </p>
                                            <div style="margin: 16px 0px 16px 0px;">
                                                <a href=" """ + str(sign_up) + """ "
                                                style="background-color: #875A7B; padding: 8px 16px 8px 16px; text-decoration: none; color: #fff; border-radius: 5px; font-size:13px;">
                                                    Accept invitation
                                                </a>
                                            </div>
                                            Your Odoo domain is: <b><a href=' """ + str(website_url) + """ '>""" + str(
                        website_url) + """</a></b><br />
                                            Your sign in email is: <b><a href="/web/login?login=""" + str(
                        email) + """" target="_blank">""" + str(email) + """</a></b><br /><br />
                                            </td>
                                            </tr>
                                            <tr>
                                            </tr>
                                            </tbody></table>
                                            </center>
                                            </div> """
                }
                msg_id_managaer = request.env['mail.mail'].create(msg_vals_manager)
                msg_id_managaer.send()


        else :

            if post.get('tree_id'):
                sale_detail_obj = request.env['website.sale.detail'].sudo().search([('tree_id', '=', post.get('tree_id'))])

                sale_detail_obj.update({'res_partner_id': user_ob.partner_id, 'is_gift': True,})

                sign_up = user_ob.partner_id.signup_url

                template_list = mail_temp_id.name.split(" ")

                if 'Christmas' in template_list:
                    self.christmas_mail(email, mail_temp_id, dear_name, mail_msg, website_url, sign_up)

                else :
                    self.christmas_mail(email, mail_temp_id, dear_name, mail_msg, website_url, sign_up)




        return request.render('shop.gift_thanks', {})


    @http.route('/email-data', auth='public', type='http', website=True)
    def email_data(self, **post):
        dear_name = post.get("res_id")
        mail_msg = post.get("mail_id")

        return request.render('shop.thankyou_email', {'dear_name': dear_name, 'mail_detail': mail_msg})


    @http.route('/gift-thanks', auth='public', type='http', website=True)
    def gift_thanks(self, **post):
        mail_detail = post.get("email")
        msg = post.get("res_id") + post.get("mail_id")
        mail = request.env['mail.mail']
        values = {
            'subject': "Thank u for gifting",
            'body_html': msg,
            'email_to': mail_detail,
        }
        mail.sudo().create(values).send()
        return request.render('shop.gift_thanks', {'email': mail_detail})




    @http.route('/cart', type="http", auth="public", website=True)
    def search_cart(self, **kwargs):
        return http.request.render('shop.shop_cart', {})

    @http.route('/shopping-thankyou', type="http", auth="public", website=True)
    def thank_you_shop(self, **kwargs):
        return http.request.render('shop.shop_thank', {})

    @http.route('/tree-quantity', type="http", auth="public", website=True)
    def tree_quantity(self, **kwargs):
        return http.request.render('shop.tree_quantity', {})

    @http.route('/aboutus', type="http", auth="public", website=True)
    def about_tree(self, **kwargs):
        return http.request.render('shop.about-us', {})

    @http.route('/gift-a-tree', type="http", auth="public", website=True)
    def gift_tree(self, **kwargs):

        email_template = request.env['mail.template'].sudo().search([('web_template', '=', True)]).sorted('id')

        if kwargs.get('tree_id'):
            values = {
                'templates': email_template,
                'tree_id': kwargs.get('tree_id'),
            }
            return http.request.render('shop.gift_tree', values)
        else:
            values = {
                'templates': email_template
            }
            return http.request.render('shop.gift_tree', values)

    @http.route('/gift-a-tree-1', type="http", auth="public", website=True)
    def gift_tree_1(self, **post):
        dear_name = post.get("dear_name")
        mail_msg = post.get("mail_msg")
        return http.request.render('shop.gift_tree_1', {})

    @http.route('/plant-a-tree', type="http", auth="public", website=True)
    def plant_a_tree(self, **kwargs):
        return http.request.render('shop.plant_trees', {})

    @http.route('/plant-a-tree1', type="http", auth="public", website=True)
    def plant_trees_1(self, **kwargs):
        return http.request.render('shop.pllant', {})

    @http.route('/old-member', type="http", auth="public", website=True)
    def old_product(self, **kwargs):
        return http.request.render('shop.old_membership', {})

    @http.route('/payment-option'
                '', type="http", auth="public", website=True)
    def payment_product(self, **kwargs):
        return http.request.render('shop.pay_option', {})

    @http.route('/login-1'
                '', type="http", auth="public", website=True)
    def login_info(self, **kwargs):
        return http.request.render('shop.login_info', {})

    @http.route('/login1', type="http", auth="public", website=True)
    def login_trees(self, **kwargs):
        return http.request.render('shop.login_info_earth', {})

    @http.route('/register-detail', type="http", auth="public", website=True)
    def register_trees(self, **kwargs):
        return http.request.render('shop.register_info_detail', {})

    @http.route('/my-tress', type="http", auth="public", website=True)
    def trees_selecting(self, **kwargs):
        return http.request.render('shop.trees_select', {})



    @http.route('/', type="http", auth="public", website=True)
    def home_page(self, **kwargs):
        return http.request.render('shop.home', {})





class CustomerPortal(CustomerPortal):



    def _tree_get_page_view_values(self, tree, access_token, **kwargs):
        values = {
            'page_name': 'trees',
            'tree': tree,
            'user': request.env.user
        }
        return self._get_page_view_values(tree, access_token, values, 'my_trees_history', False, **kwargs)


    @http.route(['/my/trees', '/my/trees/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_quotes(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        PortalUserTree = request.env['website.sale.detail']

        domain = [
            ('res_partner_id', '=', partner.id)
        ]

        # searchbar_sortings = {
        #     'date': {'label': _('Order Date'), 'order': 'date_order desc'},
        #     'name': {'label': _('Reference'), 'order': 'name'},
        #     'stage': {'label': _('Stage'), 'order': 'state'},
        # }

        # default sortby order
        # if not sortby:
        #     sortby = 'date'
        # sort_order = searchbar_sortings[sortby]['order']
        #
        # if date_begin and date_end:
        #     domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # count for pager
        tree_count = PortalUserTree.sudo().search_count(domain)

        # make pager
        pager = portal_pager(
            url="/my/trees",
            # url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=tree_count,
            page=page,
            step=self._items_per_page
        )
        # search the count to display, according to the pager data
        # quotations = PortalUserTree.search(domain, order=sort_order, limit=self._items_per_page, offset=pager['offset'])
        trees = PortalUserTree.sudo().search(domain, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_trees_history'] = trees.ids[:100]

        values.update({
            'trees': trees.sudo(),
            'page_name': 'tree',
            'pager': pager,
            'default_url': '/my/trees',
        })
        return request.render("shop.portal_my_trees", values)


    @http.route(['/my/trees/<int:tree_id>'], type='http', auth="public", website=True)
    def portal_my_trees(self, tree_id, access_token=None, **kw):
        try:
            trees_sudo = self._document_check_access('website.sale.detail', tree_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/old-member')

        # ensure attachment are accessible with access token inside template
        # for attachment in task_sudo.attachment_ids:
        #     attachment.generate_access_token()
        values = self._tree_get_page_view_values(trees_sudo, access_token, **kw)
        return request.render("shop.portal_my_tree", values)








class CustomController(AuthSignupHome):

    def do_signup(self, qcontext):
        """ Shared helper that creates a res.partner out of a token """
        values = { key: qcontext.get(key) for key in ('login', 'name', 'password') }
        if not values:
            raise UserError(_("The form was not properly filled in."))
        if values.get('password') != qcontext.get('confirm_password'):
            raise UserError(_("Passwords do not match; please retype them."))
        supported_lang_codes = [code for code, _ in request.env['res.lang'].get_installed()]
        lang = request.context.get('lang', '').split('_')[0]
        if lang in supported_lang_codes:
            values['lang'] = lang

        if qcontext.get('age_day', False):
            values.update({'day': qcontext.get('age_day', False)})

        if qcontext.get('age_month', False):
            values.update({'month': qcontext.get('age_month', False)})

        if qcontext.get('age_year', False):
            values.update({'year': qcontext.get('age_year', False)})

        if qcontext.get('cellnumber', False):
            values.update({'mobile': qcontext.get('cellnumber', False)})

        if qcontext.get('city', False):
            values.update({'city': qcontext.get('city', False)})

        if qcontext.get('select_country', False):
            country_id = qcontext.get('select_country', False)
            if country_id:
                values.update({'country_id': int(country_id)})

        if qcontext.get('bank_st_front_pg_attachment', False):
            self.attachment_ = request.env['ir.attachment']
            Attachments = self.attachment_
            name = qcontext.get('bank_st_front_pg_attachment').filename
            file = qcontext.get('bank_st_front_pg_attachment')
            attachment = file.read()
            attachment_id = Attachments.sudo().create({
                'name': name,
                'display_name': name,
                'res_name': name,
                'type': 'binary',
                'res_model': 'res.users',
                'res_id': 4,
                # 'datas': attachment.encode('base64'),
                'datas': base64.standard_b64encode(attachment)
            })

            values.update({
                'image_1920': base64.standard_b64encode(attachment),
            })


        if qcontext.get('gender_selection', False):
            gender = qcontext.get('gender_selection', False)
            if gender == 'male':
                values.update({'gender': 'male'})
            elif gender == 'female':
                values.update({'gender': 'female'})
            else:
                values.update({'gender': 'others'})

        self._signup_with_values(qcontext.get('token'), values)
        request.env.cr.commit()






class CustomWebsiteController(Website):

    # ------------------------------------------------------
    # Login - overwrite of the web login so that regular users are redirected to the backend
    # while portal users are redirected to the frontend by default
    # ------------------------------------------------------

    def _login_redirect(self, uid, redirect=None):
        """ Redirect regular users (employees) to the backend) and others to
        the frontend
        """
        if not redirect and request.params.get('login_success'):
            if request.env['res.users'].browse(uid).has_group('base.group_user'):
                redirect = b'/web?' + request.httprequest.query_string
            else:
                # redirect = '/my'
                redirect = '/old-member'
        return super()._login_redirect(uid, redirect=redirect)







class CustomWebsiteSale(WebsiteSale):

    @http.route('/shop/payment/validate', type='http', auth="public", website=True, sitemap=False)
    def payment_validate(self, transaction_id=None, sale_order_id=None, **post):
        """ Method that should be called by the server when receiving an update
        for a transaction. State at this point :

         - UDPATE ME
        """
        if sale_order_id is None:
            order = request.website.sale_get_order()
        else:
            order = request.env['sale.order'].sudo().browse(sale_order_id)
            assert order.id == request.session.get('sale_last_order_id')

        if transaction_id:
            tx = request.env['payment.transaction'].sudo().browse(transaction_id)
            assert tx in order.transaction_ids()
        elif order:
            tx = order.get_portal_last_transaction()
        else:
            tx = None

        if not order or (order.amount_total and not tx):
            return request.redirect('/shop')

        if order and not order.amount_total and not tx:
            order.with_context(send_email=True).action_confirm()
            return request.redirect(order.get_portal_url())

        # clean context and session, then redirect to the confirmation page
        request.website.sale_reset()
        if tx and tx.state == 'draft':
            return request.redirect('/shop')

        PaymentProcessing.remove_payment_transaction(tx)

        if order.state == 'sale' and tx.state == 'done':
            partner = request.env.user.partner_id

            for line in order.order_line:
                partner_sale_line = request.env['website.sale.detail'].sudo().create({'product_tree_name': line.product_id.id, 'is_gift': False, 'qty': line.product_uom_qty, 'res_partner_id': partner.id})
                print(partner_sale_line)

                partner.write({'sale_detail_ids': [(4, partner_sale_line.id)]})

        # return request.redirect('/shop/confirmation')
        return request.redirect('/shopping-thankyou', {'tree_id': partner_sale_line.tree_id})












