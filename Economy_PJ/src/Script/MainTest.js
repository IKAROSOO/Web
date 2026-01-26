import { requestExchangeDatabyPeriod } from "./CardAddTest";

const container = document.querySelector('.dashboard-container');
const dashboardContainer = document.querySelector('.dashboard-container');
const modal = document.getElementById('custom-period-modal');
const overlay = document.getElementById('modal-overlay');
const templateCard = document.querySelector('.chart-card.template');
const addNewCard = document.getElementById("add-new-chart");

/**
 * 1. UI 레이아웃 업데이트
 * 카드의 개수에 따라 CSS클래스를 변경하여 그리드 조정
 */
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

/**
 * 2. Modal 제어
 */
const setModalVisibility = (isVisible) => {
    modal?.classList.toggle('hidden', !isVisible);
    overlay?.classList.toggle('hidden', !isVisible);
}

/**
 * 3. 커스텀 기간 설정 로직
 */
function handleCustomPeriod(card, indicatorId) {
    setModalVisibility(true);

    const confirmBtn = modal.querySelector('.custom-period-confirm');
    const cancelBtn = modal.querySelector('.custom-period-cancel');

    confirmBtn.onclick = () => {
        const start = document.getElementById("custom-start").value;
        const end = document.getElementById("custom-end").value;

        if (!start || !end) return alert("날짜를 모두 선택하세요");
        if (new Date(start) > new Date(end)) return alert("날짜 범위 오류");

        setModalVisibility(false);
        requestExchangeDatabyPeriod(indicatorId, start, card, end);
    };
    cancelBtn.onclick = () => setModalVisibility(false);
    overlay.onclick = () => setModalVisibility(false);
}

/**
 * 4. 고정 기간 설정 로직
 */
function handleFixedPeriod(card, indicatorId, period) {
    requestExchangeDatabyPeriod(indicatorId, period, card);
}


/**
 * 5. 통합 이벤트 리스너(이벤트 위임)
 */
container.addEventListener('click', (e) => {
    const periodBtn = e.target.closest('.btn-period');
    if (!periodBtn) return;

    const card = periodBtn.closest('.chart-card');
    const indicatorId = card.dataset.chartId; // HTML의 data-chart-id 속성 사용
    const period = periodBtn.dataset.period;

    // UI 피드백: 활성 버튼 표시
    card.querySelectorAll('.btn-period').forEach(btn => btn.classList.remove('active'));
    periodBtn.classList.add('active');

    if (period === 'custom') {
        handleCustomPeriod(card, indicatorId);
    } else {
        // 차트 모듈에 데이터 요청 위임
        requestExchangeDatabyPeriod(indicatorId, period, card);
    }
});

/**
 * 새 카드 추가
 */
addNewCard.addEventListener('click', () => {
    const indicatorId = `exchange-${Date.now()}`;
    
    const card = templateCard.cloneNode(true);
    card.classList.remove('template', 'hidden');
    card.dataset.indicatorId = indicatorId;

    dashboardContainer.insertBefore(card, addNewCard);

    updateDashboardLayout();
    requestExchangeDatabyPeriod(indicatorId, "1y", card);
})


/**
 * 6. 초기화 실행
 */
const init = () => {
    updateDashboardLayout();

    // 초기 로드 시 존재하는 모든 카드에 대해 데이터 요청
    const initialCards = container.querySelectorAll('.chart-card');
    initialCards.forEach(card => {
        const id = card.dataset.indicatorId;
        if (id) requestExchangeDatabyPeriod(id, "1y", card);
    });
};

// DOM 로드 완료 후 실행
init();