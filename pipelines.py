
from decimal import Decimal


def field_to_upper(value):
    return value.upper()


def field_float(value):
    if type(value) == Decimal:
        return str(value)
    else:
        return str(float(value))


def field_currency(value):
    if type(value) == Decimal:
        return str(value)
    else:
        return str(float(value))


def field_integer(value):
    if type(value) == Decimal:
        return str(value.quantize(0))
    else:
        return str(int(value))


def field_postal_code(value):
    # postal code:
    #  ANA NAN
    #  ANANAN
    #  MUST HAVE A SPACE and exactly 6 characters
    # format postal code
    if len(value) == 6:
        value = '%s %s' % (value[:3], value[3:])
    return field_to_upper(value)


def field_zip_code(value):
    # zip code
    # 99999, 99999-9999, or 999999999
    #     var zipCodeTest = /\d\d\d\d\d/;
    #     var zipCodePattern2 = /\d\d\d\d\d-\d\d\d\d/;
    #     var zipCodePattern3 = /\d\d\d\d\d\d\d\d\d/;
    return value


def field_telephone(value):
    #Valid Telephone Number. Can only contain numbers and -
    return value


def field_no_asterisk(value):
    return value.replace('*', '')


### Shared Form Fields

# Shipping form fields (step 1)

SHIP_FORM_FIELDS = [
    ### Shipper Info
    # <input type="text" name="contactName" style="width: 160px;" size="35" maxlength="35" value="NAME">
    {
        'type': 'text',
        'name': 'contactName',
        'data_key': 'shipper_name',
        'required': False,
        'max_length': 35
    },
    # <input type="text" name="shipperPhone" style="width: 160px;" size="22" maxlength="22" value="PHONE NUMBER"
    {
        'type': 'text',
        'name': 'shipperPhone',
        'data_key': 'shipper_phone',
        'required': False,
        'max_length': 22
    },
    # <select name="preferredMethodOfPayment" style="width: 160px; font-size: 10pt;">
    #   <option value=""></option>
    #   <option value="CREDIT" SELECTED>Credit Card</option>
    # </select>
    {
        'type': 'select',
        'name': 'preferredMethodOfPayment',
        'default': ['CREDIT'],  # default, used credit card
        'required': True
    },
    # <input name="shippingPointPC" style="width: 55px;" size="7" maxlength="7" value="POSTAL CODE"
    {
        'type': 'text',
        'name': 'shippingPointPC',
        'data_key': 'shipper_postal_code',
        'required': True,
        'filters': [field_postal_code],
        'max_length': 7
    },
    #
    ### Recipient data:
    # Name: <input type="text" style="width: 215px;" name="name" size="44" maxlength="44" value="" onchange="return isValidChars(this, 323, null, null)" >
    {
        'type': 'text',
        'name': 'name',
        'data_key': 'recipient_name',
        'required': True,
        'max_length': 44
    },
    # Title/Dept: <input type="text" name="title" style="width: 215px;" size="44" maxlength="44" value="" onchange="return isValidChars(this, 323, null, null)">
    {
        'type': 'text',
        'name': 'title',
        'data_key': 'recipient_title',
        'required': False,
        'max_length': 44
    },
    # Address line 1: <input type="text" name="addressLine1" size="44" maxlength="44"  style="width: 215px;" value="" onchange="return isValidChars(this, 323, null, null)">
    {
        'type': 'text',
        'name': 'addressLine1',
        'data_key': 'recipient_address_line1',
        'required': True,
        'max_length': 44
    },
    # Address line 2: <input type="text" name="addressLine2" size="44" maxlength="44" style="width: 215px;" value="" onchange="return isValidChars(this, 323, null, null)">
    {
        'type': 'text',
        'name': 'addressLine2',
        'data_key': 'recipient_address_line2',
        'required': False,
        'max_length': 44
    },
    # City: <input type="text" name="city" size="20" maxlength="35" style="width: 215px;" value="" onchange="return isValidChars(this, 323, null, null)">
    {
        'type': 'text',
        'name': 'city',
        'data_key': 'recipient_city',
        'required': True,
        'max_length': 35
    },
    ### Optional fields:
    # Contact phone: <input type="text" name="contactPhone" size="25" maxlength="25" style="width: 215px;"
    {
        'type': 'text',
        'name': 'contactPhone',
        'data_key': 'recipient_contact_phone',
        'required': False,
        'max_length': 25
    },
    # Contact email: <input type="text" name="recipientEmail" size="25" maxlength="60" style="width: 215px;"
    {
        'type': 'text',
        'name': 'recipientEmail',  # 'contactEmail', ???
        'data_key': 'recipient_contact_email',
        'required': False,
        'max_length': 60
    },
    ### Parcel data:
    # Weight: <input type="text" name="weight" size="6" maxlength="7"
    {
        'type': 'text',
        'name': 'weight',
        'data_key': 'parcel_weight',
        'required': True,  # always required
        'filters': [field_float],
        'max_length': 7
    },
    # Length: <input type="text" name="parcelLength" size="6" maxlength="7"
    {
        'type': 'text',
        'name': 'parcelLength',
        'data_key': 'parcel_length',
        'required': False,  # required only if not is_document
        'filters': [field_float],
        'max_length': 7
    },
    # Width: <input type="text" name="parcelWidth" size="6" maxlength="7"
    {
        'type': 'text',
        'name': 'parcelWidth',
        'data_key': 'parcel_width',
        'required': False,  # required only if not is_document
        'filters': [field_float],
        'max_length': 7
    },
    # Height: <input type="text" name="parcelHeight" size="6" maxlength="7"
    {
        'type': 'text',
        'name': 'parcelHeight',
        'data_key': 'parcel_height',
        'required': False,  # required only if not is_document
        'filters': [field_float],
        'max_length': 7
    },
    # isDocument, SET FALSE: <input type="Checkbox" name="isDocument" value="true"
    {
        'type': 'checkbox',
        'name': 'isDocument',
        'data_key': 'parcel_is_document',
        'default': False
    },
    ### Shipping info:
    # reference 1: <input name="referenceNumber" size="12" maxlength="12" value=""
    {
        'type': 'text',
        'name': 'referenceNumber',
        'data_key': 'reference1',
        'required': False,
        'max_length': 12
    },
    # reference 2: <input name="referenceNumber2" size="30" maxlength="30" value=""
    {
        'type': 'text',
        'name': 'referenceNumber2',
        'data_key': 'reference2',
        'required': False,
        'max_length': 30
    },
    # Template: <select name="selectedTemplate" style="width: 214px; font-size: 10pt;">
    #   <option value="" SELECTED></option>
    # <option value="USA_Small_Packet_Air.paru">USA_Small_Packet_Air</option>
    # <option value="USA_Expedited_Parcel.paru">USA_Expedited_Parcel</option>
    {
        'type': 'select',
        'name': 'selectedTemplate',
        'data_key': 'shipping_template',
        'required': True
    },
]

