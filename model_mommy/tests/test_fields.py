# -*- coding:utf-8 -*-
from django.db.models.fields import *
from django.db.models.fields.related import *
from django.db.models.fields.files import *

from django.test import TestCase
import django

from decimal import Decimal

if django.VERSION < (1, 2):
    BigIntegerField = IntegerField


class HandlingModelsWithUnsupportedFields(TestCase):

    def test_unsupported_model_raises_an_explanatory_exception(self):
        from model_mommy import mommy
        from model_mommy.models import UnsupportedModel

        self.assertRaises(TypeError, lambda: mommy.make_one(UnsupportedModel))


class TestFillingSlugField(TestCase):

    def is_slug(self, slug):
        import string

        slug_table = string.letters + string.digits + '_-'
        for char in slug:
            if char not in slug_table:
                return False
        return True

    def test_create_model_with_slugfield(self):
        from model_mommy import mommy
        from model_mommy.models import DummySlugModel

        dummy_slug_model = mommy.make_one(DummySlugModel)
        self.assertTrue(
            isinstance(dummy_slug_model.slug_field, basestring))

    def test_if_data_for_slugfield_is_slug_text(self):
        from model_mommy.models import DummySlugModel
        from model_mommy import mommy

        dummy_slug_model = mommy.make_one(DummySlugModel)
        self.assertTrue(
            self.is_slug(dummy_slug_model.slug_field))


class TestFillingStringFields(TestCase):

    def test_create_model_with_CharField(self):
        from model_mommy import mommy
        from model_mommy.models import DummyCharModel

        char_field = DummyCharModel._meta.get_field('char_field')
        self.assertTrue(isinstance(char_field, CharField))

        dummy_char_model = mommy.make_one(DummyCharModel)
        self.assertTrue(
            isinstance(dummy_char_model.char_field, basestring))

    def test_create_model_with_TextField(self):
        from model_mommy import mommy
        from model_mommy.models import DummyTextModel

        text_field = DummyTextModel._meta.get_field('text_field')
        self.assertTrue(isinstance(text_field, TextField))

        dummy_text_model = mommy.make_one(DummyTextModel)
        self.assertTrue(
            isinstance(dummy_text_model.text_field, basestring))


class TestFillingXMLFields(TestCase):
    def test_create_model_with_xml_field(self):
        from model_mommy import mommy
        from model_mommy.models import DummyXMLModel
        from xml.dom.minidom import parseString, Document

        dummy_model = mommy.make_one(DummyXMLModel)
        xml_field = DummyXMLModel._meta.get_field('xml_field')
        xml_value = dummy_model.xml_field

        self.assertTrue(isinstance(xml_field, XMLField))
        self.assertTrue(isinstance(xml_value, basestring))
        self.assertTrue(isinstance(parseString(xml_value), Document))


class TestFillingEmailFields(TestCase):

    def test_create_model_with_email_field(self):
        from model_mommy import mommy
        from model_mommy.models import DummyEmailModel

        dummy_email_model = mommy.make_one(DummyEmailModel)
        email_field = DummyEmailModel._meta.get_field('email_field')

        self.assertTrue(isinstance(email_field, EmailField))
        self.assertTrue(
            isinstance(dummy_email_model.email_field, basestring))

    def test_if_generated_email_format_is_valid(self):
        import re
        import string

        from model_mommy import mommy
        from model_mommy.models import DummyEmailModel

        dummy_email_model = mommy.make_one(DummyEmailModel)
        data = dummy_email_model.email_field

        table = string.letters + string.digits + "!#$%&'*+-/=?^_`{|}~."

        m = re.match(r"[%(t)s]+@[%(t)s](\.[%(t)s]+)*" % {'t': table}, data)
        self.assertTrue(m is not None)
        self.assertTrue('..' not in data)
        self.assertTrue(data[0] != '.')
        self.assertTrue(data[-1] != '.')


class TestFillingBooleanFields(TestCase):

    def test_create_model_with_BooleanField(self):
        from model_mommy import mommy
        from model_mommy.models import DummyBooleanModel

        dummy_boolean_model = mommy.make_one(DummyBooleanModel)
        boolean_field = DummyBooleanModel._meta.get_field('boolean_field')

        self.assertTrue(isinstance(boolean_field, BooleanField))
        self.assertTrue(
            isinstance(dummy_boolean_model.boolean_field, bool))


class TestFillingDateFields(TestCase):

    def test_create_model_with_DateField(self):
        from model_mommy import mommy
        from model_mommy.models import DummyDateModel

        from datetime import date

        dummy_date_model = mommy.make_one(DummyDateModel)
        date_field = dummy_date_model._meta.get_field('date_field')

        self.assertTrue(isinstance(date_field, DateField))
        self.assertTrue(
            isinstance(dummy_date_model.date_field, date))


class TestFillingDateTimeFields(TestCase):

    def test_create_model_with_DateTimeField(self):
        from model_mommy import mommy
        from model_mommy.models import DummyDateTimeModel

        from datetime import date

        dummy_datetime_model = mommy.make_one(DummyDateTimeModel)
        datetime_field = dummy_datetime_model._meta.get_field('datetime_field')

        self.assertTrue(isinstance(datetime_field, DateTimeField))
        self.assertTrue(
            isinstance(dummy_datetime_model.datetime_field, date))


