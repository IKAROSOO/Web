from google.cloud import monitoring_v3
import Monitoring_Test_00 as monitoring
import os

using_API = {
    'generativelanguage.googleapis.com' : 1500,
    'vision.googleapis.com' : 1000
}

project_name = monitoring.project_name
now = monitoring.now
month_start = monitoring.start_of_month

monitoring_client = monitoring.client

interval = monitoring_v3.TimeInterval(
    {
        "end_time" : {"seconds": int(now)},
        "start_time" : {"seconds": int(month_start.timestamp())},
    }
)

results = monitoring_client.list_time_series(
    request={
        "name": project_name,
        "filter": 'metric.type = "serviceruntime.googleapis.com/api/request_count"',
        "interval": interval,
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        "aggregation": {
            "alignment_period": {"seconds": 86400 * 30},
            "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_SUM,
            "cross_series_reducer": monitoring_v3.Aggregation.Reducer.REDUCE_SUM,
            "group_by_fields": ["resource.label.service"],
        },
    }
)

api_usage = {}
for page in results.pages:
    for series in page.time_series:
        service_name = series.resource.labels["service"]
        if series.points:
            cnt = series.points[0].value.int64_value
            api_usage[service_name] = cnt
    if not api_usage:
        print("이번 달에 집계된 API 사용량이 없습니다.")
    else:
        sorted_usage = sorted(api_usage.items(), key=lambda item: item[1], reverse=True)
        for service, cnt in sorted_usage:
            if service in using_API:
                using_API[service] -= cnt
                print(f"{service}: {using_API[service]}회 사용가능")

