function checkTabInfo() {
    // const tabUrl = window.location.href;
    
    // 파일명으로 사용할 수 없는 특수문자(\ / : * ? " < > |)를 언더바(_)로 치환
    const tabTitle = document.title.replace(/[\/\\:*?"<>|]/g, "_");

    // console.log(`Tab URL: ${tabUrl}`);
    // console.log(`Tab Title: ${tabTitle}`);

    return {
        // url: tabUrl,
        title: tabTitle
    };
}

function extractPageText() {
    let pageText = "";
    const mainFrame = document.getElementById("mainFrame");

    // 네이버 블로그와 같이 iframe(id="mainFrame")을 사용하는 사이트 대응
    if (mainFrame && mainFrame.contentDocument) {
        pageText = mainFrame.contentDocument.body.innerText;
    } else {
        pageText = document.body.innerText;
    }

    /**
     * 1. Blob 객체 생성: 텍스트 데이터를 파일 객체(Blob)로 변환
     */
    const blob = new Blob([pageText], {type: 'text/plain'});

    /**
     * 2. 가상 URL 생성: 메모리 상의 Blob 객체에 접근할 수 있는 임시 주소 생성
     */
    const url = URL.createObjectURL(blob);

    // 3. 가상의 다운로드 링크(<a>) 생성
    const a = document.createElement('a');
    const tabTitle = checkTabInfo().title;

    // console.log(`Length of PageText: ${pageText.length}`);
    // console.log(`Part of Text: ${pageText.substring(0, 100)}`);

    a.href = url;
    a.download = `${tabTitle}.txt`; // download 속성으로 파일명 지정

    /**
     * 4. 강제 클릭 이벤트 발생
     * - DOM에 링크를 붙이고 클릭하여 다운로드 트리거
     */
    document.body.appendChild(a);
    a.click();
    
    console.log(`${tabTitle}.txt Download`);

    /**
     * 5. 뒷정리 (메모리 해제)
     * - DOM에서 링크 제거 및 임시 URL 해제
     */
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "DownloadBtn_clicked") {
        console.log(`${request.action} 수신`);
        console.log(`${checkTabInfo().title}`);
        // extractPageText();
    }
    return true;
});