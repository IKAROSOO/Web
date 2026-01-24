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
const addChartBtn = document.getElementById('add-new-chart');
const dashboardContainer = document.querySelector('.dashboard-container');

/* ===== 상태 ===== */
const currentIndicator = {
    id: chartCard.dataset.chartId, // HTML 기준
    title: chartTitleElement.textContent,
};

let economicChart = null;

addChartBtn.addEventListener('click', () => {
    alert('새로운 경제지표 추가');
});

function updateDashboardLayout() {
    const chartCards = dashboardContainer.querySelectorAll('.chart-card');

    dashboardContainer.classList.remove('single', 'odd', 'even');

    if (chartCards.length === 1) {
        dashboardContainer.classList.add('single');
    } else if (chartCards.length % 2 === 0) {
        dashboardContainer.classList.add('even');
    } else {
        dashboardContainer.classList.add('odd');
    }
}

/* ===== 차트 렌더 ===== */
function renderChart(data) {
    if (economicChart) {
        economicChart.remove();
        economicChart = null;
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

/* ===== 기간설정 버튼 클릭시 배경 블러처리 및 상호작용 방지 ===== */
function openPeriodModal() {
    document.getElementById('custom-period-modal').classList.remove('hidden');
    document.getElementById('modal-overlay').classList.remove('hidden');
}

/* ===== 기간설정 완료시 원상복구 ===== */
function closePeriodModal() {
    document.getElementById('custom-period-modal').classList.add('hidden');
    document.getElementById('modal-overlay').classList.add('hidden');
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
    openPeriodModal();

    const modal = document.getElementById("custom-period-modal");
    const overlay = document.getElementById("modal-overlay");
    modal.classList.remove("hidden");

    modal.querySelector(".custom-period-confirm").onclick = () => {
        const start = document.getElementById("custom-start").value;
        const end = document.getElementById("custom-end").value;

        if (!start || !end) return alert("날짜를 모두 선택하세요");
        if (new Date(start) > new Date(end)) return alert("날짜 범위 오류");

        closePeriodModal();
        requestDatabyPeriod(currentIndicator.id, start, end);
    };

    modal.querySelector(".custom-period-cancel").onclick = () => {
        closePeriodModal();
    };

    overlay.onclick = () => {
        closePeriodModal();
    }
}

/* ===== 초기 로드 ===== */
requestDatabyPeriod(currentIndicator.id, "1y");
updateDashboardLayout();
