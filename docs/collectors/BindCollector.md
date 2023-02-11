<!--This file was generated from the python source
Please edit the source to make changes
-->
BindCollector
=====

Collects stats from bind 9.5's statistics server

#### Dependencies

 * [bind 9.5](http://www.isc.org/software/bind/new-features/9.5)
    configured with libxml2 and statistics-channels


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
host | localhost |  | str
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
port | 8080 |  | int
publish | resolver, server, zonemgmt, sockets, memory, | Available stats:<br>
 - resolver (Per-view resolver and cache statistics)<br>
 - server (Incoming requests and their answers)<br>
 - zonemgmt (Zone management requests/responses)<br>
 - sockets (Socket statistics)<br>
 - memory (Global memory usage)<br>
 | list
publish_view_bind | False |  | bool
publish_view_meta | False |  | bool
data_format | xml_v2 | Bind stats version:<br>
 - xml_v2 (Original bind stats version from 9.5)<br>
 - xml_v3 (New xml version)<br>
 - json_v1 (JSON replacement for XML)<br>
 | str

#### Example Output

```
servers.hostname.bind.nsstat.AuthQryRej 0.0
servers.hostname.bind.nsstat.QryAuthAns 0.0
servers.hostname.bind.nsstat.QryDropped 0.0
servers.hostname.bind.nsstat.QryDuplicate 0.0
servers.hostname.bind.nsstat.QryFORMERR 0.0
servers.hostname.bind.nsstat.QryFailure 0.0
servers.hostname.bind.nsstat.QryNXDOMAIN 0.0
servers.hostname.bind.nsstat.QryNoauthAns 0.0
servers.hostname.bind.nsstat.QryNxrrset 0.0
servers.hostname.bind.nsstat.QryRecursion 0.0
servers.hostname.bind.nsstat.QryReferral 0.0
servers.hostname.bind.nsstat.QrySERVFAIL 0.0
servers.hostname.bind.nsstat.QrySuccess 0.0
servers.hostname.bind.nsstat.RecQryRej 0.0
servers.hostname.bind.nsstat.ReqBadEDNSVer 0.0
servers.hostname.bind.nsstat.ReqBadSIG 0.0
servers.hostname.bind.nsstat.ReqEdns0 0.0
servers.hostname.bind.nsstat.ReqSIG0 0.0
servers.hostname.bind.nsstat.ReqTCP 0.0
servers.hostname.bind.nsstat.ReqTSIG 0.0
servers.hostname.bind.nsstat.Requestv4 0.0
servers.hostname.bind.nsstat.Requestv6 0.0
servers.hostname.bind.nsstat.RespEDNS0 0.0
servers.hostname.bind.nsstat.RespSIG0 0.0
servers.hostname.bind.nsstat.RespTSIG 0.0
servers.hostname.bind.nsstat.Response 0.0
servers.hostname.bind.nsstat.TruncatedResp 0.0
servers.hostname.bind.nsstat.UpdateBadPrereq 0.0
servers.hostname.bind.nsstat.UpdateDone 0.0
servers.hostname.bind.nsstat.UpdateFail 0.0
servers.hostname.bind.nsstat.UpdateFwdFail 0.0
servers.hostname.bind.nsstat.UpdateRej 0.0
servers.hostname.bind.nsstat.UpdateReqFwd 0.0
servers.hostname.bind.nsstat.UpdateRespFwd 0.0
servers.hostname.bind.nsstat.XfrRej 0.0
servers.hostname.bind.nsstat.XfrReqDone 0.0
servers.hostname.bind.queries.A 0.0
servers.hostname.bind.requests.QUERY 0.0
servers.hostname.bind.sockstat.FDWatchClose 0.0
servers.hostname.bind.sockstat.FDwatchConn 0.0
servers.hostname.bind.sockstat.FDwatchConnFail 0.0
servers.hostname.bind.sockstat.FDwatchRecvErr 0.0
servers.hostname.bind.sockstat.FDwatchSendErr 0.0
servers.hostname.bind.sockstat.FdwatchBindFail 0.0
servers.hostname.bind.sockstat.TCP4Accept 0.0
servers.hostname.bind.sockstat.TCP4AcceptFail 0.0
servers.hostname.bind.sockstat.TCP4BindFail 0.0
servers.hostname.bind.sockstat.TCP4Close 0.0
servers.hostname.bind.sockstat.TCP4Conn 0.0
servers.hostname.bind.sockstat.TCP4ConnFail 0.0
servers.hostname.bind.sockstat.TCP4Open 0.0
servers.hostname.bind.sockstat.TCP4OpenFail 0.0
servers.hostname.bind.sockstat.TCP4RecvErr 0.0
servers.hostname.bind.sockstat.TCP4SendErr 0.0
servers.hostname.bind.sockstat.TCP6Accept 0.0
servers.hostname.bind.sockstat.TCP6AcceptFail 0.0
servers.hostname.bind.sockstat.TCP6BindFail 0.0
servers.hostname.bind.sockstat.TCP6Close 0.0
servers.hostname.bind.sockstat.TCP6Conn 0.0
servers.hostname.bind.sockstat.TCP6ConnFail 0.0
servers.hostname.bind.sockstat.TCP6Open 0.0
servers.hostname.bind.sockstat.TCP6OpenFail 0.0
servers.hostname.bind.sockstat.TCP6RecvErr 0.0
servers.hostname.bind.sockstat.TCP6SendErr 0.0
servers.hostname.bind.sockstat.UDP4BindFail 0.0
servers.hostname.bind.sockstat.UDP4Close 0.0
servers.hostname.bind.sockstat.UDP4Conn 0.0
servers.hostname.bind.sockstat.UDP4ConnFail 0.0
servers.hostname.bind.sockstat.UDP4Open 0.0
servers.hostname.bind.sockstat.UDP4OpenFail 0.0
servers.hostname.bind.sockstat.UDP4RecvErr 0.0
servers.hostname.bind.sockstat.UDP4SendErr 0.0
servers.hostname.bind.sockstat.UDP6BindFail 0.0
servers.hostname.bind.sockstat.UDP6Close 0.0
servers.hostname.bind.sockstat.UDP6Conn 0.0
servers.hostname.bind.sockstat.UDP6ConnFail 0.0
servers.hostname.bind.sockstat.UDP6Open 0.0
servers.hostname.bind.sockstat.UDP6OpenFail 0.0
servers.hostname.bind.sockstat.UDP6RecvErr 0.0
servers.hostname.bind.sockstat.UDP6SendErr 0.0
servers.hostname.bind.sockstat.UnixAccept 0.0
servers.hostname.bind.sockstat.UnixAcceptFail 0.0
servers.hostname.bind.sockstat.UnixBindFail 0.0
servers.hostname.bind.sockstat.UnixClose 0.0
servers.hostname.bind.sockstat.UnixConn 0.0
servers.hostname.bind.sockstat.UnixConnFail 0.0
servers.hostname.bind.sockstat.UnixOpen 0.0
servers.hostname.bind.sockstat.UnixOpenFail 0.0
servers.hostname.bind.sockstat.UnixRecvErr 0.0
servers.hostname.bind.sockstat.UnixSendErr 0.0
servers.hostname.bind.view._default.resstat.EDNS0Fail 0.0
servers.hostname.bind.view._default.resstat.FORMERR 0.0
servers.hostname.bind.view._default.resstat.GlueFetchv4 0.0
servers.hostname.bind.view._default.resstat.GlueFetchv4Fail 0.0
servers.hostname.bind.view._default.resstat.GlueFetchv6 0.0
servers.hostname.bind.view._default.resstat.GlueFetchv6Fail 0.0
servers.hostname.bind.view._default.resstat.Lame 0.0
servers.hostname.bind.view._default.resstat.Mismatch 0.0
servers.hostname.bind.view._default.resstat.NXDOMAIN 0.0
servers.hostname.bind.view._default.resstat.OtherError 0.0
servers.hostname.bind.view._default.resstat.QryRTT10 0.0
servers.hostname.bind.view._default.resstat.QryRTT100 0.0
servers.hostname.bind.view._default.resstat.QryRTT1600 0.0
servers.hostname.bind.view._default.resstat.QryRTT1600+ 0.0
servers.hostname.bind.view._default.resstat.QryRTT500 0.0
servers.hostname.bind.view._default.resstat.QryRTT800 0.0
servers.hostname.bind.view._default.resstat.QueryAbort 0.0
servers.hostname.bind.view._default.resstat.QuerySockFail 0.0
servers.hostname.bind.view._default.resstat.QueryTimeout 0.0
servers.hostname.bind.view._default.resstat.Queryv4 0.0
servers.hostname.bind.view._default.resstat.Queryv6 0.0
servers.hostname.bind.view._default.resstat.Responsev4 0.0
servers.hostname.bind.view._default.resstat.Responsev6 0.0
servers.hostname.bind.view._default.resstat.Retry 0.0
servers.hostname.bind.view._default.resstat.SERVFAIL 0.0
servers.hostname.bind.view._default.resstat.Truncated 0.0
servers.hostname.bind.view._default.resstat.ValAttempt 0.0
servers.hostname.bind.view._default.resstat.ValFail 0.0
servers.hostname.bind.view._default.resstat.ValNegOk 0.0
servers.hostname.bind.view._default.resstat.ValOk 0.0
servers.hostname.bind.zonestat.AXFRReqv4 0.0
servers.hostname.bind.zonestat.AXFRReqv6 0.0
servers.hostname.bind.zonestat.IXFRReqv4 0.0
servers.hostname.bind.zonestat.IXFRReqv6 0.0
servers.hostname.bind.zonestat.NotifyInv4 0.0
servers.hostname.bind.zonestat.NotifyInv6 0.0
servers.hostname.bind.zonestat.NotifyOutv4 0.0
servers.hostname.bind.zonestat.NotifyOutv6 0.0
servers.hostname.bind.zonestat.NotifyRej 0.0
servers.hostname.bind.zonestat.SOAOutv4 0.0
servers.hostname.bind.zonestat.SOAOutv6 0.0
servers.hostname.bind.zonestat.XfrFail 0.0
servers.hostname.bind.zonestat.XfrSuccess 0.0
```

