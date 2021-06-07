# url = 'https://jdcdev-weiland-doors-studio-customization-0321-2230310.dev.odoo.com'
# db = 'jdcdev-weiland-doors-studio-customization-0321-2230310'
# username = 'admin'
# password = 'admin'

url = 'http://127.0.0.1:8069'
db = 'v13e_weliand_studio_12_march_test'
username = 'admin'
password = 'admin'

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

with open('/home/odoo/Desktop/fatemi/workspace/projects/v13/weiland/weiland-doors/scripts/account_payment_term_line.csv', newline='') as csv_file:

    csv_file = csv.DictReader(csv_file)
    xls_row = []
    excel_row = 2
    
    for row in csv_file:
        rec = dict(row)

        if excel_row >= 2:
            print("\n\n:::::::::excel_row:::::::::::::::", excel_row)

            if rec['id']:
                try:
                    payment_term_line_id = models.execute_kw(
                        db, uid, password, 'ir.model.data', 'xmlid_to_res_model_res_id', [rec['id'].strip()])
                    print(">>>payment_term_line_id>>>", payment_term_line_id)
                    payment_term_line_id = payment_term_line_id[1]

                    if not payment_term_line_id:
                        option = False
                        if rec['option'].strip():
                            if rec['option'].strip() == 'day(s) after the invoice date':
                                option = 'day_after_invoice_date'
                            elif rec['option'].strip() == 'of the following month':
                                option = 'day_following_month'
                            elif rec['option'].strip() == 'of the current month':
                                option = 'day_current_month'
                            else:
                                option = 'after_invoice_month'

                        if rec['value'].strip():
                            if rec['value'].strip() == 'Balance':
                                value = 'balance'
                            elif rec['value'].strip() == 'Percent':
                                value = 'percent'
                            else:
                                value = 'fixed'

                        payment_term_id = models.execute_kw(
                            db, uid, password, 'account.payment.term', 'search', [[
                            ['external_id', '=', rec['payment_id'].strip()]]])
                        print("::::payment_term_id:::", payment_term_id)

                        if payment_term_id:
                            vals = {
                                'day_of_the_month': int(rec['day_of_the_month'].strip()),
                                'days': int(rec['days'].strip()),
                                'option': option,
                                'sequence': int(rec['sequence'].strip()),
                                'value': value,
                                'value_amount': float(rec['value_amount'].strip()),
                                'payment_id': payment_term_id and payment_term_id[0]
                            }

                            payment_term_line_id = models.execute_kw(db, uid, password, 
                                'account.payment.term.line', 'create', [vals])
                except Exception as e:
                    xls_row.append(excel_row)

        excel_row += 1
print(":::Exception::::xls_row:::::::::", xls_row)