# Payment form fields

PAYMENT_FORM_FIELDS = [
    ### Payment Info
    # <select name="creditCardAlias" style="width: 140px; font-size: 10pt;">
    #   <option value="" SELECTED></option>
    #   <option value="NNNN********NNNN">NNNN********NNNN</option>
    {
        'type': 'select',
        'name': 'creditCardAlias',
        'data_key': 'payment_credit_card_alias',
        'required': False
    },
    ### Manual credit card number entry
    # <select name="creditCardType" style="width: 161px; font-size: 10pt;">
    #   <option value="" SELECTED></option>
    #   <option value="AME1">American Express</option>
    #   <option value="MC1">Master Card</option>
    #   <option value="VIS1">Visa Card</option>
    # </select>
    # <input type="text" name="creditCardNumber" style="width: 160px;" size="16" maxlength="16" value=""
    # <input type="text" name="creditCardExpiryDate" style="width: 80px;" size="5" maxlength="5"
    # <input type="text" name="creditCardOwner" style="width: 160px;" size="40" maxlength="40"
    # <input type="text" name="creditCardCVV" style="width: 75px;" size="4" maxlength="4
    {
        'type': 'text',
        'name': 'creditCardCVV',
        'data_key': 'payment_credit_card_cvv',
        'required': True,
        'max_length': 4
    },
]

# USA & Intl Customs Info fields

CUSTOMS_INFO_FIELDS = [
    ### Customs Info
    # <input type="Text" name="customsCurrency" size="10" maxlength="10" value="CAD" onchange=" return noAsterisk(theForm.customsCurrency, 3, null, null);" onfocus="javascript: document.theForm.customsCurrency.value = document.theForm.customsCurrency.value.toUpperCase()";>
    {
        'type': 'text',
        'name': 'customsCurrency',
        # 'data_key': 'customs_currency',
        'default': 'CAD',
        'required': True,
    },
    ##
    # <select name="reasonForExport" style="width: 200px; font-size: 10pt;" onchange="return testForOtherCustomsExportReason()">
    #     <option value="SAM">Commercial Sample</option>
    #     <option value="GIF">Gift</option>
    #     <option value="REP">Repair/Warranty</option>
    #     <option value="DOC">Document</option>
    #     <option value="SOG">Sale of Goods</option>
    #     <option value="OTH">Other</option>
    # </select>
    {
        'type': 'select',
        'name': 'reasonForExport',
        'data_key': 'reason_for_export',
        'required': False,
        'default': ['SOG']
        # value can be ['GIF'] for gifts
    },
    ##
    # <select name="nonDeliveryInstructions" style="width: 200px; font-size: 10pt;">
    #   <option value="RTS">Return to Sender</option>
    # </select>
    {
        'type': 'select',
        'name': 'nonDeliveryInstructions',
        'data_key': 'non_delivery_instructions',
        'required': False,
        'default': ['RTS']
    }
]

