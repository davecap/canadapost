# Test Canada
import canadapost
from credentials import USERNAME, PASSWORD, CREDIT_CARD_ALIAS, CREDIT_CARD_CVV


cpb = canadapost.CanadaPostBot()
cpb.login(USERNAME, PASSWORD)
cpb.generate_waybill('CA',
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


# Test USA
import canadapost
from credentials import USERNAME, PASSWORD, CREDIT_CARD_ALIAS, CREDIT_CARD_CVV

cpb = canadapost.CanadaPostBot()
cpb.login(USERNAME, PASSWORD)

test_items = [
    {
        'description': 'Handmade bow tie',
        'quantity': 2,
        'unit_price': '10.00',
    },
    {
        'description': 'Handmade necktie',
        'quantity': 1,
        'unit_price': '50.00',
    }
]

cpb.generate_waybill('US', skip_login=False,
    shipper_name='David Caplan',
    shipper_phone='5143122520',
    shipper_postal_code='H3N1V5',
    recipient_name='David F. Norman',
    recipient_address_line1='2669 Mercy Dr',
    recipient_address_line2='',
    recipient_city='Orlando',
    recipient_province='FL',
    recipient_postal_code='32808-3858',
    # recipient_contact_email='dcaplan@gmail.com',
    parcel_weight='0.1',
    parcel_length='1.0',
    parcel_width='1.0',
    parcel_height='1.0',
    # parcel_is_document=True,
# <option value="USA_Small_Packet_Air.paru">USA_Small_Packet_Air</option>
# <option value="USA_Expedited_Parcel.paru">USA_Expedited_Parcel</option>
    shipping_template='USA_Small_Packet_Air.paru',
    payment_credit_card_alias=CREDIT_CARD_ALIAS,
    payment_credit_card_cvv=CREDIT_CARD_CVV,
    items=test_items
)


# Test INTL
import canadapost
from credentials import USERNAME, PASSWORD, CREDIT_CARD_ALIAS, CREDIT_CARD_CVV

cpb = canadapost.CanadaPostBot()
cpb.login(USERNAME, PASSWORD)

test_items = [
    {
        'description': 'Handmade bow tie',
        'quantity': 2,
        'unit_price': '10.00',
    },
    {
        'description': 'Handmade necktie',
        'quantity': 1,
        'unit_price': '50.00',
    }
]

cpb.generate_waybill('DK', skip_login=False,
    shipper_name='David Caplan',
    shipper_phone='5143122520',
    shipper_postal_code='H3N1V5',
    recipient_name='Mads Christensen',
    recipient_address_line1=' Vestervoldgade 47',
    recipient_address_line2='1. tv',
    recipient_city='Nyborg',
    recipient_province='Fyn',
    recipient_postal_code='5800',
    recipient_country='DK',  # must be 2 letter code
    # recipient_contact_email='dcaplan@gmail.com',
    parcel_weight='0.1',
    parcel_length='21.0',  # min 21 cm
    parcel_width='14.0',  # min 14 cm
    parcel_height='1.0',  # min 1 mm
    # parcel_is_document=True,
#<option value="Intl_small_packet_air.pari">Intl_small_packet_air</option>
# <option value="USA_Small_Packet_Air.paru">USA_Small_Packet_Air</option>
# <option value="USA_Expedited_Parcel.paru">USA_Expedited_Parcel</option>
    shipping_template='Intl_small_packet_air.pari',
    payment_credit_card_alias=CREDIT_CARD_ALIAS,
    payment_credit_card_cvv=CREDIT_CARD_CVV,
    items=test_items
)
