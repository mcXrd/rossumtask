from app.annotation_wrapper import Annotation
from decimal import Decimal
import xmltodict


def _get_value_from_section(original_dict, section_schema_id, datapoint_schema_id):
    for section in original_dict["export"]["results"]["annotation"]["content"][
        "section"
    ]:
        if section["@schema_id"] == section_schema_id:
            for datapoint in section["datapoint"]:
                if datapoint["@schema_id"] == datapoint_schema_id:
                    return datapoint["#text"]


def transform_details(original_dict: dict) -> dict:

    line_items_section = None
    for section in original_dict["export"]["results"]["annotation"]["content"][
        "section"
    ]:
        if section["@schema_id"] == "line_items_section":
            line_items_section = section
            break

    raw_details = []
    for line_item in line_items_section["multivalue"]["tuple"]:
        assert line_item["@schema_id"] == "line_item"

        raw_detail = {}
        for datapoint in line_item["datapoint"]:
            if datapoint.get("#text"):
                raw_detail[datapoint["@schema_id"]] = datapoint["#text"]
        raw_details.append(raw_detail)

    details = []
    for raw_detail in raw_details:
        detail = {
            "Amount": raw_detail["item_amount_total"],
            "AccountId": None,
            "Quantity": raw_detail["item_quantity"],
            "Notes": raw_detail["item_description"],
        }
        details.append(detail)
    return {"Detail": details}


def transform_annotation(original_annotation: Annotation) -> Annotation:
    original_dict = original_annotation.dict_repr
    details = transform_details(original_dict)
    amount = _get_value_from_section(original_dict, "amounts_section", "amount_total")
    tax = _get_value_from_section(original_dict, "amounts_section", "amount_total_tax")
    total_amount = str(Decimal(amount) + Decimal(tax))
    payable = {
        "InvoiceNumber": _get_value_from_section(
            original_dict, "invoice_info_section", "invoice_id"
        ),
        "InvoiceDate": _get_value_from_section(
            original_dict, "invoice_info_section", "date_issue"
        )
        + "T00:00:00",
        "DueDate": _get_value_from_section(
            original_dict, "invoice_info_section", "date_due"
        )
        + "T00:00:00",
        "TotalAmount": total_amount,
        "Notes": None,
        "Iban": _get_value_from_section(original_dict, "invoice_info_section", "iban"),
        "Amount": amount,
        "Currency": _get_value_from_section(
            original_dict, "amounts_section", "currency"
        ).upper(),
        "Vendor": _get_value_from_section(
            original_dict, "vendor_section", "sender_name"
        ),
        "VendorAddress": _get_value_from_section(
            original_dict, "vendor_section", "sender_address"
        ),
        "Details": details,
    }
    result = {"InvoiceRegisters": {"Invoices": {"Payable": payable}}}
    transformed_annotation = Annotation(raw_str=xmltodict.unparse(result))
    return transformed_annotation
