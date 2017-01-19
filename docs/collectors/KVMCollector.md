<!--This file was generated from the python source
Please edit the source to make changes
-->
KVMCollector
=====

Collects /sys/kernel/debug/kvm/*

#### Dependencies

 * /sys/kernel/debug/kvm


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType

#### Example Output

```
servers.hostname.kvm.efer_reload 0.0
servers.hostname.kvm.exits 1436135848.0
servers.hostname.kvm.fpu_reload 121764903.5
servers.hostname.kvm.halt_exits 544586282.6
servers.hostname.kvm.halt_wakeup 235093451.4
servers.hostname.kvm.host_state_reload 801854250.6
servers.hostname.kvm.hypercalls 0.0
servers.hostname.kvm.insn_emulation 1314391264.7
servers.hostname.kvm.insn_emulation_fail 0.0
servers.hostname.kvm.invlpg 0.0
servers.hostname.kvm.io_exits 248822813.2
servers.hostname.kvm.irq_exits 701647108.4
servers.hostname.kvm.irq_injections 986654069.6
servers.hostname.kvm.irq_window 162240965.2
servers.hostname.kvm.largepages 351789.4
servers.hostname.kvm.mmio_exits 20169.4
servers.hostname.kvm.mmu_cache_miss 1643.3
servers.hostname.kvm.mmu_flooded 0.0
servers.hostname.kvm.mmu_pde_zapped 0.0
servers.hostname.kvm.mmu_pte_updated 0.0
servers.hostname.kvm.mmu_pte_write 11144.0
servers.hostname.kvm.mmu_recycled 0.0
servers.hostname.kvm.mmu_shadow_zapped 384.7
servers.hostname.kvm.mmu_unsync 0.0
servers.hostname.kvm.nmi_injections 0.0
servers.hostname.kvm.nmi_window 0.0
servers.hostname.kvm.pf_fixed 355636.1
servers.hostname.kvm.pf_guest 0.0
servers.hostname.kvm.remote_tlb_flush 111.2
servers.hostname.kvm.request_irq 0.0
servers.hostname.kvm.signal_exits 0.0
servers.hostname.kvm.tlb_flush 0.0
```

