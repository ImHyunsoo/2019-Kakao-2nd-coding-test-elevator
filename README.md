# 2019-Kakao-2nd-coding-test-elevator
2019 카카오 2차 코딩테스트 엘레베이터 문제를 직접 푸는 과정과 다른 사람들의 풀이를 참고하여 문제풀이를 개선하는 과정을 담는 리포지터리입니다.
문제를 풀며 마주친 오류들은 깃헙의 Issues와 Pull requests 기능을 이용하여 해결하는 과정을 기록합니다.

## 직접 풀어본 문제 풀이
* 엘리베이터 기본 아이디어 
    1. 진향 방향쪽으로 내리거나 태울 승객이 있다면 진행 방향을 유지하면 승객을 수송합니다.  
    2. 진행 방향쪽으로 내리거나 태울 승객이 없다면 진행 방향을 바꿔서 1.의 과정을 반복합니다. 
    3. 모든 층에서 내리거나 태울 승객이 없다면 정지합니다.

### 문제0. 어피치 맨션 (problem_id = 0)
* 엘리베이터 한 대를 운용합니다.                

### 문제1. 제이지 빌딩 (problem_id = 1)
* 엘리베이터 여러 대를 운용합니다.
    * 태울 승객 리스트를 관리합니다. 
        * 태울 승객은 리스트에서 제거하여 또 다른 엘베에 동시에 탑승하지 못하도록 합니다.
        * 현재 타고 있는 승객의 수를 고려하여 정원 초과되지 않도록 승객을 태웁니다.
<img width="80%" src="https://user-images.githubusercontent.com/20950569/161916553-75fe79e8-8402-4a18-b433-e743614700c6.gif"/>

#### 다른 사람 풀이를 참고 및 개선사항 


### 문제2. 라이언 타워 (problem_id = 2)
* 엘리베이터를 최적화하여 운용합니다.