# Customs template
# each line should have:
#   {
#       'description': 'handmade bow tie',
#       'quantity': '1',
#       'unit_price': '10.00',
#   }
CUSTOMS_LINE_FIELDS = {
    # Item/Part/SKU
    # <input type="Text" name="vendorPartNumber<INDEX>" size="48" maxlength="48"
    'sku': {
        'name': 'vendorPartNumber%d',
        'type': 'text',
        'max_length': 48,
        'required': False
    },
    # Quantity*
    # <input type="Text" name="quantity<INDEX>" size="4" maxlength="4" value="" onchange="return isIntInRange(theForm.quantity1, 0, 9999, 161, null, null)">
    'quantity': {
        'name': 'quantity%d',
        'type': 'text',
        'filters': [field_integer],
        'required': True
    },
    # Description*
    # <input type="Text" name="description<INDEX>" size="25" maxlength="25" value="" onchange=" return noAsterisk(theForm.description1, 3, null, null)">
    'description': {
        'name': 'description%d',
        'type': 'text',
        'max_length': 25,
        'filters': [field_no_asterisk],
        'required': True
    },
    # Unit value*
    # <input type="Text" name="value<INDEX>" size="8" maxlength="8" value="" onchange="return isFloatInRange(theForm.value1, 0.01, 99999.99, 2, 70, null, null)">
    'unit_price': {
        'name': 'value%d',
        'type': 'text',
        'max_length': 8,
        'filters': [field_currency],
        'required': True,
        'min_value': 0.01,
        'max_value': 99999.99,
        'decimal_places': 2
    },
    # Unit weight
    # <input type="Text" name="netWeight<INDEX>" size="6" maxlength="6" value="" onchange="return isFloatInRange2(theForm.netWeight1, 0, 999999.999, 3, 68, null, null, 6)">
    'unit_weight': {
        'name': 'netWeight%d',
        'type': 'text',
        'max_length': 6,
        'filters': [field_float],
        'required': False,
        'min_value': 0.01,
        'max_value': 999999.999,
        'decimal_places': 3
    },
    # Country of origin: CA
    # <select name="country<INDEX>" style="width: 120px; font-size: 10pt;" onchange="setProvForCanada(this, document.theForm.province1)">
    #   value: CA
    'country': {
        'name': 'country%d',
        'type': 'select',
        'required': False,
        'default': ['CA']  # always Canada
    },
}

### Pipelines

# Canada Post EST SSO login pipeline

