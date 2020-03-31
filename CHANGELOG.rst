##########
Change log
##########

0.1.0 (2020-03-31)
==================

This is the first release of LTD Events:

- The ``/webhook`` HTTP endpoint (accessible only from within a Kubernetes cluster) accepts webhook paylads from `LTD Keeper <https://ltd-keeper.lsst.io>`__.
  Currently the webhook only accepts ``edition.updated`` events from LTD Keeper.

- LTD Events forwards ``edition.forwarded`` events to the ``ltd.events`` Kafka topic using the ``ltd.edition_update_v1`` Avro schema.
