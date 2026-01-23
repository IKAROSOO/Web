import {
    createChart,
    LineSeries,
    CandlestickSeries,
} from "lightweight-charts";

const chartCard = document.querySelector('.chart-card');
const chartContainer = document.querySelector('.chart-container');
const chartTitleElement = document.getElementById('chart-title');
const placeHolder = document.querySelector('.placeholder-text');

const currentIndicator = { id: "exchange-rate", title: "원/달러 환율"};

let economicChart = null;
let customPeriod = {
    start: null,
    end: null
}

function getAdaptiveFontSize(text) {
    const len = text.length;
    if (len > 8) return "0.8rem";
    if (len > 5) return "0.95rem";
    return "1.1rem";
}

/**
 * lightweight-charts라이브러리를 활용한 그래프 그리기
 */
function renderChart(data) {
    if (economicChart) {
        economicChart.remove();
        economicChart = null;
    }

    placeHolder.style.display = 'none';

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
        rightPriceScale: {
            borderColor: '#ccc',
        },
        timeScale: {
            borderColor: '#ccc',
        },
    });

    const series = economicChart.addSeries(LineSeries, {
        color: '#2962FF',
        lineWidth: 2,
    });

    const chartData = data
    .filter(item => item.value !== null && item.value !== ".")
    .map(item => ({
        time: item.date,
        value: Number(item.value)
    }));

    series.setData(chartData);

    requestAnimationFrame(() => {
        economicChart.timeScale().fitContent();
    });
}

async function requestDatabyPeriod(indicatorId, startDate, endDate=null) {
    if (placeHolder) {
        placeHolder.style.display = 'block';
        placeHolder.textContent = "데이터를 불러오는 중...";
    }

    try {
        const url = `/api/data?indicator=${indicatorId}&startDate=${startDate}&endDate=${endDate}`;
        const response = await fetch(url);

        if(!response.ok) {
            throw new Error('네트워크 응답 없음');
        }

        const result = await response.json();

        if (result.data&&result.data.length > 0) {
            renderChart(result.data);
        } else {
            placeHolder.textContent = "표시할 데이터가 없습니다.";
        }
    } catch (error) {
        console.error("오류 발생 : ", error);
        if (placeHolder)
            placeHolder.textContent = "데이터를 가져오지 못했습니다.";
    }
}

function openCustomPeriodUI() {
    const modal = document.getElementById("custom-period-modal");
    modal.classList.remove("hidden");

    modal.querySelector(".custom-period-confirm").onclick = () => {
        const start = document.getElementById("custom-start").value;
        const end = document.getElementById("custom-end").value;

        if (!start || !end) {
            alert("날짜를 모두 선택하세요");
            return;
        }

        if (new Date(start) > new Date(end)) {
            alert("시작일이 종료일보다 늦습니다");
            return;
        }

        modal.classList.add("hidden");

        const indicatorId = chartContainer.dataset.indicatorId;
        requestDatabyPeriod(indicatorId, start, end);
    };

    modal.querySelector(".custom-period-cancel").onclick = () => {
        modal.classList.add("hidden");
    };
}

function init() {
    chartTitleElement.textContent = currentIndicator.title;
    chartTitleElement.style.fontSize = getAdaptiveFontSize(currentIndicator.title);
    chartCard.dataset.indicatorId = currentIndicator.id;

    const periodControls = document.querySelector('.period-controls');
    periodControls.addEventListener('click', (e) => {
        const periodBtn = e.target.closest('.btn-period');
        if (!periodBtn) return;

        const period = periodBtn.dataset.period;
        const indicatorId = chartCard.dataset.indicatorId;

        const allBtns = periodControls.querySelectorAll('.btn-period');
        allBtns.forEach(btn => btn.classList.remove('active'));
        periodBtn.classList.add('active');

        if (period === "custom") {
            openCustomPeriodUI();
            return;
        }

        requestDatabyPeriod(indicatorId, period);
    });

    // 첫 로드 (1년치)
    requestDatabyPeriod(currentIndicator.id, "1y");
}

document.addEventListener('DOMContentLoaded', init);