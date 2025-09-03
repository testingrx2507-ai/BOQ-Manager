import frappe

def copy_boq_reference(doc, method):
    if doc.quotation_reference:
        quotation_doc = frappe.get_doc("Quotation", doc.quotation_reference)
        if hasattr(quotation_doc, 'boq_reference') and quotation_doc.boq_reference:
            doc.boq_reference = quotation_doc.boq_reference
            doc.save()