-- query
-- 젊은 동물 조회 query 만들기(INTAKE_CONDITION != 'Aged')
SELECT 
    * 
FROM   ANIMAL_INS 
WHERE INTAKE_CONDITION != 'Aged'

-- 조회한 젊은 동물수 확인
SELECT 
    COUNT(*) 
FROM   ANIMAL_INS 
WHERE INTAKE_CONDITION != 'Aged'

-- 젊은 동물만 있는 아이디와 이름 query 만들고, row 수 확인
SELECT 
    ANIMAL_ID, NAME 
FROM   ANIMAL_INS 
WHERE INTAKE_CONDITION != 'Aged'
ORDER BY ANIMAL_ID

-- 젊은 동물만 있는 아이디와 이름 query 만들고, row 수 확인
SELECT 
    COUNT(*) 
FROM   ANIMAL_INS 
WHERE INTAKE_CONDITION != 'Aged'
