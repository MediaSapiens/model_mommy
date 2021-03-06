# -*- coding:utf-8 -*-

from django.test import TestCase
from django.db.models.fields.related import *


class TestDummyRelationModel(TestCase):
    def test_model_has_no_fields_but_pk(self):
        from django.db.models.fields import AutoField
        from model_mommy.models import DummyRelationModel

        fields = DummyRelationModel._meta.fields

        self.assertEqual(len(fields), 1)
        self.assertTrue(isinstance(fields[0], AutoField))


class TestFillingOneToOneField(TestCase):
    def test_create_model_with_OneToOneField(self):
        from model_mommy.models import DummyOneToOneModel
        from model_mommy.models import DummyRelationModel
        from model_mommy import mommy

        dummy_one_to_one_model = mommy.make_one(DummyOneToOneModel)
        one_to_one_field = dummy_one_to_one_model._meta.get_field('one_to_one_field')

        self.assertTrue(isinstance(one_to_one_field, OneToOneField))
        self.assertTrue(
            isinstance(
                dummy_one_to_one_model.one_to_one_field, DummyRelationModel))


class TestFillingForeignKey(TestCase):
    def test_create_model_with_ForeignKey(self):
        from model_mommy.models import DummyForeignKeyModel
        from model_mommy.models import DummyRelationModel
        from model_mommy import mommy

        dummy_foreignkey_model = mommy.make_one(DummyForeignKeyModel)
        foreignkey_field = dummy_foreignkey_model._meta.get_field('foreignkey_field')

        self.assertTrue(isinstance(foreignkey_field, ForeignKey))
        self.assertTrue(isinstance(
            dummy_foreignkey_model.foreignkey_field, DummyRelationModel))


class TestFillingM2MField(TestCase):
    def test_create_model_with_M2MField(self):
        """
        M2M fields should be populated manually.

        """
        from model_mommy.models import DummyM2MModel
        from model_mommy.models import DummyRelationModel
        from model_mommy import mommy

        dummy_m2m_model = mommy.make_one(DummyM2MModel)
        m2m_field = DummyM2MModel._meta.get_field('m2m_field')

        self.assertTrue(isinstance(m2m_field, ManyToManyField))
        self.assertEqual(DummyRelationModel.objects.count(), 0)
        self.assertEqual(dummy_m2m_model.m2m_field.count(), 0)

    def test_prepare_model_with_M2MField_does_not_hit_database(self):
        from model_mommy.models import DummyM2MModel
        from model_mommy.models import DummyRelationModel
        from model_mommy import mommy

        dummy_m2m_model = mommy.prepare_one(DummyM2MModel)

        # relation is not created if parent model is not persisted
        self.assertEqual(DummyRelationModel.objects.count(), 0)
        self.assertRaises(ValueError, lambda: dummy_m2m_model.m2m_field)


class TestFillingSelfReferenceModels(TestCase):
    def test_create_self_reference_model(self):
        from model_mommy.models import DummySelfReferenceModel
        from model_mommy import mommy

        dummy_selfref_model = mommy.make_one(DummySelfReferenceModel)

    def test_filling_self_reference_ForeignKey(self):
        from model_mommy.models import DummySelfReferenceModel
        from model_mommy import mommy

        dummy_selfref_model = mommy.make_one(DummySelfReferenceModel)
        foreignkey_value = dummy_selfref_model.foreignkey_field
        foreignkey_field = dummy_selfref_model._meta.get_field('foreignkey_field')

        self.assertTrue(isinstance(foreignkey_field, ForeignKey))
        self.assertTrue(foreignkey_value is None)

    def test_filling_self_reference_OneToOneField(self):
        from model_mommy.models import DummySelfReferenceModel
        from model_mommy import mommy

        dummy_selfref_model = mommy.make_one(DummySelfReferenceModel)
        one_to_one_value = dummy_selfref_model.one_to_one_field
        one_to_one_field = dummy_selfref_model._meta.get_field('one_to_one_field')

        self.assertTrue(isinstance(one_to_one_field, OneToOneField))
        self.assertTrue(one_to_one_value is None)

    def test_filling_self_reference_M2MField(self):
        from model_mommy.models import DummySelfReferenceModel
        from model_mommy import mommy

        dummy_selfref_model = mommy.make_one(DummySelfReferenceModel)
        m2m_value = dummy_selfref_model.m2m_field
        m2m_field = dummy_selfref_model._meta.get_field('m2m_field')

        self.assertTrue(isinstance(m2m_field, ManyToManyField))
        self.assertEqual(m2m_value.count(), 0)