EST_SSO_PIPELINE = [
    {
        'open_url': 'https://www.canadapost.ca/cpid/apps/signIn',
        'title': 'Canada Post - My Business Profile Sign In',
        'redirect': None,
        'form': {
            'name': 'cpidSignIn',
            'action': "/cpid/apps/signIn?execution=e1s1",
            # 'assert': {
            #             '#cpidSignIn:j_username': {},
            #             '#cpidSignIn:j_password': {},
            #             'select[name="destination"]': {
            #                 'value': 'https://obc.canadapost.ca/zcpb2b/b2b/init.do'
            #             },
            #             '#cpidSignIn:signIn': {},
            #             'input[type="hidden",name="cpidSignIn:signIn"]': {},
            #             'input[type="hidden",name="javax.faces.ViewState"]': {},
            #             'cpidSignIn_SUBMIT': {},
            # },
            'fields': [
                {'type': 'text',
                    'name': 'cpidSignIn:j_username',
                    'data_key': 'username',
                    'required': True,
                },
                {'type': 'text',
                    'name': 'cpidSignIn:j_password',
                    'data_key': 'password',
                    'required': True,
                },
            ]
        }
    },
    {
        'assert_url': 'https://www.canadapost.ca/cpid/login.jsp',
        'title': '',
        'redirect': None,
        'form': {
            'name': 'Login',
            'action': '/cpid/login/redirect',
            'assert_fields': {},
                # <input type="hidden" name="SHOP" value = "CPFRCOMM">
                # <input type="hidden" name="SSO_ITS_URL" value="/cpid/login.jsp">
                # <input type="hidden" name="SSO_ACTION" value="0">
                # <input type="hidden" name="P_SHOP" value = "CPFRCOMM">
                # <input type="hidden" name="login_type" value = "2">
                # <input type="hidden" name="password_length" value = "0">
                # <input type="hidden" name="~language" value="EN">
                # <input type="hidden" name="APP_ID" value="B2B">
                # <input type="hidden" name="SSO_USERID" value="USERNAME">
                # <input type="hidden" name="SSO_PASSWORD" value="null">
                # <input type="hidden" name="EXT_REF_URL" value="null">
        }
    },
    {
        'assert_url': 'https://www.canadapost.ca/cpid/login/redirect',
        'title': '',
        'redirect': None,
        'form': {
            'name': 'Login',
            'action': '/cpid/login.jsp',
            'assert': {},
                # <input type=hidden name="APP_ID" value="B2B">
                # <input type=hidden name="shop" value="CPENCOMM">
                # <input type=hidden name="SSO_CUSTOMER_NUMBER" value="********,">
                # <input type=hidden name="SSO_VERSION_MAJOR" value="3">
                # <input type=hidden name="SSO_VERSION_MINOR" value="0">
                # <input type=hidden name="SSO_VERSION_MICRO" value="0">
                # <input type=hidden name="SSO_VERSION" value="3.0.0">
                # <input type=hidden name="SSO_USER_ROLE" value="ZC.CRM_BDT_CMPLTE,ZC.CRM_OBC_SBOEXP">
                # <input type=hidden name="SSO_PASSWORD" value="76636669722b722e122e011f03396664">
                # <input type="hidden" name="APP_ID" value="B2B">
        }
    },
    {
        'assert_url': 'https://www.canadapost.ca/cpid/login.jsp',
        'title': '',
        'redirect': None,
        'form': {
            'name': 'goNext',
            'action': 'https://obc.canadapost.ca/zcpb2b/b2b/init.do',
            'assert': {},
                # <input type=hidden name="SSO_VERSION_MICRO" value="0">
                # <input type=hidden name="SSO_VERSION_MINOR" value="0">
                # <input type=hidden name="APP_ID" value="B2B">
                # <input type=hidden name="shop" value="CPENCOMM">
                # <input type=hidden name="SSO_VERSION_MAJOR" value="3">
                # <input type=hidden name="SSO_VERSION" value="3.0.0">
                # <input type="hidden" name="SSO_USERID" value="USERNAME">
                # <input type="hidden" name="SSO_CUSTOMER_NUMBER" value="*******,">
                # <input type="hidden" name="~language"  value="EN">
                # <input type="hidden" name="SSO_SECURITY_TOKEN" value="">
                # <input type="hidden" name="SSO_PASSWORD"  value="76636669722b722e122e011f03396664">
                # <input type="Hidden" name="SSO_USER_ROLE" value="ZC.CRM_BDT_CMPLTE,ZC.CRM_OBC_SBOEXP">
        }
    },
    {
        'assert_url': 'https://obc.canadapost.ca/zcpb2b/b2b/init.do',
        'title': '',
        'redirect': None,
        'form': {
            'name': 'login_form',
            #'https://obc.canadapost.ca/zcpb2b/b2b/login.do',
            'action': '/zcpb2b/b2b/login.do',
            'assert': {},
                # <input type="hidden" name="REQUEST_ID" value="(J2EE319200500)ID2075576650DB4a7a8a535a085cfbbcfd4b2742cef8147aa60eb8End">
                # <script type="text/javascript">
                #   // determine the browser version
                #   document.write('<input type="hidden" name="browsername" value="' +  escape(navigator.userAgent.toLowerCase()) + '">');
                #   document.write('<input type="hidden" name="browsermajor" value="' + escape(parseInt(navigator.appVersion)) + '">');
                #   document.write('<input type="hidden" name="browserminor" value="' + escape(parseFloat(navigator.appVersion)) + '">');
                # </script>
                # <input class="submitDoc" type="hidden" name="isSSO" value="true">
                # <input class="submitDoc" type="hidden" name="UserId" value="USERNAME">
                # <input class="submitDoc" type="hidden" name="nolog_password" value="PASSWORD">
                # <input class="submitDoc" type="hidden" name="nolog_password" value="PASSWORD">
                # <input class="submitDoc" type="hidden" name="deepLink" value="">
        }
    },
    {
        'assert_url': 'https://obc.canadapost.ca/zcpb2b/b2b/login.do',
        'title': '',
        'form': None,
        'redirect': 'https://obc.canadapost.ca/zcpb2b/b2b/zisa_start_choice.do'
    },
    {
        'assert_url': 'https://obc.canadapost.ca/zcpb2b/b2b/zisa_start_choice.do',
        'title': '',
        'form': {
            'name': 'formChoice',
            'action': '/zcpb2b/b2b/zisa_choice.do',
            'assert': {},
                # <form method="post" action='/zcpb2b/b2b/zisa_choice.do' name="formChoice" >
                # <input type="hidden" name="REQUEST_ID" value="*********">
                # <input type="hidden" name="targetPage" value="">
                # <input type="hidden" name="errPage" value="">
                # </form>
        }
    }
]

# Canada Shipping

