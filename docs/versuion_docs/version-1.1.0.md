# `Version 1.1.0`

## Design Summary

In this version I just added the static pages for the meta and legal information about the site. Such as the terms and agreements, community rules, policy pages ... etc.

## Frontend Updates

At this point there is no libraries or any other frontend framework implemented in the site. It uses vanilla html, css, javascript and uses Django template engine to display the data not JSON API format:

Newly Additions to the template folder:
- Template and Static directories named `about`
  - about page
  - community rules page
  - privacy policy page
  - terms and agreements page
- Added a landing_page base template for the about pages to extends from

## Backend Updates

I haven't added any logic behind them they are just empty views rendering templates. There isn't even any models implemented because there is no need at the moment.

- `about` app new views:
  - About page (`about`) -- url path (`about/`)
  - Community Rules page (`about_community_rules`) -- url path(`about/communityrules/`)
  - Terms and Agreements page (`about_terms`) -- url path(`about/terms`/)
  - Privacy Policy(`about_privacy`) -- url path(`about/privacypolicy/`)

## DevOps Updates

At this version I haven't implemented anything regarding DevOps.

## Mobile Updates

At this version I haven't implemented anything regarding mobile.

## Security

I just scanned it with OWASP zap, I havent implemented anything at the moment.
