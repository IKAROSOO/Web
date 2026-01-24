import os
import time
from datetime import datetime
from google.cloud import monitoring_v3

'''
구글 API의 사용횟수를 알 수 있는 코드
무료사용량을 초과하지 않도록 추적할 수 있게 해준다.
'''

PROJECT_ID = "gen-lang-client-0420119918"

file_path = os.path.dirname(os.path.abspath(__file__))
script_path = os.path.dirname(file_path)
CONFIG_PATH = os.path.join(script_path, 'CloudVision_config.json')

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CONFIG_PATH

client = monitoring_v3.MetricServiceClient()
project_name = f"projects/{PROJECT_ID}"

now = time.time()
start_of_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

def main():

    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": int(now)},
            "start_time": {"seconds": int(start_of_month.timestamp())},
        }
    )

    results = client.list_time_series(
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

    print(f"--- {start_of_month.strftime('%Y년 %m월')} API 호출 횟수 (JSON 키 인증) ---")

    api_usage = {}
    for page in results.pages:
        for series in page.time_series:
            service_name = series.resource.labels["service"]
            if series.points:
                count = series.points[0].value.int64_value
                api_usage[service_name] = count

    if not api_usage:
        print("이번 달에 집계된 API 사용량이 없습니다.")
    else:
        sorted_usage = sorted(api_usage.items(), key=lambda item: item[1], reverse=True)
        for service, count in sorted_usage:
            print(f"{service}: {count} 회")

if __name__ == "__main__":
    main()