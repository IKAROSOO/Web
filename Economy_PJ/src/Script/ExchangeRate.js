import Chart from "chart.js/auto";
import zoomPlugin from 'chartjs-plugin-zoom';

const card = document.querySelector('.chart-card');
const chartTitleElement = document.getElementById('chart-title');
const placeholder = document.querySelector('.placeholder-text');

// 차트 인스턴스를 저장할 변수 (새로 그릴 때 기존 차트를 삭제하기 위함)
let economicChart = null;

let customPeriod = {
    start: null,
    end: null
};

const currentIndicator = { id: "exchange-rate", title: "원/달러 환율" };

function getAdaptiveFontSize(text) {
    const len = text.length;
    if (len > 8) return "0.8rem";
    if (len > 5) return "0.95rem";
    return "1.1rem";
}

/**
 * Chart.js를 사용하여 그래프를 그리는 함수
 */
function renderChart(rawData) {
    const ctx = document.getElementById('indicator-chart').getContext('2d');
    
    // 1. 데이터 가공 (null 값 필터링 또는 0 처리 선택 가능)
    // 여기서는 null 데이터를 제외하고 날짜와 값만 추출합니다.
    const filteredData = rawData.filter(item => item.value !== null);
    const labels = filteredData.map(item => item.date);
    const values = filteredData.map(item => item.value);

    // 2. 기존 차트가 있다면 파괴 (중복 생성 방지)
    if (economicChart) {
        economicChart.destroy();
    }

    // 3. 차트 생성
    economicChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: currentIndicator.title,
                data: values,
                borderColor: '#1a237e',
                backgroundColor: 'rgba(26, 35, 126, 0.05)',
                borderWidth: 2,
                pointRadius: 0, // 점 숨기기 (선형 강조)
                hitRadius: 10,  // 호버 감지 범위
                fill: true,
                tension: 0.1    // 곡선 정도
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false } // 범례 숨김
            },
            scales: {
                x: {
                    display: true,
                    grid: { display: false }
                },
                y: {
                    beginAtZero: false, // 환율이므로 0부터 시작할 필요 없음
                    grid: { color: '#f0f0f0' }
                }
            }
        }
    });

    // 그래프가 그려지면 placeholder 숨기기
    if (placeholder) placeholder.style.display = 'none';
}

async function requestDatabyPeriod(indicatorId, startDate, endDate=null) {
    if (placeholder) {
        placeholder.style.display = 'block';
        placeholder.textContent = "데이터를 불러오는 중...";
    }

    try {
        const url = `/api/data?indicator=${indicatorId}&startDate=${startDate}&endDate=${endDate}`;
        const response = await fetch(url);
        if (!response.ok) throw new Error('네트워크 응답 없음');
        
        const result = await response.json();
        
        // 이미지에서 확인된 데이터 구조: result.data 가 배열임
        if (result.data && result.data.length > 0) {
            renderChart(result.data);
        } else {
            placeholder.textContent = "표시할 데이터가 없습니다.";
        }

    } catch (error) {
        console.error("오류 발생:", error);
        if (placeholder) placeholder.textContent = "데이터를 가져오지 못했습니다.";
    }
}

function openCustomPeriodUI() {
    const modal = document.getElementById("custom-period-modal");
    modal.classList.remove("hidden");

    modal.querySelector(".custom-period-confirm").onclick = () => {
        const start = document.getElementById("custom-start").value;
        const end = document.getElementById("custom-end").value;

        if (!start || !end) {
            alert("날짜를 모두 선택하세요.");
            return;
        }

        if (new Date(start) > new Date(end)) {
            alert("시작일이 종료일보다 늦습니다.");
            return;
        }

        modal.classList.add("hidden");

        const indicatorId = card.dataset.indicatorId;
        requestDatabyPeriod(indicatorId, start, end);
    };

    modal.querySelector(".custom-period-cancel").onclick = () => {
        modal.classList.add("hidden");
    };
}


function init() {
    chartTitleElement.textContent = currentIndicator.title;
    chartTitleElement.style.fontSize = getAdaptiveFontSize(currentIndicator.title);
    card.dataset.indicatorId = currentIndicator.id;

    const periodControls = document.querySelector('.period-controls');
    periodControls.addEventListener('click', (e) => {
        const periodBtn = e.target.closest('.btn-period');
        if (!periodBtn) return;

        const period = periodBtn.dataset.period;
        const indicatorId = card.dataset.indicatorId;

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