class TestFillingIPAddressFields(TestCase):

    def test_create_model_withIPAddressField(self):
        from model_mommy import mommy
        from model_mommy.models import IPAddressModel

        dummy_ipaddress_model = mommy.make_one(IPAddressModel)
        ip_address_value = dummy_ipaddress_model.ip_address_field

        tokens = ip_address_value.split('.')

        for token in tokens:
            self.assertTrue(token.isdigit())

        self.assertEqual(len(tokens), 4)  # IPV4 only


class TestFillingIntFields(TestCase):

    def setUp(self):
        from model_mommy import mommy
        from model_mommy.models import DummyIntModel

        self.dummy_int_model = mommy.make_one(DummyIntModel)

    def test_create_model_with_IntegerField(self):
        from model_mommy.models import DummyIntModel

        int_field = DummyIntModel._meta.get_field('int_field')
        self.assertTrue(isinstance(int_field, IntegerField))

        self.assertTrue(isinstance(self.dummy_int_model.int_field, int))

    def test_create_model_with_BigIntegerField(self):
        from model_mommy.models import DummyIntModel

        big_int_field = DummyIntModel._meta.get_field('big_int_field')
        self.assertTrue(isinstance(big_int_field, BigIntegerField))

        self.assertTrue(isinstance(self.dummy_int_model.big_int_field, long))

    def test_create_model_with_SmallIntegerField(self):
        from model_mommy.models import DummyIntModel

        small_int_field = DummyIntModel._meta.get_field('small_int_field')
        self.assertTrue(isinstance(small_int_field, SmallIntegerField))

        self.assertTrue(isinstance(self.dummy_int_model.small_int_field, int))
        self.assertTrue(self.dummy_int_model.small_int_field >= -32768)
        self.assertTrue(self.dummy_int_model.small_int_field <= 32768)


class TestFillingPositiveIntFields(TestCase):

    def setUp(self):
        from model_mommy import mommy
        from model_mommy.models import DummyPositiveIntModel

        self.dummy_positive_int_model =\
            mommy.make_one(DummyPositiveIntModel)

    def test_create_model_with_PositiveSmallIntegerField(self):
        from model_mommy.models import DummyPositiveIntModel
        from model_mommy.mommy import POS_MAX_SMALL_INT

        dummy_model = self.dummy_positive_int_model

        positive_small_int_value = dummy_model.positive_small_int_field
        positive_small_int_field = DummyPositiveIntModel.\
            _meta.get_field('positive_small_int_field')

        self.assertTrue(isinstance(
            positive_small_int_field, PositiveSmallIntegerField))

        self.assertTrue(isinstance(positive_small_int_value, int))
        self.assertTrue(positive_small_int_value >= 0)
        self.assertTrue(positive_small_int_value <= POS_MAX_SMALL_INT)

    def test_create_model_with_PositiveIntegerField(self):
        from model_mommy.models import DummyPositiveIntModel
        from model_mommy.mommy import POS_MAX_INT

        dummy_model = self.dummy_positive_int_model

        positive_int_value = dummy_model.positive_int_field
        positive_int_field = DummyPositiveIntModel.\
            _meta.get_field('positive_int_field')

        self.assertTrue(
            isinstance(positive_int_field, PositiveIntegerField))

        self.assertTrue(positive_int_value >= 0)
        self.assertTrue(positive_int_value <= POS_MAX_INT)


class TestFillingOthersNumericFields(TestCase):

    def test_create_model_with_FloatField(self):
        from model_mommy import mommy
        from model_mommy.models import DummyNumbersModel

        self.dummy_numbers_model = mommy.make_one(DummyNumbersModel)
        float_field = DummyNumbersModel._meta.get_field('float_field')

        self.assertTrue(isinstance(float_field, FloatField))
        self.assertTrue(isinstance(
            self.dummy_numbers_model.float_field, float))

    def test_create_model_with_DecimalField(self):
        from model_mommy import mommy
        from model_mommy.models import DummyDecimalModel

        dummy_model = mommy.make_one(DummyDecimalModel)

        decimal_field =\
            DummyDecimalModel._meta.get_field('decimal_field')

        self.assertTrue(isinstance(decimal_field, DecimalField))
        self.assertTrue(isinstance(
            dummy_model.decimal_field, Decimal))


class TestFillingURLFields(TestCase):

    def test_create_model_with_URLField(self):
        from model_mommy import mommy
        from model_mommy.models import DummyURLModel

        dummy_url_field = mommy.make_one(DummyURLModel)
        url_field = dummy_url_field._meta.get_field('url_field')

        self.assertTrue(isinstance(url_field, URLField))
        self.assertTrue(
            isinstance(dummy_url_field.url_field, basestring))


class TestFillingFileFields(TestCase):

    def test_create_model_with_FileField(self):
        from model_mommy import mommy
        from model_mommy.models import DummyFileModel

        dummy_file_model = mommy.make_one(DummyFileModel)
        file_field = dummy_file_model._meta.get_field('file_field')

        self.assertTrue(isinstance(file_field, FileField))
        self.assertTrue(
            isinstance(dummy_file_model.file_field.url, basestring))

    def test_create_model_with_ImageField(self):
        from model_mommy import mommy
        from model_mommy.models import DummyImageModel

        dummy_image_model = mommy.make_one(DummyImageModel)
        image_field = dummy_image_model._meta.get_field('image_field')

        self.assertTrue(isinstance(image_field, FileField))
        self.assertTrue(
            isinstance(dummy_image_model.image_field.url, basestring))