import datetime
from typing import TYPE_CHECKING, List, Optional, Tuple

import pydantic

from classiq.interface.enum_utils import StrEnum


class Provider(StrEnum):
    """
    This class defines all Providers that Classiq supports.
    This is mainly used in backend_preferences when specifying where do we want to execute the defined model.
    """

    IBM_QUANTUM = "IBM Quantum"
    AZURE_QUANTUM = "Azure Quantum"
    AMAZON_BRAKET = "Amazon Braket"
    IONQ = "IonQ"
    CLASSIQ = "Classiq"
    GOOGLE = "Google"
    ALICE_AND_BOB = "Alice & Bob"
    OQC = "OQC"
    INTEL = "Intel"
    AQT = "AQT"

    @property
    def id(self) -> "ProviderIDEnum":
        return self.value.replace(" ", "-").lower()  # type: ignore[return-value]


ProviderIDEnum = StrEnum("ProviderIDEnum", {p.id: p.id for p in Provider})  # type: ignore[misc]


class AvailabilityStatus(StrEnum):
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"

    @property
    def is_available(self) -> bool:
        return self == self.AVAILABLE


class DeviceType(StrEnum):
    SIMULATOR = "simulator"
    HARDWARE = "hardware"
    STATEVECTOR = "state_vector_simulator"

    @property
    def is_simulator(self) -> bool:
        return self != self.HARDWARE


class HardwareStatus(pydantic.BaseModel):
    last_update_time: datetime.datetime = pydantic.Field(
        default_factory=lambda: datetime.datetime.now(tz=datetime.UTC)
    )
    availability: AvailabilityStatus
    queue_time: Optional[datetime.timedelta]
    pending_jobs: Optional[int]


if TYPE_CHECKING:
    ConnectivityMapEntry = Tuple[int, int]
else:
    ConnectivityMapEntry = List[int]


class HardwareInformation(pydantic.BaseModel):
    provider: Provider
    vendor: str
    name: str
    display_name: str
    device_type: DeviceType
    number_of_qubits: int
    connectivity_map: Optional[List[ConnectivityMapEntry]]
    basis_gates: List[str]
    status: HardwareStatus

    def is_simulator(self) -> bool:
        return self.device_type != DeviceType.HARDWARE
