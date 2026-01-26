import {
    createChart,
    LineSeries,
    CandlestickSeries,
} from "lightweight-charts";

/* ===== DOM ===== */
const chartCard = document.querySelector('.chart-card');
const chartContainer = chartCard.querySelector('.chart-container-target');
const loadingOverlay = chartCard.querySelector('.loading-overlay');

let economicChart = null;
let resizeObserver = null;

/* ===== 차트 렌더 ===== */
function renderChart(data) {
    if (economicChart) {
        economicChart.remove();
        if (resizeObserver) resizeObserver.disconnect();
    }

    loadingOverlay.classList.add('hidden');

    economicChart = createChart(chartContainer, {
        localization: {
            /* ===== 기존의 DD-MM-YY로 나오는 것을 YY-MM-DD로 변형 ===== */
            timeFormatter: (time) => {
                // console.log(time, typeof(time)); -> time의 형과 형태 확인용

                const [yyyy, mm, dd] = time.split('-');
                return `${yyyy.slice(2)}-${mm}-${dd}`;
            }
        },
        /* ===== 부모 컨테이너의 실제 크기를 반영 ===== */
        width: chartContainer.clientWidth,
        height: chartContainer.clientHeight,
        layout: {
            textColor: '#333',
            background: { color: '#ffffff' },
        },
        grid: {
            vertLines: { color: '#eee' },
            horzLines: { color: '#eee' },
        },
        rightPriceScale: { borderColor: '#ccc' },
        timeScale: {
            borderColor: '#ccc',
            fixLeftEdge: true,
            fixRightEdge: true,
            lockVisibleTimeRangeOnResize: true,
        },
    });

    const series = economicChart.addSeries(LineSeries, {
        color: '#2962FF',
        lineWidth: 2,
    });

    /* ===== 컨테이너의 크기가 변할 시 차트크기 자동 업데이트 ===== */
    const resizeObserver = new ResizeObserver(entries => {
        if (!resizeObserver) return;
        
        for (let entry of entries) {
            const {width, height} = entry.contentRect;
            economicChart.applyOptions({
                width: width,
                height: height
            });
        }
    });
    resizeObserver.observe(chartContainer);

    const chartData = data
        .filter(item => item.value !== null && item.value !== ".")
        .map(item => ({
            time: item.date,
            value: Number(item.value),
        }));

    series.setData(chartData);

    requestAnimationFrame(() => {
        economicChart.timeScale().fitContent();
    });
}

/* ===== 데이터 요청 (기존 로직 유지) ===== */
export async function requestExchangeDatabyPeriod(indicatorId, startDate, card, endDate = null) {
    loadingOverlay.classList.remove('hidden');
    loadingOverlay.textContent = "데이터를 불러오는 중...";

    try {
        const url = `/api/data?indicator=${indicatorId}&startDate=${startDate}&endDate=${endDate}`;
        const response = await fetch(url);

        if (!response.ok) throw new Error("네트워크 오류");

        const result = await response.json();

        if (result.data && result.data.length > 0) {
            renderChart(result.data);
        } else {
            loadingOverlay.textContent = "표시할 데이터가 없습니다.";
        }
    } catch (err) {
        console.error(err);
        loadingOverlay.textContent = "데이터를 가져오지 못했습니다.";
    }
}