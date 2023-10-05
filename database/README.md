** Uploaded files would be stored under this folder **

** Setting up local database schema **

```SQL
-- Create database
MariaDB [(none)]> CREATE DATABASE capstone;
MariaDB [(none)]> SHOW DATABASES;

-- Create tables
MariaDB [(none)]> USE capstone;
MariaDB [capstone]> CREATE TABLE doc (
  did INT PRIMARY KEY AUTO_INCREMENT,
  dname TEXT UNIQUE,
  contents TEXT,
  typo BOOLEAN DEFAULT FALSE,
  slang BOOLEAN DEFAULT FALSE,
  dup BOOLEAN DEFAULT FALSE,
  pdd BOOLEAN DEFAULT FALSE,
  spc BOOLEAN DEFAULT FALSE
);
MariaDB [capstone]> DESC doc;
-- Sample result
-- +----------+------------+------+-----+---------+----------------+
-- | Field    | Type       | Null | Key | Default | Extra          |
-- +----------+------------+------+-----+---------+----------------+
-- | did      | int(11)    | NO   | PRI | NULL    | auto_increment |
-- | dname    | text       | YES  | UNI | NULL    |                |
-- | contents | text       | YES  |     | NULL    |                |
-- | typo     | tinyint(1) | YES  |     | 0       |                |
-- | slang    | tinyint(1) | YES  |     | 0       |                |
-- | dup      | tinyint(1) | YES  |     | 0       |                |
-- | pdd      | tinyint(1) | YES  |     | 0       |                |
-- | spc      | tinyint(1) | YES  |     | 0       |                |
-- +----------+------------+------+-----+---------+----------------+

MariaDB [capstone]> CREATE TABLE sprocessing (
  sid INT PRIMARY KEY,
  did INT,
  osent TEXT,
  typo JSON DEFAULT NULL,
  slang JSON DEFAULT NULL,
  dup BOOLEAN DEFAULT FALSE,
  pdd JSON DEFAULT NULL,
  spc JSON DEFAULT NULL,
  csent TEXT
);
MariaDB [capstone]> ALTER TABLE sprocessing DROP PRIMARY KEY;
MariaDB [capstone]> ALTER TABLE sprocessing ADD PRIMARY KEY(sid, did);
MariaDB [capstone]> ALTER TABLE sprocessing ADD FOREIGN KEY (did) REFERENCES doc(did);

MariaDB [capstone]> DESC sprocessing;
-- Sample result
-- +-------+------------+------+-----+---------+-------+
-- | Field | Type       | Null | Key | Default | Extra |
-- +-------+------------+------+-----+---------+-------+
-- | sid   | int(11)    | NO   | PRI | NULL    |       |
-- | did   | int(11)    | NO   | PRI | NULL    |       |
-- | osent | text       | YES  |     | NULL    |       |
-- | typo  | longtext   | YES  |     | NULL    |       |
-- | slang | longtext   | YES  |     | NULL    |       |
-- | dup   | tinyint(1) | YES  |     | 0       |       |
-- | pdd   | longtext   | YES  |     | NULL    |       |
-- | spc   | longtext   | YES  |     | NULL    |       |
-- | csent | text       | YES  |     | NULL    |       |
-- +-------+------------+------+-----+---------+-------+
MariaDB [capstone]> SHOW INDEX FROM sprocessing;
-- Sample result
-- +-------------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+
-- | Table       | Non_unique | Key_name | Seq_in_index | Column_name | Collation | Cardinality | Sub_part | Packed | Null | Index_type | Comment | Index_comment | Ignored |
-- +-------------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+
-- | sprocessing |          0 | PRIMARY  |            1 | sid         | A         |           0 |     NULL | NULL   |      | BTREE      |         |               | NO      |
-- | sprocessing |          0 | PRIMARY  |            2 | did         | A         |           0 |     NULL | NULL   |      | BTREE      |         |               | NO      |
-- | sprocessing |          1 | did      |            1 | did         | A         |           0 |     NULL | NULL   |      | BTREE      |         |               | NO      |
-- +-------------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+


-- Insert sample data
MariaDB [capstone]> INSERT INTO doc (dname, contents) VALUES (
  'demo.txt',
'게시글 샘플 잉니다.
이건 시발 욕설 문장이다.
010-1234-5678로 연락해라!
중복된 문장 입니다.
중복된 문장 입니다.'
);
-- Update value when needed
-- Start of updating queries
MariaDB [capstone]> UPDATE doc SET pdd = True WHERE did = 1;
MariaDB [capstone]> UPDATE sprocessing
                    SET typo = '{"0": {"dvalue": "ㅁ", "cvalue": "뭐", "desc": ""}, "1": {"dvalue": "123", "cvalue": "1234", "desc": ""}}'
                    WHERE sid = 3;
-- End of updating queries

MariaDB [capstone]> INSERT INTO sprocessing (sid, did, osent, typo, slang, dup, pdd, spc, csent)
VALUES (1, 1, '게시글 샘플 잉니다.', '{"0": {"dvalue": "잉", "cvalue": "입", "desc": ""}}', NULL, NULL, NULL, NULL, NULL);
MariaDB [capstone]> INSERT INTO sprocessing (sid, did, osent, typo, slang, dup, pdd, spc, csent)
VALUES (2, 1, '이건 시발 욕설 문장이다.', NULL, '{"0": {"dvalue": "시발", "cvalue": "**", "desc": "욕설"}}', NULL, NULL, NULL, NULL);
MariaDB [capstone]> INSERT INTO sprocessing (sid, did, osent, typo, slang, dup, pdd, spc, csent)
VALUES (3, 1, '010-1234-5678로 연락해라!', NULL, NULL, NULL, '{"0": {"dvalue": "010-1234-5678", "cvalue": "010-****-****", "desc": "전화번호"}}', NULL, NULL);
MariaDB [capstone]> INSERT INTO sprocessing (sid, did, osent, typo, slang, dup, pdd, spc, csent)
VALUES (4, 1, '중복된 문장 입니다.', NULL, NULL, FALSE, NULL, NULL, NULL);
MariaDB [capstone]> INSERT INTO sprocessing (sid, did, osent, typo, slang, dup, pdd, spc, csent)
VALUES (5, 1, '중복된 문장 입니다.', NULL, NULL, TRUE, NULL, NULL, NULL);
```