EST_SHIP_CANADA_PIPELINE = [
    {
        'open_url': 'https://obc.canadapost.ca/zcpb2b/b2b/zisa_estForward.do?forwardTo=shipCanada',
        'title': '',
        'redirect': 'https://est-oee.canadapost-postescanada.ca/shipping/estShipping.jsp?locale=en_CA&formId=110&isV1=true',
        # FUTURE: parse redirect from document.location="https://est-oee.canadapost-postescanada.ca/shipping/estShipping.jsp?locale=en_CA&formId=110&isV1=true";
        'form': {}
    },
    {
        'assert_url': 'https://www.canadapost.ca/cpid/login.jsp',
        'title': '',
        'redirect': None,
        'form': {
            'name': 'goNext',
            'action': 'https://est-oee.canadapost-postescanada.ca/shipping/estShipping.jsp?formId=110&locale=en_CA&isV1=true',
            'assert': {},
                #  <form name="goNext" action="https://est-oee.canadapost-postescanada.ca//shipping/estShipping.jsp?formId=110&locale=en_CA&isV1=true" method="POST">
                #  <input type="hidden" name="SSO_USERID" value="********">
                #  <input type="hidden" name="SSO_CUSTOMER_NUMBER" value="********,">
                # <input type="hidden" name="~language"    value="EN">
                #  <input type="hidden" name="SSO_SECURITY_TOKEN" value="">
                #  <input type="hidden" name="SSO_PASSWORD"    value="*********">
                # </form>
        }
    },
    {
        'assert_url': 'https://www.canadapost.ca/cpid/login.jsp',
        'title': '',
        'redirect': None,
        'form': {
            'name': 'goNext',
            'action': 'https://est-oee.canadapost-postescanada.ca/shipping/estShipping.jsp',
            'assert': {},
                # <form name="goNext" action="https://est-oee.canadapost-postescanada.ca//shipping/estShipping.jsp?locale=en_CA&formId=110&SSO_SECURITY_TOKEN=&isV1=true&~language=EN&SSO_USERID=&SSO_PASSWORD=&SSO_CUSTOMER_NUMBER=," method="POST">
                # <input type="hidden" name="SSO_USERID" value="********">
                # <input type="hidden" name="SSO_CUSTOMER_NUMBER" value="*********,">
                # <input type="hidden" name="~language"    value="EN">
                # <input type="hidden" name="SSO_SECURITY_TOKEN" value="">
                # <input type="hidden" name="SSO_PASSWORD"    value="*********">
                # </form>
        }
    },
    {
        'open_url': 'https://obc.canadapost.ca/zcpb2b/b2b/zisa_estForward.do?forwardTo=shipCanada',
        'title': '',
        'redirect': 'https://est-oee.canadapost-postescanada.ca/shipping/estShipping.jsp?locale=en_CA&formId=110&isV1=true',
        'form': {}
    },
    {
        'assert_url': 'https://est-oee.canadapost-postescanada.ca/shipping/estShipping.jsp',
        'redirect': None,
        'form': {
            'name': 'theForm',
            'action': 'https://est-oee.canadapost-postescanada.ca/ShippingServlet',
            'assert': {},
            'fields': SHIP_FORM_FIELDS + [
                # Province: <select name="province" style="width: 214px; font-size: 10pt;">
                #     <option value="" SELECTED></option>
                #     <option value="AB">Alberta</option>
                #     <option value="BC">British Columbia</option>
                #     <option value="MB">Manitoba</option>
                #     <option value="NT">NW Territories</option>
                #     <option value="NB">New Brunswick</option>
                #     <option value="NL">Newfoundland & Labr.</option>
                #     <option value="NS">Nova Scotia</option>
                #     <option value="NU">Nunavut</option>
                #     <option value="ON">Ontario</option>
                #     <option value="PE">Prince Edward Island</option>
                #     <option value="QC">Quebec</option>
                #     <option value="SK">Saskatchewan</option>
                #     <option value="YT">Yukon Territory</option>
                {
                    'type': 'select',
                    'name': 'province',
                    'data_key': 'recipient_province',
                    'required': True
                },
                # Postal Code: <input type="text" name="postalCode" style="width: 215px;" maxlength="7" value=""
                {
                    'type': 'text',
                    'name': 'postalCode',
                    'data_key': 'recipient_postal_code',
                    'required': True,
                    'filters': [field_postal_code],
                    'max_length': 7
                },
                ### Misc CP fields:
                # assert nextPageFormId value = 111
                {
                    'type': 'hidden',
                    'name': 'nextPageFormId',
                    'default': '111'
                }
            ]
        }
    },
    {
        'assert_url': 'https://est-oee.canadapost-postescanada.ca/shipping/estShipping.jsp?locale=en_CA&formId=114',
        'redirect': None,
        'form': {
            'name': 'theForm',
            'action': 'https://est-oee.canadapost-postescanada.ca/ParcelMailTransmitServlet',
            'assert': {},
            'fields': PAYMENT_FORM_FIELDS
        }
    },
    {
        'assert_url': 'https://est-oee.canadapost-postescanada.ca/shipping/parcelMailViewLabelFrameset.jsp?label=forward&locale=en_CA',
        'redirect': 'https://est-oee.canadapost-postescanada.ca/shipping/../waitingForPDF.jsp?servletName=ParcelMailViewLabelServlet&label=forward&locale=en_CA&language=en_CA',
        'form': {}
    },
    {
         # Send request to generate Preview PDF\ndocument.location.replace("ParcelMailViewLabelServlet?useraction=null&label=forward");
        'download': 'https://est-oee.canadapost-postescanada.ca/shipping/../ParcelMailViewLabelServlet?useraction=null&label=forward',
        'form': {}
    }
]

