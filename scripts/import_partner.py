url = 'https://jdcdev-weiland-doors-studio-customization-0321-2230310.dev.odoo.com'
db = 'jdcdev-weiland-doors-studio-customization-0321-2230310'
username = 'admin'
password = 'admin'

# url = 'http://127.0.0.1:8069'
# db = 'v13e_weliand_studio_12_march_test'
# username = 'admin'
# password = 'admin'

from xmlrpc import client
import csv
from datetime import datetime
import os

common = client.ServerProxy('{}/xmlrpc/2/common'.format(url))
common.version()
uid = common.authenticate(db, username, password, {})
models = client.ServerProxy('{}/xmlrpc/2/object'.format(url))

start_time = datetime.now()
print(":::::::::::::start::::::::::",start_time)

with open('/home/odoo/Desktop/fatemi/workspace/projects/v13/weiland/weiland-doors_studio_staging/scripts/res_partner.csv', newline='') as csv_file:

    csv_file = csv.DictReader(csv_file)
    xls_row = []
    excel_row = 2
    
    for row in csv_file:
        rec = dict(row)

        if excel_row >= 2:
            print("\n\n:::::::::excel_row:::::::::::::::", excel_row)
            address_type = False
            if rec['Address Type'].strip():
                if rec['Address Type'].strip() == 'Contact':
                    address_type = 'contact'
                elif rec['Address Type'].strip() == 'Invoice address':
                    address_type = 'invoice'
                elif rec['Address Type'].strip() == 'Other address':
                    address_type = 'other'
                elif rec['Address Type'].strip() == 'Private Address':
                    address_type = 'private'
                else:
                    address_type = 'delivery'

            if rec['Company Type'].strip() == 'Individual':
                company_type = 'person'
            else:
                company_type = 'company'

            if rec['State']:
                state_id = models.execute_kw(db, uid, password, 'ir.model.data', 'xmlid_to_res_model_res_id', [rec['State'].strip()])
                print(">>>state_id>>>", state_id)

            customer_industry = False
            if rec['Contact Type'].strip():
                if rec['Contact Type'].strip() == 'Architect':
                    customer_industry = 'architect'
                elif rec['Contact Type'].strip() == 'Maintenance Supervisor':
                    customer_industry = 'maintenance_supervisor'
                elif rec['Contact Type'].strip() == 'Owner or VIP':
                    customer_industry = 'owner_vip'
                elif rec['Contact Type'].strip() == 'Plant Manager/Engineer':
                    customer_industry = 'plant_manager_engineer'
                elif rec['Contact Type'].strip() == 'Project Manager':
                    customer_industry = 'project_manager'
                elif rec['Contact Type'].strip() == 'Purchasing/AP':
                    customer_industry = 'purchasing'
                elif rec['Contact Type'].strip() == 'Shipping/Receiving Contact':
                    customer_industry = 'shipping_receiving_contact'
                elif rec['Contact Type'].strip() == 'Superintendent':
                    customer_industry = 'superintendent'
                else:
                    customer_industry = 'sanitation_expert'

            if rec['Country']:
                country_id = models.execute_kw(
                    db, uid, password, 'ir.model.data', 'xmlid_to_res_model_res_id', [rec['Country'].strip()])
                print(">>>country_id>>>", country_id)

            customer_loc_id = False
            if rec['Customer Location']:
                customer_loc_id = models.execute_kw(
                    db, uid, password, 'ir.model.data', 'xmlid_to_res_model_res_id', [rec['Customer Location'].strip()])
                print(">>>customer_loc_id>>>", customer_loc_id)

            property_payment_term_id = False
            if rec['Customer Payment Terms']:
                property_payment_term_id = models.execute_kw(
                    db, uid, password, 'ir.model.data', 'xmlid_to_res_model_res_id', [rec['Customer Payment Terms'].strip()])
                print(">>>property_payment_term_id>>>", property_payment_term_id)
            
            customer_type = False
            if rec['Customer Type'].strip():
                if rec['Customer Type'].strip() == 'Architect':
                    customer_type = 'architect'
                elif rec['Customer Type'].strip() == 'Design/Build':
                    customer_type = 'design_build'
                elif rec['Customer Type'].strip() == 'Distributors':
                    customer_type = 'distributors'
                elif rec['Customer Type'].strip() == 'End User':
                    customer_type = 'end_user'
                elif rec['Customer Type'].strip() == 'General Contractor':
                    customer_type = 'general_contractor'
                else:
                    customer_type = 'panel_contractor'

            if rec['Invoice']:
                if rec['Invoice'].strip() == 'No Message':
                    invoice_warn = 'no-message'
                if rec['Invoice'].strip() == 'Warning':
                    invoice_warn = 'warning'
                else:
                    invoice_warn = 'block'

            if rec['Is a Customer']:
                customer_rank = 1
            else:
                customer_rank = 0

            if rec['Is a Vendor']:
                supplier_rank = 1
            else:
                supplier_rank = 0

            last_ack_date = False
            if rec['Last notification']:
                last_ack_date = str(datetime.strptime(rec['Last notification'].strip(), '%Y-%m-%d %H:%M:%S'))

            partner_tags_id = False
            if rec['Partner Tags']:
                partner_tags_id = models.execute_kw(
                    db, uid, password, 'ir.model.data', 'xmlid_to_res_model_res_id', [rec['Partner Tags']])
                print(">>>partner_tags_id>>>", partner_tags_id)

            if rec['Purchase Order']:
                if rec['Purchase Order'].strip() == 'No Message':
                    purchase_warn = 'no-message'
                if rec['Purchase Order'].strip() == 'Warning':
                    purchase_warn = 'warning'
                else:
                    purchase_warn = 'block'

            parent_id = False
            if rec['Related Company'].strip():
                parent_id = models.execute_kw(db, uid, password, 'res.partner', 'search', [[
                    ['external_id', '=', rec['Related Company'].strip()]]])
                print(":::::parent_id:::::", parent_id)

            responsible_id = False
            if rec['Responsible User']:
                responsible_id = models.execute_kw(
                    db, uid, password, 'ir.model.data', 'xmlid_to_res_model_res_id', [rec['Responsible User']])
                print(">>>responsible_id>>>", responsible_id)

            sale_team_id = False
            if rec['Sales Team']:
                sale_team_id = models.execute_kw(
                    db, uid, password, 'ir.model.data', 'xmlid_to_res_model_res_id', [rec['Sales Team']])
                print(">>>sale_team_id>>>", sale_team_id)

            saleperson_id = False
            if rec['Salesperson']:
                saleperson_id = models.execute_kw(
                    db, uid, password, 'ir.model.data', 'xmlid_to_res_model_res_id', [rec['Salesperson']])
                print(">>>saleperson_id>>>", saleperson_id)

            if rec['Sales Warnings']:
                if rec['Sales Warnings'].strip() == 'No Message':
                    sale_warn = 'no-message'
                if rec['Sales Warnings'].strip() == 'Warning':
                    sale_warn = 'warning'
                else:
                    sale_warn = 'block'

            vendor_contact_type = False
            if rec['Vendor Contact Type'].strip():
                if rec['Vendor Contact Type'].strip() == 'Accounts Receivable/Payable':
                    vendor_contact_type = 'accounts_receivable_payable'
                elif rec['Vendor Contact Type'].strip() == 'Drafting':
                    vendor_contact_type = 'drafting'
                elif rec['Vendor Contact Type'].strip() == 'Estimating':
                    vendor_contact_type = 'estimating'
                elif rec['Vendor Contact Type'].strip() == 'Plant Manager':
                    vendor_contact_type = 'plant_manager'
                elif rec['Vendor Contact Type'].strip() == 'President/CEO':
                    vendor_contact_type = 'president_ceo'
                elif rec['Vendor Contact Type'].strip() == 'Sales':
                    vendor_contact_type = 'sales'
                elif rec['Vendor Contact Type'].strip() == 'Sales Exec':
                    vendor_contact_type = 'sales_exec'
                else:
                    vendor_contact_type = 'shipping_receiving'

            property_stock_supplier = False
            if rec['Vendor Location']:
                property_stock_supplier = models.execute_kw(db, uid, password, 'ir.model.data', 'xmlid_to_res_model_res_id', [rec['Vendor Location']])
                print(">>>property_stock_supplier>>>", property_stock_supplier)

            property_supplier_payment_term_id = False
            if rec['Vendor Payment Terms']:
                property_supplier_payment_term_id = models.execute_kw(
                    db, uid, password, 'ir.model.data', 'xmlid_to_res_model_res_id', [rec['Vendor Payment Terms'].strip()])
                print(">>>property_supplier_payment_term_id>>>", property_supplier_payment_term_id)
                
            property_account_payable_id = False    
            if rec['Account Payable']:
                property_account_payable_id = models.execute_kw(
                    db, uid, password, 'ir.model.data', 'xmlid_to_res_model_res_id', [rec['Account Payable'].strip()])
                print(">>>property_account_payable_id>>>", property_account_payable_id)

            property_account_receivable_id = False
            if rec['Account Receivable']:
                property_account_receivable_id = models.execute_kw(
                    db, uid, password, 'ir.model.data', 'xmlid_to_res_model_res_id', [rec['Account Receivable'].strip()])
                print(">>>property_account_receivable_id>>>", property_account_receivable_id)

            vals = {
                'external_id': rec['ID'].strip(),
                'type': address_type, 
                'city': rec['City'].strip(),
                'company_type': company_type,
                'email': rec['Email'].strip(),
                'phone': rec['Phone'].strip(),
                'state_id': state_id and state_id[1],
                'name': rec['Name'].strip(),
                'account_number': rec['Account #'].strip(),
                'customer_industry': customer_industry,
                'country_id': country_id and country_id[1],
                'property_stock_customer': customer_loc_id and customer_loc_id[1],
                'property_payment_term_id': property_payment_term_id and property_payment_term_id[1],
                'customer_type': customer_type,
                'fax_number': rec['Fax #'].strip(),
                'gets_a_1099': rec['Gets a 1099'].strip(),
                'invoice_warn': invoice_warn,
                'is_customer': rec['Is a Customer'],
                'customer_rank': customer_rank,
                'is_supplier': rec['Is a Vendor'],
                'supplier_rank': supplier_rank,
                'function': rec['Job Position'].strip(),
                'calendar_last_notif_ack': last_ack_date,
                'linkedin': rec['LinkedIn'].strip(),
                'mobile': rec['Mobile'].strip(),
                'activity_summary': rec['Next Activity Summary'].strip(),
                'comment': rec['Notes'].strip(),
                'partner_tags': partner_tags_id and [(6,0, [partner_tags_id[1]])],
                'purchase_warn': purchase_warn,
                'parent_id': parent_id and parent_id[0],
                'activity_user_id': responsible_id and responsible_id[1],
                'team_id': sale_team_id and sale_team_id[1],
                'user_id': saleperson_id and saleperson_id[1],
                'sale_warn': sale_warn,
                'signup_token': rec['Signup Token'].strip(),
                'signup_type': rec['Signup Token Type'].strip(),
                'street': rec['Street'].strip(),
                'street2': rec['Street2'].strip(),
                'vat': rec['Tax ID'].strip(),
                'vendor_contact_type': vendor_contact_type,
                'property_stock_supplier': property_stock_supplier and property_stock_supplier[1],
                'property_supplier_payment_term_id': property_supplier_payment_term_id and property_supplier_payment_term_id[1],
                'website': rec['Website'].strip(),
                'zip': rec['Zip'].strip(),
                'property_account_payable_id': property_account_payable_id and property_account_payable_id[1],
                'property_account_receivable_id': property_account_receivable_id and property_account_receivable_id[1],
                'employee': False,
                'top_10': False,
                'top_25': False,
            }

            # try:
            partner_id = models.execute_kw(
                db, uid, password, 'res.partner', 'search', [[
                ['external_id', '=', rec['ID'].strip()]]])
            print("::::partner_id:::", partner_id)
            if partner_id:
                partner_id = models.execute_kw(db, uid, password, 'res.partner', 'write', [[partner_id[0]], vals])
            else:
                partner_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [vals])
            # except Exception as e:
            #     xls_row.append(excel_row)

        excel_row += 1
print(":::Exception::::xls_row:::::::::", xls_row)
