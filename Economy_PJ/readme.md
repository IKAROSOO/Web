**설계 배경 :
환울, 화폐가치, 금리 등의 다양한 경제지표를 한눈에 확인할 수 있는 프로그램을 작성해보고 싶음** 

# 향후 추가 사항들
$$
	1. 최초 사용시 API KEY를 입력하여 env에 저장하는 기능
	2. 이미 저장된 API KEY를 교체/갱신하는 기능
$$ 

==설계==
1. Python을 활용한 Server
	1. [[Server 설계]]
	2.  기본적인 API요청 등은 Python을 활용
	3.  받아온 데이터를 가공하는 과정에서 연산의 최적화를 위해 부분적으로 C를 사용
	4.  최종적으로 RUST로 언어를 바꾸는 것이 목적
2. JS, HTML, CSS를 활용한 Client
	1. [[Client 설계]]
	2.  '한국'의 환율 그래프(1개)를 표시
	3.  '한국'의 경제지표 그래프 2개를 표시
		1. 경제지표 선택지는 하드코딩
	4. '한국'의 경제지표 그래프 N개를 선택해서 표시
		1. 경제지표 선택지는 하드코딩
		2. 경제지표 선택지를 API로 선택할 수 있게 수정
	5. '임의'의 국가의 경제지표 그래프를 N개 선택가능
		1. API로 선택가능한 경제지표 리스트 불러오기
		2. '환율'의 경우, 주고받는 통화를 자유롭게 선택 가능

![js](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=JavaScript&logoColor=white)  ![js](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![js](https://img.shields.io/badge/HTML-239120?style=for-the-badge&logo=html5&logoColor=white)