# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
__init__.py
"""
from .__about__ import (  # noqa
    __author__, __copyright__, __email__, __license__, __summary__, __title__,
    __uri__, __version__,
)

_about_exports = [
    "__author__", "__copyright__", "__email__", "__license__", "__summary__",
    "__title__", "__uri__", "__version__",
]

from etherflow_acitoolkit.acicounters import (  # noqa
    AtomicCounter, AtomicCountersOnGoing, AtomicNode, AtomicPath,
    InterfaceStats,
)
from etherflow_acitoolkit.aciHealthScore import HealthScore  # noqa
from etherflow_acitoolkit.aciFaults import (Faults)  # noqa
from etherflow_acitoolkit.aciSearch import AciSearch, Searchable  # noqa
from etherflow_acitoolkit.acisession import EventHandler, Login, Session, Subscriber, CredentialsError  # noqa
from etherflow_acitoolkit.aciTable import Table  # noqa
from etherflow_acitoolkit.acibaseobject import BaseACIObject, BaseRelation
from etherflow_acitoolkit.acitoolkit import (  # noqa
    AnyEPG, AppProfile, AttributeCriterion, BaseContract,
    BGPSession, BridgeDomain, CollectionPolicy,
    CommonEPG, Context, Contract, ContractInterface, ContractSubject, Endpoint,
    EPG, EPGDomain, FexInterface, Filter, FilterEntry, IPEndpoint, InputTerminal,
    L2ExtDomain, L2Interface, L3ExtDomain, L3Interface, LogicalModel, MonitorPolicy,
    MonitorStats, MonitorTarget, NetworkPool, OSPFInterface,
    OSPFInterfacePolicy, OSPFRouter, OutputTerminal, OutsideEPG,
    OutsideL2, OutsideL2EPG, OutsideL3, OutsideNetwork,
    PhysDomain, PortChannel, Search, Subnet, Taboo, Tenant, TunnelInterface,
    VMM, VMMCredentials, VmmDomain, VMMvSwitchInfo, Tag, _interface_from_dn
)
from etherflow_acitoolkit.acitoolkitlib import Credentials, AcitoolkitGraphBuilder  # noqa
from etherflow_acitoolkit.acifakeapic import FakeSession  # noqa
# Dependent on acitoolkit
from etherflow_acitoolkit.aciConcreteLib import (  # noqa
    ConcreteAccCtrlRule, ConcreteArp, ConcreteBD, ConcreteContext, ConcreteEp,
    ConcreteFilter, ConcreteFilterEntry, ConcreteLoopback, ConcreteOverlay,
    ConcretePortChannel, ConcreteSVI, ConcreteVpc, ConcreteVpcIf,
    ConcreteTunnel, ConcreteCdp
)
# Dependent on aciconcretelib
from etherflow_acitoolkit.aciphysobject import (  # noqa
    Cluster, ExternalSwitch, Fabric, Fan, Fantray, Interface, Linecard, Link,
    Node, PhysicalModel, Pod, Powersupply, Process, Supervisorcard,
    Systemcontroller, WorkingData,
)

import inspect as _inspect

__all__ = _about_exports + sorted(
    name for name, obj in locals().items()
    if not (name.startswith('_') or _inspect.ismodule(obj))
)
