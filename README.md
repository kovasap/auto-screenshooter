auto-screenshooter
================

Automatically take screenshots on a regular cadence and upload them to Google
photos.

# Google Photos Setup

1. Obtain a Google Photos API key (Client ID and Client Secret) by following
   the instructions on [Getting started with Google Photos REST
   APIs](https://developers.google.com/photos/library/guides/get-started)
1. Replace YOUR_CLIENT_ID in the client_id_template.json file with the provided
   Client ID.
1. Replace YOUR_CLIENT_SECRET in the client_id_template.json file with the
   provided Client Secret.
1. Move the client_id_template.json file to
   `src/auto_screenshooter/client_id.json`

# Build

Make sure you have Python 3.7+ and `poetry` installed, then install with
`poetry install`.

To run, simply execute `auto-screenshooter`.
