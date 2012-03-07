import sys
import time
import logging
import mechanize
import cookielib
import tempfile
from urlparse import urlparse
from urllib2 import HTTPError

from pipelines import EST_SSO_PIPELINE, EST_SHIP_CANADA_PIPELINE, EST_SHIP_INTL_PIPELINE, \
                        EST_SHIP_USA_PIPELINE, CUSTOMS_LINE_FIELDS

logger = logging.getLogger("mechanize")
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)
logger = logging.getLogger("canadapost")
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)


class PipelineException(Exception):
    pass


class URLMismatchException(PipelineException):
    pass


class FormFieldException(PipelineException):
    pass


class CanadaPostBot():
    # This is probably bad, not used at the moment
    #USER_AGENT = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    DEBUG = False
    data = {}
    logged_in = False

    def __init__(self, defaults={}, cookiejar_file='temp.cookie'):
        self.data = defaults
        self.logged_in = False
        self.cookiejar = cookielib.LWPCookieJar(cookiejar_file)
        self.browser = mechanize.Browser()
        self.browser.set_cookiejar(self.cookiejar)

    def set_browser_options(self):
        # Browser options
        self.browser.set_handle_equiv(True)
        # self.browser.set_handle_gzip(True)
        self.browser.set_handle_redirect(True)
        self.browser.set_handle_referer(True)
        self.browser.set_handle_robots(False)

    def save_cookiejar(self):
        logger.info("Saving cookiejar to %s", self.cookiejar.filename)
        self.cookiejar.save()

    def open_url(self, url):
        self.browser.open(url)
        assert self.browser.viewing_html()
        logger.debug(self.browser.title())
        logger.debug(self.browser.geturl())

    def customs_data(self):
        try:
            return self.data['items']
        except KeyError:
            raise PipelineException('No customs line items found!')

    def get_form_field_value(self, field):
        value = None
        try:
            # get the value
            if 'data_key' in field and field['data_key'] in self.data:
                # if data_key is specified, try that first
                value = self.data[field['data_key']]
            else:
                # otherwise, try the default value (if specified)
                value = field['default']

            if field['type'] == 'text':
                if 'filters' in field:
                    for fltr in field['filters']:
                        value = fltr(value)
            elif field['type'] == 'select':
                # selects must be set as an iterable
                if type(value) != list:
                    value = [value]
            elif field['type'] in ['checkbox', 'hidden']:
                pass
        except KeyError:
            # data key not found.. check if the field is required
            # if we have an actual form, see if the field is filled
            if 'required' in field and field['required']:
                if self.browser.form and self.browser.form[field['name']]:
                    return None  # field has a value, so don't worry about it
                raise FormFieldException('Could not fill required form field %s, required data key %s' % (field['name'], field['data_key']))
            else:
                return None
        return value

    def fill_form_field(self, field):
        logger.info("Filling form field <%s (%s)>", field['type'], field['name'])
        if field['type'] == 'text':
            value = self.get_form_field_value(field)
            if value is not None:
                self.browser.form[field['name']] = value
        elif field['type'] == 'select':
            value = self.get_form_field_value(field)
            if value is not None:
                self.browser.form[field['name']] = value
        elif field['type'] == 'checkbox':
            ctrl = self.browser.form.find_control(field['name'])
            ctrl.items[0].selected = self.get_form_field_value(field)
        elif field['type'] == 'hidden':
            # check value and set hidden value
            ctrl = self.browser.form.find_control(field['name'])
            ctrl.attrs['value'] = self.get_form_field_value(field)

    def fill_customs_line(self, index, item):
        # item contains:
        #   'description': 'Handmade bow tie',
        #   'quantity': 2,
        #   'unit_price': Decimal('10.00'),
        # if _index > 6: log the error and break
        if index > 6:
            logger.warning("Can't fill more than 6 customs lines!")
            return False
        for field_name, field_data in CUSTOMS_LINE_FIELDS.items():
            # for each field, add to customs_field
            _field = field_data.copy()
            _field.update({'name': field_data['name'] % index})
            if field_name in item:
                # if the field has been passed in, set the value
                _field.update({'default': item[field_name]})
            elif field_data['required'] and 'default' not in field_data:
                # required field has no default
                raise FormFieldException('Missing required field for customs line: %s' % field_name)
            elif not field_data['required'] and 'default' not in field_data:
                # not required and no default = ignore
                continue
            self.fill_form_field(_field)
        return True

    def fill_form(self, form):
        logger.debug("Handling form: %s", form['name'])
        self.browser.select_form(name=form['name'])
        # TODO: assert form elements
        # TODO: assert action
        if self.browser.form.action == form['action']:
            logger.debug("Form action (%s) is valid!", form['action'])
        else:
            logger.warning("Invalid form actions: expected %s, found %s", form['action'], self.browser.form.action)
        # set form fields
        if 'fields' in form:
            for f in form['fields']:
                self.fill_form_field(f)
        # fill customs data
        if 'customs' in form and form['customs']:
            for i, item in enumerate(self.customs_data()):
                # canada post counting starts at 1
                self.fill_customs_line(i + 1, item)

    def submit_form(self, form=None):
        if not self.browser.form:
            self.browser.select_form(name=form['name'])
        logger.info('Submitting form %s...', str(self.browser.form))
        for ctrl in self.browser.form.controls:
            logger.info('\t%s', str(ctrl))
        return self.browser.submit()

    def download_file(self, url):
        logger.info('Downloading file from: %s', url)
        return self.browser.retrieve(url)[0]

    def save_file(self, f, ext='.pdf'):
        fh = open(f)
        # save to random file location
        (fd, fpath) = tempfile.mkstemp(suffix=ext)
        outfile = open(fpath, 'w')
        outfile.write(fh.read())
        outfile.close()
        logger.info('Saved PDF : %s', fpath)
        return fpath

    def assert_url(self, expected):
        o = urlparse(self.browser.geturl())
        # remove url parameters from found url
        found = '%s://%s%s' % (o.scheme, o.netloc, o.path.replace('//', '/'))
        if expected.startswith('/'):
            expected = '%s://%s%s' % (o.scheme, o.netloc, expected)
        p = urlparse(expected)
        # remove url parameters from expected url
        expected = '%s://%s%s' % (p.scheme, p.netloc, p.path.replace('//', '/'))
        if found != expected:
            raise URLMismatchException('Found/expected urls not equal.\n\tFound: %s\n\tExpected %s' % (found, expected))

    def run_pipeline(self, pipeline, sleep=0, steps=None):
        _error = ''
        download = None  # waybill to be returned
        # _stored_exception = None
        try:
            # for each page in the pipeline
            # get the url and submit the form
            # assert the next page is expected
            logger.info("Starting pipeline...")
            for i, page in enumerate(pipeline):
                self.current_page = page
                if 'open_url' in page:
                    self.browser.open(page['open_url'])
                if 'assert_url' in page:
                    self.assert_url(page['assert_url'])
                logger.info("Handling page: %s ..." % self.browser.geturl()[:50])
                # TODO: assert page elements exist
                if 'form' in page and page['form']:
                    self.fill_form(page['form'])
                    response = self.submit_form()
                    logger.debug(response.geturl())
                    logger.debug(response.read())
                elif 'redirect' in page and page['redirect']:
                    # do a redirect
                    self.browser.open(page['redirect'])
                elif 'download' in page and page['download']:
                    download = self.download_file(page['download'])
                else:
                    raise PipelineException('No action defined in pipeline page')
                time.sleep(sleep)
        except PipelineException as e:
            _error = str(e)
        except HTTPError as e:
            _error = 'HTTP error, most likely a problem with the submitted form.'

        logger.info("Final pipeline url: %s", self.browser.geturl())
        self.save_cookiejar()

        if _error:
            logger.info("Pipeline encountered an error!")
            logger.error(_error)
            return None
        else:
            logger.info("Pipeline complete!")
            return download

    def audit_pipeline(self, pipeline):
        """Audit a pipeline
            This checks all the forms in the given pipeline and verifies
            that all the required data is present in self.data
        """
        ok = True
        for i, page in enumerate(pipeline):
            if page['form'] and 'fields' in page['form']:
                for f in page['form']['fields']:
                    try:
                        if 'data_key' in f:
                            self.get_form_field_value(f)
                    except FormFieldException as e:
                        logger.error(str(e))
                        ok = False
        return ok

    ### API

    def login(self, credentials={}):
        """ credentials should contain the keys 'username' and 'password',
            otherwise the defaults will be used. """
        if self.logged_in:
            return
        self.data.update(credentials)
        if self.run_pipeline(pipeline=EST_SSO_PIPELINE):
            self.logged_in = True

    def generate_waybill(self, country, skip_login=False, **kwargs):
        self.login()
        # load the data
        self.data.update(kwargs)
        if country == 'CA':
            if skip_login:
                # already generated a waybill, use shorter pipeline
                pipeline = [EST_SHIP_CANADA_PIPELINE[3], EST_SHIP_CANADA_PIPELINE[4]]
            else:
                pipeline = EST_SHIP_CANADA_PIPELINE
        elif country == 'US':
            if skip_login:
                # already generated a waybill, use shorter pipeline
                pipeline = [EST_SHIP_USA_PIPELINE[3], EST_SHIP_USA_PIPELINE[4]]
            else:
                pipeline = EST_SHIP_USA_PIPELINE
        else:
            # international
            if skip_login:
                # already generated a waybill, use shorter pipeline
                pipeline = [EST_SHIP_INTL_PIPELINE[3], EST_SHIP_INTL_PIPELINE[4]]
            else:
                pipeline = EST_SHIP_INTL_PIPELINE

        if not self.audit_pipeline(pipeline):
            logger.error("Some form parameters were missing...")
            return None
        else:
            return self.run_pipeline(pipeline)

    def quote_waybill(self, country, **kwargs):
        self.login()
        # TODO
        pass

    def get_stored_data(self, country):
        self.login()
        fields = ['clientId', 'isVentureOne', 'contactName', 'shipperPhone',
                    'preferredMethodOfPayment', 'shippingPointPC', 'selectedTemplate']
        stored_data = {}

        if country == 'CA':
            result = self.run_pipeline(pipeline=EST_SHIP_CANADA_PIPELINE[:4])
            # stopped at the form, extract info from the form page
        elif country == 'US':
            result = self.run_pipeline(pipeline=EST_SHIP_USA_PIPELINE[:4])
        else:
            result = self.run_pipeline(pipeline=EST_SHIP_INTL_PIPELINE[:4])

        if not result:
            logger.error('Error in pipeline... cannot get stored data')
            return {}
        else:
            self.browser.select_form(self.current_page['form']['name'])  # usually 'theForm'
            for field in fields:
                ctrl = self.browser.form.find_control(field)
                if ctrl.type in ['hidden', 'text']:
                    # check for boolean
                    if ctrl.attrs['value'] == 'true':
                        stored_data[field] = True
                    elif ctrl.attrs['value'] == 'false':
                        stored_data[field] = False
                    else:
                        stored_data[field] = ctrl.attrs['value']
                elif ctrl.type == 'select':
                    stored_data[field] = []
                    for item in ctrl.get_items():
                        stored_data[field] = item.attrs
            return stored_data