# USA Shipping

EST_SHIP_USA_PIPELINE = [
    {
        'open_url': 'https://obc.canadapost.ca/zcpb2b/b2b/zisa_estForward.do?forwardTo=shipUSA',
        'title': '',
        'redirect': 'https://est-oee.canadapost-postescanada.ca/shipping/estShipping.jsp?locale=en_CA&formId=120&isV1=true',
        # FUTURE: parse redirect from document.location="https://est-oee.canadapost-postescanada.ca/shipping/estShipping.jsp?locale=en_CA&formId=120&isV1=true";
        'form': {}
    },
    {
        'assert_url': 'https://www.canadapost.ca/cpid/login.jsp',
        'title': '',
        'redirect': None,
        'form': {
            'name': 'goNext',
            'action': 'https://est-oee.canadapost-postescanada.ca//shipping/estShipping.jsp?formId=120&locale=en_CA&isV1=true',
            'assert': {},
                #  <form name="goNext" action="https://est-oee.canadapost-postescanada.ca//shipping/estShipping.jsp?formId=120&locale=en_CA&isV1=true" metho="POST">
                #  <input type="hidden" name="SSO_USERID" value="********">
                #  <input type="hidden" name="SSO_CUSTOMER_NUMBER" value="********,">
                # <input type="hidden" name="~language"    value="EN">
                #  <input type="hidden" name="SSO_SECURITY_TOKEN" value="">
                #  <input type="hidden" name="SSO_PASSWORD"    value="*********">
                # </form>
        }
    },
    {
        'assert_url': 'https://www.canadapost.ca/cpid/login.jsp',
        'title': '',
        'redirect': None,
        'form': {
            'name': 'goNext',
            'action': 'https://est-oee.canadapost-postescanada.ca/shipping/estShipping.jsp',
            'assert': {},
                # <form name="goNext" action="https://est-oee.canadapost-postescanada.ca//shipping/estShipping.jsp?locale=en_CA&formId=110&SSO_SECURITY_TOKEN=&isV1=true&~language=EN&SSO_USERID=&SSO_PASSWORD=&SSO_CUSTOMER_NUMBER=," method="POST">
                # <input type="hidden" name="SSO_USERID" value="********">
                # <input type="hidden" name="SSO_CUSTOMER_NUMBER" value="*********,">
                # <input type="hidden" name="~language"    value="EN">
                # <input type="hidden" name="SSO_SECURITY_TOKEN" value="">
                # <input type="hidden" name="SSO_PASSWORD"    value="*********">
                # </form>
        }
    },
    {
        'open_url': 'https://obc.canadapost.ca/zcpb2b/b2b/zisa_estForward.do?forwardTo=shipUSA',
        'title': '',
        'redirect': 'https://est-oee.canadapost-postescanada.ca/shipping/estShipping.jsp?locale=en_CA&formId=120&isV1=true',
        'form': {}
    },
    {
        'assert_url': 'https://est-oee.canadapost-postescanada.ca/shipping/estShipping.jsp',
        'redirect': None,
        'form': {
            'name': 'theForm',
            'action': 'https://est-oee.canadapost-postescanada.ca/ShippingServlet',
            'assert': {},
            'fields': SHIP_FORM_FIELDS + [
                # Province: <select name="province" style="width: 214px; font-size: 10pt;">
                # US STATES
                # <option value="AL">Alabama</option>
                # <option value="AK">Alaska</option>
                # <option value="AS">American Samoa</option>
                # <option value="AZ">Arizona</option>
                # <option value="AR">Arkansas</option>
                # <option value="AA">Armed Forces America</option>
                # <option value="AE">Armed Forces Europe</option>
                # <option value="AP">Armed Forces Pacific</option>
                # <option value="CA">California</option>
                # <option value="CO">Colorado</option>
                # <option value="CT">Connecticut</option>
                # <option value="DE">Delaware</option>
                # <option value="DC">District of Columbia</option>
                # <option value="FL">Florida</option>
                # <option value="GA">Georgia</option>
                # <option value="GU">Guam</option>
                # <option value="HI">Hawaii</option>
                # <option value="ID">Idaho</option>
                # <option value="IL">Illinois</option>
                # <option value="IN">Indiana</option>
                # <option value="IA">Iowa</option>
                # <option value="KS">Kansas</option>
                # <option value="KY">Kentucky</option>
                # <option value="LA">Louisiana</option>
                # <option value="ME">Maine</option>
                # <option value="MH">Marshall Islands</option>
                # <option value="MD">Maryland</option>
                # <option value="MA">Massachusetts</option>
                # <option value="MI">Michigan</option>
                # <option value="FM">Micronesia</option>
                # <option value="MN">Minnesota</option>
                # <option value="UM">Minor Outlying Isls.</option>
                # <option value="MS">Mississippi</option>
                # <option value="MO">Missouri</option>
                # <option value="MT">Montana</option>
                # <option value="NE">Nebraska</option>
                # <option value="NV">Nevada</option>
                # <option value="NH">New Hampshire</option>
                # <option value="NJ">New Jersey</option>
                # <option value="NM">New Mexico</option>
                # <option value="NY">New York</option>
                # <option value="NC">North Carolina</option>
                # <option value="ND">North Dakota</option>
                # <option value="MP">North Mariana Isls.</option>
                # <option value="OH">Ohio</option>
                # <option value="OK">Oklahoma</option>
                # <option value="OR">Oregon</option>
                # <option value="PW">Palau</option>
                # <option value="PA">Pennsylvania</option>
                # <option value="PR">Puerto Rico</option>
                # <option value="RI">Rhode Island</option>
                # <option value="SC">South Carolina</option>
                # <option value="SD">South Dakota</option>
                # <option value="TN">Tennessee</option>
                # <option value="TX">Texas</option>
                # <option value="UT">Utah</option>
                # <option value="VT">Vermont</option>
                # <option value="VI">Virgin Islands</option>
                # <option value="VA">Virginia</option>
                # <option value="WA">Washington</option>
                # <option value="WV">West Virginia</option>
                # <option value="WI">Wisconsin</option>
                # <option value="WY">Wyoming</option>
                {
                    'type': 'select',
                    'name': 'province',
                    'data_key': 'recipient_province',
                    'required': True
                },
                # <input type="text" name="postalCode" size="10" maxlength="10" style="width: 215px;"
                {
                    'type': 'text',
                    'name': 'postalCode',
                    'data_key': 'recipient_postal_code',
                    'required': True,
                    'filters': [field_zip_code],
                    'max_length': 10
                },
                # TODO?
                # <input type="Checkbox" name="displayInsuredValue" value="true" >
                ### Misc CP fields:
                # assert nextPageFormId value = 111
                {
                    'type': 'hidden',
                    'name': 'nextPageFormId',
                    'default': '111'
                }
            ]
        }
    },
    {
        'assert_url': 'https://est-oee.canadapost-postescanada.ca/shipping/estShipping.jsp?locale=en_CA&formId=122',
        'redirect': None,
        'form': {
            'name': 'theForm',
            'action': 'https://est-oee.canadapost-postescanada.ca/ShippingServlet',
            'assert': {},
            # ENABLE customs fields for this form
            'customs': True,
            'fields': CUSTOMS_INFO_FIELDS + [
                {
                    'type': 'hidden',
                    'name': 'formId',
                    'default': '124'
                },
                {
                    'type': 'hidden',
                    'name': 'nextPageFormId',
                    'default': '124'
                }
            ]
        }
    },
    {
        'assert_url': 'https://est-oee.canadapost-postescanada.ca/shipping/estShipping.jsp?locale=en_CA&formId=124',
        'redirect': None,
        'form': {
            'name': 'theForm',
            'action': 'https://est-oee.canadapost-postescanada.ca/ParcelMailTransmitServlet',
            'assert': {},
            'fields': PAYMENT_FORM_FIELDS
        }
    },
    {
        'assert_url': 'https://est-oee.canadapost-postescanada.ca/shipping/parcelMailViewLabelFrameset.jsp?label=forward&locale=en_CA',
        'redirect': 'https://est-oee.canadapost-postescanada.ca/shipping/../waitingForPDF.jsp?servletName=ParcelMailViewLabelServlet&label=forward&locale=en_CA&language=en_CA',
        'form': {}
    },
    {
         # Send request to generate Preview PDF\ndocument.location.replace("ParcelMailViewLabelServlet?useraction=null&label=forward");
        'download': 'https://est-oee.canadapost-postescanada.ca/shipping/../ParcelMailViewLabelServlet?useraction=null&label=forward',
        'form': {}
    }
]


