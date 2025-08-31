// Client.js

document.addEventListener("DOMContentLoaded", function() {
    
    const API_ENDPOINT = "http://127.0.0.1:5000/api/exchange-rate";

    fetch(API_ENDPOINT)
        .then(response => {
            if (!response.ok) {
                throw new Error("네트워크 응답에 문제가 있습니다.");
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            updateUI(data);
        })
        .catch(error => {
            console.error("데이터를 가져오는 중 문제가 발생했습니다:", error);
            alert("환율 정보를 불러오는 데 실패했습니다: " + error.message);
        });

});

function updateUI(rates) {
    // 원/달러(USD) 정보 업데이트
    const usdRate = rates.find(rate => rate.currency_code === "USD");
    if (usdRate) {
        document.getElementById("krw-usd-sell").textContent = usdRate.sell_price;
        document.getElementById("krw-usd-buy").textContent = usdRate.buy_price;
        updateChangeInfo("krw-usd-change", usdRate);
    }

    // 원/엔(JPY) 정보 업데이트
    const jpyRate = rates.find(rate => rate.currency_code === "JPY(100)");
    if (jpyRate) {
        document.getElementById("krw-jpy-sell").textContent = jpyRate.sell_price;
        document.getElementById("krw-jpy-buy").textContent = jpyRate.buy_price;
        updateChangeInfo("krw-jpy-change", jpyRate);
    }
}

function updateChangeInfo(elementId, rateData) {
    const changeElement = document.getElementById(elementId);
    let changeText = "";
    
    if (rateData.direction === "up") {
        changeText = `▲ ${Math.abs(rateData.change).toFixed(2)}`;
    } else if (rateData.direction === "down") {
        changeText = `▼ ${Math.abs(rateData.change).toFixed(2)}`;
    } else {
        changeText = `${rateData.change.toFixed(2)}`;
    }
    
    changeElement.textContent = changeText;
    // 이전 클래스 초기화 후 새로운 클래스 추가
    changeElement.className = ""; 
    changeElement.classList.add(rateData.direction);
}