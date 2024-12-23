# CORDEX-AWS

[![Open In Studio Lab](https://studiolab.sagemaker.aws/studiolab.svg)](https://studiolab.sagemaker.aws/import/github/euro-cordex/cordex-aws/blob/master/notebooks/catalog.ipynb)

Manage Open Data Sponsorhip.

## How this works

This repository contains the front end workflow to extract CORDEX data from ESGF and upload it to the [EURO-CORDEX S3 bucket on AWS](https://registry.opendata.aws/euro-cordex). The workflow utilizes the [pangeo-forge-cordex](https://github.com/euro-cordex/pangeo-forge-cordex) package for accessing the [ESGF API](https://esgf.github.io/esg-search/ESGF_Search_RESTful_API.html) and prepares the input for extracting and converting datasets using [pangeo-forge-recipes](https://github.com/pangeo-forge/pangeo-forge-recipes).

See also [this discussion](https://github.com/orgs/WCRP-CORDEX/discussions/5).

## Examples

See [AWS-Access notebook](https://wcrp-cordex.github.io/cordex-tutorials/aws-access.html).

## Attribution

We thank the awesome [AWS Open Data Sponsorship Program](https://aws.amazon.com/de/opendata/open-data-sponsorship-program/) for supporting the
storage and distribution of our EURO-CORDEX datasets! :rocket:
