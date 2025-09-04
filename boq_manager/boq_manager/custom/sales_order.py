import frappe

def copy_boq_reference(doc, method):
    if doc.custom_boq_reference:
        quotation_doc = frappe.get_doc("Quotation", {"custom_boq_reference_link": doc.custom_boq_reference})
        if hasattr(quotation_doc, 'custom_boq_reference_link') and quotation_doc.custom_boq_reference_link:
            doc.custom_boq_reference = quotation_doc.custom_boq_reference_link
            doc.save()