# -*- coding: utf-8 -*-
"""Translations of locales/ (compiled by zope_i18n_compile_mo_files)."""
from __future__ import unicode_literals
from communesplone.layout.testing import INTEGRATION
from zope.component import getUtility
from zope.i18n import translate
from zope.i18n.interfaces import ITranslationDomain

import os
import unittest


LOCALES = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "locales"
)


class TestLocales(unittest.TestCase):

    layer = INTEGRATION

    def test_communesplone_layout_domain(self):
        catalogs = getUtility(
            ITranslationDomain, "communesplone.layout"
        ).getCatalogsInfo()
        self.assertTrue(set(["de", "en", "es", "fr", "nl"]).issubset(catalogs))
        self.assertEqual(
            catalogs["fr"],
            [os.path.join(LOCALES, "fr", "LC_MESSAGES", "communesplone.layout.mo")],
        )
        self.assertEqual(
            translate(
                "no_source_users", domain="communesplone.layout", target_language="fr"
            ),
            "La connexion au site est momentanément suspendue pour raison de maintenance. Si besoin, vous pouvez "
            "<a href=\"contact-info\">contacter l'administrateur du site</a> pour plus d'informations.",
        )
        self.assertEqual(
            translate(
                "label_captcha", domain="communesplone.layout", target_language="fr"
            ),
            "Code de vérification",
        )
        self.assertEqual(
            translate(
                "help_captcha", domain="communesplone.layout", target_language="fr"
            ),
            "Recopiez le texte de l'image ci-dessous, ceci permet de lutter contre le SPAM.",
        )
        self.assertEqual(
            translate(
                "Please provide the message here above correctly, case sensitive.",
                domain="communesplone.layout",
                target_language="fr",
            ),
            "Recopiez les lettres et chiffres ci-dessous correctement en respectant la casse (majuscules/minuscules).",
        )

    def test_plone_domain(self):
        """The overrides of locales/*/plone.po are registered after plone.app.locales: Plone's msgstr wins."""
        catalogs = getUtility(ITranslationDomain, "plone").getCatalogsInfo()["fr"]
        self.assertIn("plone.app.locales", catalogs[0])
        self.assertEqual(
            catalogs[-1], os.path.join(LOCALES, "fr", "LC_MESSAGES", "plone.mo")
        )
        # overrides: u'Créé par Chris', u'cliquez ici pour le récupérer'
        self.assertEqual(
            translate(
                "label_by_author",
                domain="plone",
                target_language="fr",
                mapping={"author": "Chris"},
            ),
            "Par Chris",
        )
        self.assertEqual(
            translate(
                "label_click_here_to_retrieve", domain="plone", target_language="fr"
            ),
            "nous pouvons vous en envoyer un nouveau",
        )
