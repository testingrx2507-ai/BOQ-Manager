# Copyright (c) 2025, Som and contributors
# For license information, please see license.txt

# import frappe

import frappe
from frappe.model.document import Document

class BillofQuantities(Document):
    def validate(self):
        self.calculate_total_amount()
    
    def on_submit(self):
        self.status = 'Submitted'
    
    def calculate_total_amount(self):
        total = 0
        for item in self.get("boq_items"):
            total += item.quantity * item.rate
        
        self.total_amount = total
    
@frappe.whitelist()
def create_quotation_from_boq(boq_name):
    boq_doc = frappe.get_doc("Bill of Quantities", boq_name)
    
    if boq_doc.status != 'Submitted':
        frappe.throw("BOQ must be in 'Submitted' status to create quotation")

    quotation = frappe.new_doc("Quotation")
    quotation.customer = boq_doc.customer
    quotation.quotation_to = "Customer"
    quotation.boq_reference = boq_name

    for boq_item in boq_doc.boq_items:
        quotation.append("items", {
            "item_code": boq_item.item_code,
            "item_name": boq_item.item_name,
            "description": boq_item.description,
            "qty": boq_item.quantity,
            "rate": boq_item.rate,
            "uom": boq_item.uom
        })
    
    quotation.insert()

    boq_doc.status = 'Quoted'
    boq_doc.save()
    
    return quotation.name

@frappe.whitelist()
def create_project_from_boq(boq_name):
    boq_doc = frappe.get_doc("Bill of Quantities", boq_name)
    sales_orders = frappe.get_all("Sales Order", 
                                 filters={"boq_reference": boq_name, "docstatus": 1})
    
    if not sales_orders:
        frappe.throw("No submitted Sales Order found linked to this BOQ")
    
    existing_project = frappe.get_all("Project", filters={"boq_reference": boq_name})
    if existing_project:
        frappe.throw("Project already exists for this BOQ")
    
    project = frappe.new_doc("Project")
    project.project_name = boq_doc.title
    project.customer = boq_doc.customer
    project.boq_reference = boq_name
    project.insert()
    
    for boq_item in boq_doc.boq_items:
        task = frappe.new_doc("Task")
        task.subject = boq_item.item_name
        task.project = project.name
        task.boq_quantity_needed = boq_item.quantity
        task.insert()
    
    return project.name