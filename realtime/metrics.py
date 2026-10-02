def percentile(values, p):
    if not values: return None
    values=sorted(values); index=(len(values)-1)*p/100; lower=int(index); upper=min(lower+1,len(values)-1); return values[lower]+(values[upper]-values[lower])*(index-lower)
def latency_report(events):
    keys=("asr_ms","signal_ms","nudge_ms","delivery_ms","end_to_end_ms")
    return {k:{"sample_count":len(events),"p50":percentile([e[k] for e in events],50),"p95":percentile([e[k] for e in events],95)} for k in keys}
