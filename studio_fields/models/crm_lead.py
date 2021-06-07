from odoo import fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    customer_id = fields.Many2one('res.partner', string="Customer Name")
    contact_architect_id = fields.Many2one(
        'res.partner', string="Contact-Architect")
    bids_ids = fields.One2many('studio.bids', 'opportunity_id', string="Bids")
    project_timeline = fields.Char(string="Project Timeline")
    project_size = fields.Char(string="Project Size")
    architecture_firm = fields.Char(string="Architecture Firm")
    subs_bidding = fields.Char(string="Subs Bidding")
    reference = fields.Html(string="Lead Reference")
    contacted = fields.Boolean(string="Contacted")
    architect_educated = fields.Boolean(string="Architect Educated")
    specd_or_qualified = fields.Boolean(string="Spec'd or Qualified")
    documents_release_date = fields.Datetime(string="Documents Release Date")
    other_key_players = fields.Text(string="Other Key Players")
    qualified = fields.Boolean(string="Qualified")
    documents_received = fields.Boolean(string="Documents Received")
    bid_due_date = fields.Datetime(string="Bid Due Date")
    project_scope = fields.Text(string="Project Scope")
    all_bids_sent = fields.Boolean(string="All Bids Sent")
    expected_decision_by = fields.Datetime(string="Expected Decision By")
    follow_up_scheduled = fields.Boolean(string="follow_up_scheduled")
    follow_up_complete = fields.Boolean(string="Follow-up Complete")
    how_did_we_do = fields.Text(string="How did we do?")
    new_priority = fields.Selection(
      [("0", "None"), ("1", "Low"), ("2", "not to good"), ("3", "Average"),
      ("4", "High"), ("5", "Very High")], string="Priority")
    contact_id = fields.Many2one('res.partner', string="Contact")
    crm_ids = fields.Many2many('studio.crm', string="CRM")
    account_manager_id = fields.Many2one(
        'hr.employee', string="Account Executive")
    crsr_id = fields.Many2one('hr.employee', string="Estimator & CSR2")
    customer_project_estimated_completion_date = fields.Date(
        string="Customer Project Estimated Completion Date")
    hot_or_high_vis_project = fields.Boolean(string="HOT or HIGH VIS PROJECT")
    single_fg_personnel_doors = fields.Float(
        string="Single FG Personnel Doors")
    dbl_fg_personnel_doors = fields.Float(string="Dbl FG Personnel Doors")
    single_ss_personnel_doors = fields.Float(
        string="Single SS Personnel Doors")
    dbl_ss_personnel_doors = fields.Float(string="Dbl SS Personnel Doors")
    nchm_doors = fields.Float(string="NCHM Doors")
    fg_infits = fields.Float(string="FG Infits")
    hd_ss_infits = fields.Float(string="HD SS Infits")
    sd_ss_infit = fields.Float(string="SD SS Infit")
    wpg_infit = fields.Float(string="WPG Infit")
    heated_windows = fields.Float(string="Heated Windows")
    project_notes = fields.Text(string="Project Notes")
    insulated_windows = fields.Float(string="Insulated Windows")
    polycarbonate_windows = fields.Float(string="Polycarbonate Windows")
    polycarbonate_type = fields.Selection([("1/4\" AR2", "1/4\" AR2"), ("3/8\" AR2", "3/8\" AR2"),
                                           ("1/2\" AR2", "1/2\" AR2")], string="Polycarbonate Type")
    polycoating = fields.Selection([("NONE", "NONE"), ("1-Side_Coated", "1-Side Coated"),
                                    ("2-Sides_Coated", "2-Sides Coated")], string="POLYCOATING")
    fg_hsd = fields.Float(string="FG HSD")
    ss_hsd = fields.Float(string="SS HSD")
    wpg_hsd = fields.Float(string="WPG HSD")
    fg_vsd = fields.Float(string="FG VSD")
    ss_vsd = fields.Float(string="SS VSD")
    wpg_vsd = fields.Float(string="WPG VSD")
    lead_source = fields.Selection([("existing_client", "Existing Client"), ("google", "Google"),
                                    ("linkedIn", "LinkedIn"), (
                                        "news_article", "News Article"),
                                    ("ARCAT_BIM", "ARCAT-BIM"),
                                    ("general_contractor", "General Contractor"),
                                    ("architect", "Architect"), (
                                        "subcontractor", "Subcontractor"),
                                    ("client_referral", "Client Referral")], string="Lead Source")
    project_type = fields.Selection([("meat_processing", "Meat Processing"),
                                     ("cold_storage", "Cold Storage"),
                                     ("ready_to_eat", "Ready to Eat"), (
                                         "pharma", "Pharma"),
                                     ("waste_water", "Waste Water"), ("dairy", "Dairy")], string="Project Type")
    lead_reference2 = fields.Text(string="Lead Reference")
    fit_score = fields.Selection([("0", "New Customer-Bad Project"),
                                  ("1", "New Customer-Good Project"),
                                  ("2", "good Customer-bad project"),
                                  ("3", "Good Customer-Good Project")], string="Fit score")
    specified_door_mfg = fields.Selection([("weiland", "Weiland"), ("chemPruf", "ChemPruf"),
                                           ("jamison", "Jamison"), (
                                               "frank", "Frank"), ("chase", "Chase"),
                                           ("eSI", "ASI"), ("corrim", "Corrim"), (
                                               "tiger", "Tiger"),
                                           ("edgewater", "Edgewater"), (
                                               "specialite", "Specialite"),
                                           ("enviro", "Enviro")], string="Specified Door Mfg")
    specified_hardware_brand = fields.Selection([("dorma/BEST", "Dorma/BEST"),
                                                 ("vonDuprin/Schlage", "VonDuprin/Schlage")], string="Specified Hardware Brand")
    region = fields.Selection([("atlantic", "Atlantic"), ("midwest", "Midwest"),
                               ("pacific Plain", "Pacific Plain"), (
                                   "south Central", "South Central"),
                               ("house Accounts", "House Accounts"),
                               ("international", "International")], string="Region")
