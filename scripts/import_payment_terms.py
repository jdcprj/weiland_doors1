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

with open('/home/odoo/Desktop/fatemi/workspace/projects/v13/weiland/weiland-doors/scripts/account_payment_term.csv', newline='') as csv_file:

    csv_file = csv.DictReader(csv_file)
    xls_row = []
    excel_row = 2
    
    for row in csv_file:
        rec = dict(row)

        if excel_row >= 2:
            print("\n\n:::::::::excel_row:::::::::::::::", excel_row)

            if rec['id']:
                try:
                    payment_term_id = models.execute_kw(
                        db, uid, password, 'ir.model.data', 'xmlid_to_res_model_res_id', [rec['id'].strip()])
                    print(">>>payment_term_id>>>", payment_term_id)
                    existing_payment_term_id = payment_term_id[1]
                    if existing_payment_term_id:
                        vals = {
                            'name': rec['name'],
                            'external_id': rec['id'].strip()
                        }
                        models.execute_kw(db, uid, password, 'account.payment.term', 'write', [[existing_payment_term_id], vals])
                        print(">write>>>payment_term_id>>>", payment_term_id)

                    if not existing_payment_term_id:
                        payment_term_id = models.execute_kw(
                            db, uid, password, 'account.payment.term', 'search', [[
                            ['external_id', '=', rec['id'].strip()]]])
                        print("::::payment_term_id:::", payment_term_id)
                        if not payment_term_id:
                            vals = {
                                'name': rec['name'].strip(),
                                'external_id': rec['id'].strip(),
                                'sequence': int(rec['sequence'].strip()),
                                'note': rec['note'].strip(),
                                'line_ids': False
                            }

                            payment_term_id = models.execute_kw(db, uid, password, 
                                'account.payment.term', 'create', [vals])
                except Exception as e:
                    xls_row.append(excel_row)

        excel_row += 1
print(":::Exception::::xls_row:::::::::", xls_row)