# International Shipping

EST_SHIP_INTL_PIPELINE = [
    {
        'open_url': 'https://obc.canadapost.ca/zcpb2b/b2b/zisa_estForward.do?forwardTo=shipIntl',
        'title': '',
        'redirect': 'https://est-oee.canadapost-postescanada.ca/shipping/estShipping.jsp?locale=en_CA&formId=130&isV1=true',
        # FUTURE: parse redirect from document.location="https://est-oee.canadapost-postescanada.ca/shipping/estShipping.jsp?locale=en_CA&formId=120&isV1=true";
        'form': {}
    },
    {
        'assert_url': 'https://www.canadapost.ca/cpid/login.jsp',
        'title': '',
        'redirect': None,
        'form': {
            'name': 'goNext',
            'action': 'https://est-oee.canadapost-postescanada.ca//shipping/estShipping.jsp?formId=130&locale=en_CA&isV1=true',
            'assert': {},
                #  <form name="goNext" action="https://est-oee.canadapost-postescanada.ca//shipping/estShipping.jsp?formId=120&locale=en_CA&isV1=true" metho="POST">
                #  <input type="hidden" name="SSO_USERID" value="********">
                #  <input type="hidden" name="SSO_CUSTOMER_NUMBER" value="********,">
                # <input type="hidden" name="~language"    value="EN">
                #  <input type="hidden" name="SSO_SECURITY_TOKEN" value="">
                #  <input type="hidden" name="SSO_PASSWORD"    value="*********">
                # </form>
        }
    },
    {
        'assert_url': 'https://www.canadapost.ca/cpid/login.jsp',
        'title': '',
        'redirect': None,
        'form': {
            'name': 'goNext',
            'action': 'https://est-oee.canadapost-postescanada.ca/shipping/estShipping.jsp',
            'assert': {},
                # <form name="goNext" action="https://est-oee.canadapost-postescanada.ca//shipping/estShipping.jsp?locale=en_CA&formId=130," method="POST">
                # <input type="hidden" name="SSO_USERID" value="********">
                # <input type="hidden" name="SSO_CUSTOMER_NUMBER" value="*********,">
                # <input type="hidden" name="~language"    value="EN">
                # <input type="hidden" name="SSO_SECURITY_TOKEN" value="">
                # <input type="hidden" name="SSO_PASSWORD"    value="*********">
                # </form>
        }
    },
    {
        'open_url': 'https://obc.canadapost.ca/zcpb2b/b2b/zisa_estForward.do?forwardTo=shipIntl',
        'title': '',
        'redirect': 'https://est-oee.canadapost-postescanada.ca/shipping/estShipping.jsp?locale=en_CA&formId=130&isV1=true',
        'form': {}
    },
    {
        'assert_url': 'https://est-oee.canadapost-postescanada.ca/shipping/estShipping.jsp',
        'redirect': None,
        'form': {
            'name': 'theForm',
            'action': 'https://est-oee.canadapost-postescanada.ca/ShippingServlet',
            'assert': {},
            'fields': SHIP_FORM_FIELDS + [
            # <input type="Text" name="province" size="20" maxlength="20" style="width: 215px;" value="" onChange="return isValidChars(this, 323, null, null)">
                {
                    'type': 'text',
                    'name': 'province',
                    'data_key': 'recipient_province',
                    'required': True,
                    'max_length': 20
                },
                # <select name="country" style="width: 214px; font-size: 10pt;">
                # 2 char country code
                {
                    'type': 'select',
                    'name': 'country',
                    'data_key': 'recipient_country',
                    'required': True,
                    'max_length': 2
                },
                # <input type="text" name="postalCode" style="width: 215px;" maxlength="14"
                {
                    'type': 'text',
                    'name': 'postalCode',
                    'data_key': 'recipient_postal_code',
                    'required': True,
                    'filters': [field_to_upper],
                    'max_length': 14
                },
                ### Misc CP fields:
                # assert nextPageFormId value = 121 for intl
                {
                    'type': 'hidden',
                    'name': 'nextPageFormId',
                    'default': '121'
                }
            ]
        }
    },
    {
        'assert_url': 'https://est-oee.canadapost-postescanada.ca/shipping/estShipping.jsp?locale=en_CA&formId=132',
        'redirect': None,
        'form': {
            'name': 'theForm',
            'action': 'https://est-oee.canadapost-postescanada.ca/ShippingServlet',
            'assert': {},
            # ENABLE customs fields for this form
            'customs': True,
            'fields': CUSTOMS_INFO_FIELDS + [
                {
                    'type': 'hidden',
                    'name': 'formId',
                    'default': '132'
                },
                {
                    'type': 'hidden',
                    'name': 'nextPageFormId',
                    'default': '134'
                },
            ]
        }
    },
    {
        'assert_url': 'https://est-oee.canadapost-postescanada.ca/shipping/estShipping.jsp?locale=en_CA&formId=134',
        'redirect': None,
        'form': {
            'name': 'theForm',
            'action': 'https://est-oee.canadapost-postescanada.ca/ParcelMailTransmitServlet',
            'assert': {},
            'fields': PAYMENT_FORM_FIELDS
        }
    },
    {
        'assert_url': 'https://est-oee.canadapost-postescanada.ca/shipping/parcelMailViewLabelFrameset.jsp?label=forward&locale=en_CA',
        'redirect': 'https://est-oee.canadapost-postescanada.ca/shipping/../waitingForPDF.jsp?servletName=ParcelMailViewLabelServlet&label=forward&locale=en_CA&language=en_CA',
        'form': {}
    },
    {
         # Send request to generate Preview PDF\ndocument.location.replace("ParcelMailViewLabelServlet?useraction=null&label=forward");
        'download': 'https://est-oee.canadapost-postescanada.ca/shipping/../ParcelMailViewLabelServlet?useraction=null&label=forward',
        'form': {}
    }
]
