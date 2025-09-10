document.addEventListener('DOMContentLoaded', function() {
    const uploadBtn = document.querySelector('.upload-btn');
    const returnBtn = document.querySelector('.return-btn');
    const fileInput = document.getElementById('file-input');
    const previewImage = document.getElementById('image-preview');
    const dropZone = document.getElementById('drop-zone');
    
    const backendUrl = 'http://127.0.0.1:5000/image-processing';
    const reader = new FileReader();

    // 업로드 버튼에 대한 이벤트리스너
    uploadBtn.addEventListener('click', function() {
        console.log("CHOOSE FILES 버튼이 클릭됨");
        fileInput.click();
    });

    // 파일이 업로드되는 것을 파악하는 이벤트리스너
    fileInput.addEventListener('change', function(event) {
        const selectedFile = event.target.files[0];
        const fileType = selectedFile.type;

        const allowImageTypes = [
            'image/jpeg',
            'image/png',
            'image/gif',
            'image/webp'
        ];

        if (allowImageTypes.includes(fileType)) {
            console.log(`File Name : ${selectedFile.name}`);
            console.log(`File Type : ${fileType}`);
            /**
             * reader.readAsText(selectedFile);
             * -> readAsText는 문자열을 읽어들이는데 특화된 함수
             */
            reader.readAsDataURL(selectedFile);
        } else {
            console.log(`Wrong File Type : ${fileType}`);
            alert('jpg, png, gif, webp 파일만 업로드 가능합니다!');

            fileInput.value = null;
            previewImage.src = null;
        }
    });

    // 업로드된 파일이 전부 읽혔을 때, 해당 내용을 출력하는 함수
    reader.onload = async function(event) {
        const dataToSend = {
            imageData: event.target.result
        }

        // 사진이 업로드되면 사진과 초기화면 버튼만 display
        previewImage.src = event.target.result;
        
        dropZone.classList.add('preview-mode');
        
        // 서버로 이미지 데이터를 송신하는 함수
        fetch(backendUrl, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dataToSend)
        })
        .then(Response => Response.json())
        .then(data => {
            console.log(`백엔드 응답 : ${data}` );
        })
        .catch(error => {
            console.error(`전송오류 : ${error}`);
            alert('서버와 통신 중 오류가 발생했습니다.');
        });
    }

    // 초기화면 버튼에 대한 이벤트리스너
    returnBtn.addEventListener('click', function() {
        console.log("초기화면으로 버튼이 클릭됨");

        dropZone.classList.remove('preview-mode');

        /**
         * 기존의 fileInput에 있던 데이터를 지우지 않으면 동일한 파일을 업로드 했을 경우,
         * 이미지가 나오지 않는 상황 발생
         */
        fileInput.value = null;
        previewImage.src = null;
    });
});