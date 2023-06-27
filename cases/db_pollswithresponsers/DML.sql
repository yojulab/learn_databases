-- Inserting choices
INSERT INTO CHOICE (CHOICE_ID, CHOICE)
VALUES ('C1', '예'),
       ('C2', '아니오'),
       ('C3', '모르겠음');

-- Inserting questions
INSERT INTO QUESTIONS (QUESTIONS, QUESTIONS_ID)
VALUES ('질문 1: 현재 증상이 있습니까?', 'Q1'),
       ('질문 2: 과거 질병 이력이 있습니까?', 'Q2'),
       ('질문 3: 현재 복용 중인 약물이 있습니까?', 'Q3'),
       ('질문 4: 가족 중 유전적으로 의료 이력이 있는 사람이 있습니까?', 'Q4');

-- Inserting respondents
INSERT INTO RESPONDENTS (RESPONDENTS, RESPONDENTS_ID)
VALUES ('김영희', 'R1'),
       ('박철수', 'R2'),
       ('이지은', 'R3'),
       ('홍길동', 'R4');

-- Inserting question-choice relationships
INSERT INTO QUESTION_CHOICE (QUESTIONS_ID, CHOICE_ID)
VALUES ('Q1', 'C1'),
       ('Q1', 'C2'),
       ('Q1', 'C3'),
       ('Q2', 'C1'),
       ('Q2', 'C2'),
       ('Q2', 'C3'),
       ('Q3', 'C1'),
       ('Q3', 'C2'),
       ('Q3', 'C3'),
       ('Q4', 'C1'),
       ('Q4', 'C2'),
       ('Q4', 'C3');

-- Inserting statistics
INSERT INTO STATISTICS (STATISTICS_ID, RESPONDENTS_ID, QUESTIONS_ID, CHOICE_ID)
VALUES ('S1', 'R1', 'Q1', 'C1'),
       ('S2', 'R1', 'Q2', 'C2'),
       ('S3', 'R1', 'Q3', 'C3'),
       ('S4', 'R1', 'Q4', 'C1'),
       ('S5', 'R2', 'Q1', 'C2'),
       ('S6', 'R2', 'Q2', 'C3'),
       ('S7', 'R2', 'Q3', 'C1'),
       ('S8', 'R2', 'Q4', 'C2'),
       ('S9', 'R3', 'Q1', 'C3'),
       ('S10', 'R3', 'Q2', 'C1'),
       ('S11', 'R3', 'Q3', 'C2'),
       ('S12', 'R3', 'Q4', 'C3'),
       ('S13', 'R4', 'Q1', 'C1'),
       ('S14', 'R4', 'Q2', 'C2'),
       ('S15', 'R4', 'Q3', 'C3'),
       ('S16', 'R4', 'Q4', 'C1');
