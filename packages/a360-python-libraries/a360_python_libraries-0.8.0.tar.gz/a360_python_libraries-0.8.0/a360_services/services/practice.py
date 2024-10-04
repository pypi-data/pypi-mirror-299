import uuid

from a360_services.utils.service_provider import ServiceProvider
from a360_services.utils.services_list import Services


class PracticeService:
    def __init__(self, service_provider: ServiceProvider):
        self.service_provider = service_provider

    def get_expert(self, expert_id: uuid.UUID) -> dict:
        request_path = f"/experts/{str(expert_id)}"
        return self.service_provider.fetch_data(
            service=Services.dict,
            request_path=request_path
        )
