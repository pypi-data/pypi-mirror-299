import ipaddress
import re

import pynetbox
import requests
from loguru import logger

from netbox_negistry_importer.config import settings


class Negistry:
    def __init__(self):
        self.data = self._get_negistry_data()
        self.pynetbox = pynetbox.api(url=settings.NETBOX_INSTANCE_URL, token=settings.NETBOX_API_TOKEN)

    def _get_negistry_data(self):
        """Fetch Negistry RIPE CESNET IP ranges from the external service."""
        try:
            logger.info("Fetching Negistry data from external service.")
            url = settings.NEGISTRY_URL
            response = requests.get(url)
            response.raise_for_status()
            logger.info("Successfully retrieved Negistry data.")
            return response.json()
        except requests.RequestException as e:
            self._handle_error(e, "Failed to retrieve Negistry data. Exiting...")

    def _handle_error(self, exception, message):
        """Logs the exception and exits the program."""
        logger.exception(exception)
        logger.error(message)
        exit()

    def _get_negistry_tag(self):
        """Retrieve the 'negistry' tag from Netbox."""
        try:
            logger.info("Loading 'negistry' tag from Netbox.")
            tag = self.pynetbox.extras.tags.get(name="negistry")
            if not tag:
                logger.error("Negistry tag does not exist.")
                raise ValueError("Negistry tag does not exist")
            logger.info("Successfully retrieved 'negistry' tag.")
            return tag
        except Exception as e:
            self._handle_error(e, "Unable to retrieve 'negistry' tag from Netbox.")

    def _get_existing_prefixes(self, tag):
        """Fetch existing Negistry prefixes from Netbox based on the 'negistry' tag."""
        try:
            logger.info("Loading existing Negistry prefixes from Netbox.")
            prefixes = {
                nb_prefix.prefix: nb_prefix
                for nb_prefix in self.pynetbox.ipam.prefixes.filter(status="container", tag=tag.name)
            }
            logger.info(f"Loaded {len(prefixes)} existing prefixes with the 'negistry' tag.")
            return prefixes
        except Exception as e:
            self._handle_error(e, "Unable to retrieve prefixes from Netbox.")

    def _get_tenants(self):
        """Fetch existing tenants from Netbox."""
        try:
            logger.info("Loading existing tenants from Netbox.")
            tenants = {tenant.custom_fields["client_id"]: tenant for tenant in self.pynetbox.tenancy.tenants.all()}
            logger.info(f"Loaded {len(tenants)} tenants from Netbox.")
            return tenants
        except Exception as e:
            self._handle_error(e, "Unable to retrieve tenants from Netbox.")

    @staticmethod
    def _get_ipv4_subnets(start, end):
        """Generate summarized IPv4 subnets from a start and end IP address."""
        try:
            logger.info(f"Summarizing IPv4 address range from {start} to {end}.")
            start_ip = ipaddress.IPv4Address(start)
            end_ip = ipaddress.IPv4Address(end)
            subnets = list(ipaddress.summarize_address_range(start_ip, end_ip))
            logger.info(f"Summarized into {len(subnets)} subnets.")
            return subnets
        except ValueError as e:
            logger.exception(e)
            logger.error(f"Invalid IPv4 range: {start} - {end}. Exiting...")
            exit()

    def import_as_prefixes(self):
        """Import IP prefixes from Negistry data into Netbox."""
        logger.info("Starting prefix import process.")
        negistry_tag = self._get_negistry_tag()
        negistry_prefixes = self._get_existing_prefixes(negistry_tag)
        tenants_dict = self._get_tenants()

        for negistry_range, data in self.data.items():
            if negistry_range == "__negistry_about__":
                logger.debug(f"Skipping metadata: {negistry_range}")
                continue

            logger.debug(f"Processing range: {negistry_range} with data: {data}")

            if data.get("ip4_start"):
                logger.info(f"Processing IPv4 range: {negistry_range}.")
                self._process_ipv4_range(negistry_range, data, negistry_prefixes, tenants_dict, negistry_tag)
            elif data.get("ip6_addr"):
                logger.info(f"Processing IPv6 range: {negistry_range}.")
                self._process_ipv6_range(negistry_range, data, negistry_prefixes, tenants_dict, negistry_tag)

        # Delete prefixes not present in the new data
        logger.info("Starting deletion of unused prefixes.")
        self._delete_unused_prefixes(negistry_prefixes)
        logger.info("Prefix import process completed.")

    def _process_ipv4_range(self, negistry_range, data, negistry_prefixes, tenants_dict, negistry_tag):
        """Process and import IPv4 ranges as prefixes."""
        ipv4_subnets = self._get_ipv4_subnets(data["ip4_start"], data["ip4_end"])
        for prefix in ipv4_subnets:
            prefix_str = str(prefix)
            nb_prefix = negistry_prefixes.pop(prefix_str, None)
            self._create_or_update_prefix(prefix_str, data, negistry_range, nb_prefix, tenants_dict, negistry_tag)

    def _process_ipv6_range(self, negistry_range, data, negistry_prefixes, tenants_dict, negistry_tag):
        """Process and import IPv6 ranges as prefixes."""
        prefix = f"{data['ip6_addr']}/{data['ip6_prefix']}"
        nb_prefix = negistry_prefixes.pop(prefix, None)
        self._create_or_update_prefix(prefix, data, negistry_range, nb_prefix, tenants_dict, negistry_tag)

    def _create_or_update_prefix(self, prefix, data, negistry_range, nb_prefix, tenants_dict, negistry_tag):
        """Create or update a prefix in Netbox."""
        tenant = tenants_dict.get(data.get("client_id"), None)
        descr = (" | ").join(data["descr"]) if data.get("descr") else ""

        if nb_prefix:
            logger.info(f"Updating existing prefix: {prefix}.")
            self._update_existing_prefix(nb_prefix, tenant, descr, data, negistry_range)
        else:
            logger.info(f"Creating new prefix: {prefix}.")
            self._create_new_prefix(prefix, tenant, descr, data, negistry_range, negistry_tag)

    def _update_existing_prefix(self, nb_prefix, tenant, description, data, negistry_range):
        """Update an existing prefix in Netbox."""
        nb_prefix.tenant = tenant
        nb_prefix.description = description
        nb_prefix.is_pool = True
        nb_prefix["custom_fields"]["netname"] = data.get("netname")
        nb_prefix["custom_fields"]["client_id"] = data.get("client_id")
        nb_prefix["custom_fields"]["negistry_primary_key"] = negistry_range

        if nb_prefix.save():
            logger.info(f"Successfully updated prefix: {nb_prefix.prefix}, id: {nb_prefix.id}")
        else:
            logger.debug(f"No changes needed for prefix: {nb_prefix.prefix}, id: {nb_prefix.id}")

    def _create_new_prefix(self, prefix, tenant, description, data, negistry_range, negistry_tag):
        """Create a new prefix in Netbox."""
        params = {
            "prefix": prefix,
            "status": "container",
            "description": description,
            "custom_fields": {
                "client_id": data.get("client_id"),
                "negistry_primary_key": negistry_range,
                "netname": data.get("netname"),
            },
            "tags": [negistry_tag.id],
            "tenant": tenant.id if tenant else None,
            "is_pool": True,
        }

        try:
            logger.info(f"Creating new prefix: {prefix}.")
            self.pynetbox.ipam.prefixes.create(params)
            logger.info(f"Successfully created new prefix: {prefix}.")
        except pynetbox.core.query.RequestError as e:
            logger.error(f"Failed to create prefix: {prefix}. Handling conflict.")
            self._handle_existing_prefix_conflict(e, prefix, data, tenant, description, negistry_tag)

    def _handle_existing_prefix_conflict(self, error, prefix, data, tenant, description, negistry_tag):
        """Handle cases where the prefix already exists in Netbox."""
        pattern = r"Prefix ((\d{1,3}\.){3}\d{1,3}\/\d{1,2}|[a-fA-F0-9:]+\/\d{1,3}) with vrf: None already exists!"
        if re.search(pattern, error.message):
            logger.warning(f"Prefix {prefix} already exists in Netbox. Attempting to update the existing record.")
            nb_prefix = self.pynetbox.ipam.prefixes.get(prefix=prefix, vrf=None)
            if not nb_prefix:
                logger.critical(f"Prefix {prefix} not found in Netbox after conflict.")
                raise error
            nb_prefix.tags.append(negistry_tag.id)
            nb_prefix.custom_fields.update(
                {
                    "client_id": data.get("client_id"),
                    "negistry_primary_key": data.get("negistry_primary_key"),
                    "netname": data.get("netname"),
                }
            )
            nb_prefix.update(
                {
                    "status": "container",
                    "description": description,
                    "tenant": tenant.id if tenant else None,
                    "is_pool": True,
                }
            )
            logger.info(f"Successfully updated conflicted prefix: {prefix}, id: {nb_prefix.id}")
        else:
            logger.critical(f"Unknown error occurred: {error}")
            raise error

    def _delete_unused_prefixes(self, negistry_prefixes):
        """Delete prefixes in Netbox that are no longer in the Negistry data."""
        try:
            for prefix, nb_prefix in negistry_prefixes.items():
                logger.info(f"Deleting unused prefix: {prefix}, id: {nb_prefix.id}")
                nb_prefix.delete()
                logger.info(f"Successfully deleted prefix: {prefix}.")
        except Exception as e:
            self._handle_error(e, "Unable to delete old prefixes from Netbox.")
