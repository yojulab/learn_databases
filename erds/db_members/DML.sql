-- INSERT INTO table_name
-- VALUES (value1, value2, value3, ...);
-- INSERT INTO table_name (column1, column2, column3, ...)
-- VALUES (value1, value2, value3, ...);


-- gender_code  성별 코드 생성
INSERT INTO gender_code
(GENDER, GENDER_CODE_ID)
VALUES
('남', 'G-01');

INSERT INTO gender_code
(GENDER, GENDER_CODE_ID)
VALUES
('여', 'G-04');

-- address_code 주소 코드 생성
INSERT INTO address_code
(ADDRESS,ADDRESS_CODE_ID)
VALUES
('서울시', 'A-01'),
('부산시', 'A-02'),
('경기도', 'A-03'),
('대전시', 'A-04'),
('인천시', 'A-05');

-- members 회원정보 입력
INSERT INTO members
(AGE,NAME,TELEPHONE,MEMBERS_ID,GENDER_CODE_ID,ADDRESS_CODE_ID)
VALUES
(30, '홍길동', '010-1234-5678', 'M-01', 'G-01', 'A-01'),
(25, '박영희', '010-9876-5432', 'M-02', 'G-04', 'A-02'),
(35, '김철수', '010-1111-2222', 'M-03', 'G-01', 'A-03'),
(28, '이영미', '010-3333-4444', 'M-04', 'G-04', 'A-04'),
(32, '정민호', '010-5555-6666', 'M-05', 'G-01', 'A-05');

-- members_hobby 취미 코드 생성
INSERT INTO hobby_code
(HOBBY, HOBBY_CODE_ID)
VALUES
('요리', 'H-01'),
('등산', 'H-02'),
('독서', 'H-03'),
('영화감상', 'H-04'),
('음악 감상', 'H-05'),
('요가', 'H-06'),
('여행', 'H-07'),
('사진촬영', 'H-08'),
('수영', 'H-09');

-- hobby_code 취미코드와 회원코드 연결
INSERT INTO members_hobby
(MEMBERS_ID, HOBBY_CODE_ID)
VALUES
('M-01', 'H-01'),
('M-01', 'H-02'),
('M-02', 'H-03'),
('M-02', 'H-04'),
('M-03', 'H-05'),
('M-03', 'H-06'),
('M-04', 'H-07'),
('M-04', 'H-08'),
('M-05', 'H-02'),
('M-05', 'H-09');

-- membewrs_login 로그인 코드
INSERT INTO members_login
(EMAIL,MEMBERS_ID,MEMBERS_LOGIN_ID)
VALUES
('hong@gmail.com', 'M-01', 'L-01'),
('park.younghee@naver.com', 'M-02', 'L-02'),
('kimchulsu@gmail.com', 'M-03', 'L-03'),
('leeyoungmi@naver.com', 'M-04', 'L-04'),
('jmh123@gmail.com', 'M-05', 'L-05');