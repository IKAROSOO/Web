import {
    createChart,
    LineSeries,
    CandlestickSeries,
} from "lightweight-charts";

/* ===== DOM ===== */
const chartCard = document.querySelector('.chart-card');
const chartContainer = chartCard.querySelector('.chart-container-target');
const chartTitleElement = chartCard.querySelector('.chart-title');
const loadingOverlay = chartCard.querySelector('.loading-overlay');
const periodControls = chartCard.querySelector('.period-controls');

/* ===== 상태 ===== */
const currentIndicator = {
    id: chartCard.dataset.chartId, // HTML 기준
    title: chartTitleElement.textContent,
};

let economicChart = null;

/* ===== 차트 렌더 ===== */
function renderChart(data) {
    if (economicChart) {
        economicChart.remove();
        economicChart = null;
    }

    loadingOverlay.classList.add('hidden');

    economicChart = createChart(chartContainer, {
        width: chartContainer.clientWidth,
        height: 350,
        layout: {
            textColor: '#333',
            background: { color: '#ffffff' },
        },
        grid: {
            vertLines: { color: '#eee' },
            horzLines: { color: '#eee' },
        },
        rightPriceScale: { borderColor: '#ccc' },
        timeScale: { borderColor: '#ccc' },
    });

    const series = economicChart.addSeries(LineSeries, {
        color: '#2962FF',
        lineWidth: 2,
    });

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
async function requestDatabyPeriod(indicatorId, startDate, endDate = null) {
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

/* ===== 기간 버튼 ===== */
periodControls.addEventListener('click', (e) => {
    const btn = e.target.closest('.btn-period');
    if (!btn) return;

    periodControls.querySelectorAll('.btn-period')
        .forEach(b => b.classList.remove('active'));
    btn.classList.add('active');

    const period = btn.dataset.period;

    if (period === "custom") {
        openCustomPeriodUI();
        return;
    }

    requestDatabyPeriod(currentIndicator.id, period);
});

/* ===== 커스텀 기간 ===== */
function openCustomPeriodUI() {
    const modal = document.getElementById("custom-period-modal");
    modal.classList.remove("hidden");

    modal.querySelector(".custom-period-confirm").onclick = () => {
        const start = document.getElementById("custom-start").value;
        const end = document.getElementById("custom-end").value;

        if (!start || !end) return alert("날짜를 모두 선택하세요");
        if (new Date(start) > new Date(end)) return alert("날짜 범위 오류");

        modal.classList.add("hidden");
        requestDatabyPeriod(currentIndicator.id, start, end);
    };

    modal.querySelector(".custom-period-cancel").onclick = () => {
        modal.classList.add("hidden");
    };
}

/* ===== 초기 로드 ===== */
requestDatabyPeriod(currentIndicator.id, "1y");
