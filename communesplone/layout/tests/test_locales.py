# -*- coding: utf-8 -*-
"""Translations of locales/ (compiled by zope_i18n_compile_mo_files)."""
from communesplone.layout.testing import INTEGRATION
from zope.component import getUtility
from zope.i18n import translate
from zope.i18n.interfaces import ITranslationDomain

import os
import unittest


LOCALES = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'locales')


class TestLocales(unittest.TestCase):

    layer = INTEGRATION

    def test_communesplone_layout_domain(self):
        catalogs = getUtility(ITranslationDomain, 'communesplone.layout').getCatalogsInfo()
        self.assertTrue(set(['de', 'en', 'es', 'fr', 'nl']).issubset(catalogs))
        self.assertEqual(catalogs['fr'], [os.path.join(LOCALES, 'fr', 'LC_MESSAGES', 'communesplone.layout.mo')])
        self.assertEqual(
            translate('no_source_users', domain='communesplone.layout', target_language='fr'),
            u'La connexion au site est momentanément suspendue pour raison de maintenance. Si besoin, vous pouvez '
            u'<a href="contact-info">contacter l\'administrateur du site</a> pour plus d\'informations.')
        self.assertEqual(translate('label_captcha', domain='communesplone.layout', target_language='fr'),
                         u'Code de vérification')
        self.assertEqual(translate('help_captcha', domain='communesplone.layout', target_language='fr'),
                         u'Recopiez le texte de l\'image ci-dessous, ceci permet de lutter contre le SPAM.')
        self.assertEqual(
            translate(u'Please provide the message here above correctly, case sensitive.',
                      domain='communesplone.layout', target_language='fr'),
            u'Recopiez les lettres et chiffres ci-dessous correctement en respectant la casse (majuscules/minuscules).')

    def test_plone_domain(self):
        """The overrides of locales/*/plone.po are registered after plone.app.locales: Plone's msgstr wins."""
        catalogs = getUtility(ITranslationDomain, 'plone').getCatalogsInfo()['fr']
        self.assertIn('plone.app.locales', catalogs[0])
        self.assertEqual(catalogs[-1], os.path.join(LOCALES, 'fr', 'LC_MESSAGES', 'plone.mo'))
        # overrides: u'Créé par Chris', u'cliquez ici pour le récupérer'
        self.assertEqual(translate('label_by_author', domain='plone', target_language='fr', mapping={'author': 'Chris'}),
                         u'Par Chris')
        self.assertEqual(translate('label_click_here_to_retrieve', domain='plone', target_language='fr'),
                         u'nous pouvons vous en envoyer un nouveau')
