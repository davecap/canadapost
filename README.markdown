Canada Post Waybill Generator
=============================

API for generating Canada Post shipping labels.

## Requirements

To use this with EST Online you’ll need:

* a Canada Post customer number
* a Canada Post contract number (not required if you are a VentureOne customer)
* Your Canada Post username and password.

To sign up to VentureOne (it's free):

    http://www.canadapost.ca/cpo/mc/business/solutions/ventureone.jsf

To get login credentials:

    https://www.canadapost.ca/cpid/apps/signup?execution=e1s1

You need to add a credit card to the EST website as well as at least one shipping template.

## Create Waybill for Canada

First determine your parcel size (cm length/width/height) and weight (kg).

Waybill parameters are the following:

    shipper_name
    shipper_phone
    shipper_postal_code
    recipient_name
    recipient_title (optional)
    recipient_address_line1
    recipient_address_line2 (optional)
    recipient_city
    recipient_province (2 character)
    recipient_contact_phone (optional)
    recipient_contact_email (optional)
    parcel_weight
    parcel_length
    parcel_width
    parcel_height
    reference1 (optional)
    reference2 (optional)
    shipping_template
    payment_credit_card_alias=CREDIT_CARD_ALIAS,
    payment_credit_card_cvv=CREDIT_CARD_CVV,

## Example usage:

    import canadapost

    cpb = canadapost.CanadaPostBot()
    
    cpb.login(USERNAME, PASSWORD)

    pdf = cpb.generate_waybill('CA',
        shipper_name='David Caplan',
        shipper_phone='5143122520',
        shipper_postal_code='H3N1V5',
        recipient_name='David Caplan',
        recipient_address_line1='1321 Sherbrooke St. West',
        recipient_address_line2='#F31',
        recipient_city='Montreal',
        recipient_province='QC',
        recipient_postal_code='H3G1J4',
        # recipient_contact_email='dcaplan@gmail.com',
        parcel_weight='0.1',
        parcel_length='1.0',
        parcel_width='1.0',
        parcel_height='1.0',
        # parcel_is_document=True,
        shipping_template='Canada_Expedited.pard',
        payment_credit_card_alias=CREDIT_CARD_ALIAS,
        payment_credit_card_cvv=CREDIT_CARD_CVV,
    )

generate_waybill returns a PDF path which you can then open.

## TODO:

*tests*

Scheduled maintenance
We perform weekly maintenance from Saturday at 9 p.m. to Sunday at 7 a.m (EST). Please note that some features may not be available during these hours.

Form field requirements
if not document, parcel_* must be filled
If one dimension is provided all three dimensions must be entered
Replace length with the largest value entered for l, w, h
Replace width with the next largest
Replace height with the smallest value
Check Weight & Dimensions are numeric

Validate if Method of Payment is Credit Card then
Mailed By must be equal to Paid By customer

Check if customer is a Venture One if NOT then Contract is mandatory

look for errors in final pipeline response
form name = theForm
<input type="Hidden" name="errorMessage" value="(1731) Parcel does not meet the minimum acceptable size threshold.">

