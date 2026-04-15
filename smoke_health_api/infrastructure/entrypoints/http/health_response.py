from smoke_health_api.domain.models.health_report import HealthReport


def health_report_to_json_body(report: HealthReport) -> dict[str, str]:
    return {"status": report.status.value}
