Changelog
=========

5.0.0 (unreleased)
------------------

- Plone 6.2 only (Python 3.10+), Plone 4 support dropped; package moved to the `src/` layout.
  [chris-adam]
- Skin layers removed: maintenance message on the `@@login` / `@@login_form` views (browser layer), new `uninstall` profile.
  [chris-adam]
- Send-to form captcha removed (collective.captcha dropped).
  [chris-adam]
- `simplify` profile: `simplify.css` is a bundle for Plone 6 markup, group and permissions set by a post handler.
  [chris-adam]
- Added unit and robot tests, Plone 6.2 buildout and GitHub Actions.
  [chris-adam]


4.3.15.1 (2020-02-25)
---------------------

- Validated for Plone 4.3.15.
  [gbastien]

4.3.8.1 (2017-05-17)
--------------------

- Adapted translation for 'label_by_author' from 'By {author}'
  to 'Created by ${author}'.
  [gbastien]


4.3.8 (2017-02-02)
------------------
- moved to Plone 4.3.8
  [gbastien]
- override the 'label_click_here_to_retrieve' translation to display a clear
  message on the link to retrieve password when lost
  [gbastien]

433 (unreleased)
----------------
- moved to Plone 4.3.3
  [gbastien]

432 (2014-02-12)
----------------
- moved to Plone 4.3.2
  [gbastien]

4 (2013-08-28)
--------------
- login_form overrides to display message when authentication plugins are deactivated
  [sgeulette]
- sendto_form overrides to integrate a captcha (collective.captcha)
  [gbastien]
