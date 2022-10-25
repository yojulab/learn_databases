SELECT * FROM study_sqls.organizaitons;
delete from study_sqls.organizaitons;

insert into organizaitons (DEPARTMENT, UNIQUE_ID, UNIQUE_ID_PARENT)
values ('이사장', 'P1', null)
, ('비서실',	'P2',	'P1')
, ('이사회',	'P3',	'P1')
, ('감사',	'P4',	'P1')
, ('감사실',	'P5',	'P4')
, ('사무총장',	'P6',	'P1')
, ('법률지원단',	'P7',	'P6')
, ('기획조정실',	'P8',	'P6')
, ('구조국',	'P9',	'P6')
, ('행정국',	'P10',	'P6')
, ('홍보실',	'P11',	'P6')
;
