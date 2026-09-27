import phonenumbers
from phonenumbers import carrier, geocoder, timezone as pn_tz, number_type
from tryreveal import logger


def scan_phone(target, cfg, db):
    logger.info(f"Phone: {target}")

    try:
        parsed = phonenumbers.parse(target, cfg.phone.default_region)
    except phonenumbers.NumberParseException as e:
        logger.error(f"Invalid number: {e}")
        return {"error": str(e), "total": 0, "confirmed": 0, "hits": []}

    result = {
        "target": target,
        "valid": phonenumbers.is_valid_number(parsed),
        "possible": phonenumbers.is_possible_number(parsed),
        "country_code": parsed.country_code,
        "region": phonenumbers.region_code_for_number(parsed) or "-",
        "region_name": geocoder.description_for_number(parsed, "en") or "-",
        "carrier": carrier.name_for_number(parsed, "en") or "-",
        "line_type": str(number_type(parsed)),
        "timezone": ", ".join(pn_tz.time_zones_for_number(parsed) or ["-"]),
        "e164": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164),
        "international": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
    }

    db.add_phone(result["e164"], result["region_name"], result["region"],
                 result["carrier"], result["line_type"])

    logger.success(f"Phone analyzed: {result['e164']}")
    for k, v in result.items():
        logger.debug(f"{k}: {v}")

    return {"total": 1, "confirmed": 1 if result["valid"] else 0, "hits": [result]}
