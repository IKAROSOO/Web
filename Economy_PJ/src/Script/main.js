const periodBtnModule = document.querySelector('.period-controls');
const graphIndicators = [
    {id: "exchange-rate", title: "원/달러 환율"},
    {id: "rcv", title: "실질적 화폐가치"},
    {id: "br", title: "기준금리"},
    {id: "ca", title: "경상수지"},
    {id: "reer", title: "실질실효환율"},
    
];
const container = document.querySelector('.dashboard-container');
const graphTemplate = document.querySelector('#indicators-template');
const addChartBtn = document.getElementById('add-new-chart');

function getAdaptiveFontSize(text) {
    /**
     * 글자 수에 따라 글자 크기를 조절해주는 함수
     */
    const len = text.length;
    if (len > 8) return "0.8rem";
    if (len > 5) return "0.95rem";
    return "1.1rem";
}

/* ===== 경제지표 추가버튼 이벤트리스너 ===== */
addChartBtn.addEventListener('click', () => {
    alert.apply('새로운 경제지표 추가');
})

/* ===== 추가할 수 있는 환율 데이터를 요청하는 함수 ===== */
async function requestSeriesData() {
    try {
        const url = "/api/exchange_series";
        const response = await fetch(url);

        if(!response.ok) throw new Error("네트워크 오류");

        const result = await response.json();
        console.log('환율 시리즈 데이터:', result);
    } catch (error) {
        console.error('데이터 요청 중 오류 발생:', error);
    }
}

// graphIndicators.forEach(data => {
//     /**
//      * indicator에서 문자열을 읽어 각 카드의 이름을 부여 선언
//      * 문자의 크기에 맞춰 적절히 조절하는 함수를 끌어온다.
//      */
//     const clone = graphTemplate.content.cloneNode(true);
//     const cardWrapper = clone.querySelector('.chart-card');
//     const graphTitleElement = clone.querySelector('h3');
//     const titleText = data.title;

//     cardWrapper.dataset.indicatorId = data.id;

//     graphTitleElement.textContent = titleText;
//     graphTitleElement.style.fontSize = getAdaptiveFontSize(titleText);

//     container.appendChild(clone);
// });

document.addEventListener('DOMContentLoaded', () => {
    /**
     * 각 카드 내부에 있는 버튼을 인식하게 해주는 이벤트리스너
     */
    const dashboard = document.querySelector('.dashboard-container');

    dashboard.addEventListener('click', (e) => {
        const periodBtn = e.target.closest('.btn-period');
        if (!periodBtn) return;

        const card = periodBtn.closest('.chart-card');
        const cardTitle = card.querySelector('.card-header h3').textContent;
        const cardId = card.dataset.indicatorId;
        const period = periodBtn.dataset.period;

        requestDatabyPeriod(card, period);

        // 눌린 카드와 버튼을 확인하는 테스트 코드
        console.log('클릭된 카드: ', cardTitle);
        console.log('클릭된 카드의 id: ', cardId);
        console.log('선택된 기간: ', period);

        const periodBtns = card.querySelectorAll('.btn-period');
        periodBtns.forEach(btn => btn.classList.remove('active'));
        periodBtn.classList.add('active');
    });
});

requestSeriesData();