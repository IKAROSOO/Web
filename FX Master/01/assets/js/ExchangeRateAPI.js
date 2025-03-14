const authkey = "ngAR4EKodVz5wYWE1z0b2SUOFyntP5IP";
// -> 인증키
const data = "AP01";
/**
 * AP01 : 환율
 * AP02 : 대출금리
 * AP03 : 국제금리
 */
const searchdate = getDate();
const url = `https://www.koreaexim.go.kr/site/program/
financial/exchangeJSON?authkey=${authkey}&searchdate=${searchdate}&data=${data}`;

function getDate() {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, "0");
  const day = String(now.getDate()).padStart(2, "0");

  return `${year}${month}${day}`;
}

/**
 *
 * fetch(url)
  .then((response) => response.json())
  .then((data) => {
    console.log(data);
  })
  .catch((error) => {
    console.log("API 호출 실패", error);
  });

 */

async function getExchangeRates() {
  try {
    const response = await fetch(url);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("API 데이터 불러오기 실패", error);
    return null;
  }
}

async function updateDollarRate() {
  const exchangeData = await getExchangeRates();
  if (exchangeData) {
    const usdRate = exchangeData.find((item) => item.cur_nm === "미국 달러");
    if (usdRate) {
      const box = document.querySelector(".box:nth-child(1)");
      box.textContent = usdRate.tts; // 또는 ttb, 또는 다른 환율 정보
    } else {
      const box = document.querySelector(".box:nth-child(1)");
      box.textContent = "USD 환율 정보 없음";
    }
  } else {
    const box = document.querySelector(".box:nth-child(1)");
    box.textContent = "API 데이터 없음";
  }
}

updateDollarRate();
