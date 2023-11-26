CREATE TABLE Detective(
    det_id VARCHAR(20) PRIMARY KEY NOT NULL,
    det_name VARCHAR(255),
    gender VARCHAR(20),
    age INT,
    adm_id VARCHAR(20));

CREATE TABLE Cases(
    case_id VARCHAR(20) PRIMARY KEY NOT NULL,
    p_o_c VARCHAR(25),
    det_id VARCHAR(20),
    status BOOLEAN,
    case_details VARCHAR(520),
    FOREIGN KEY(det_id) REFERENCES Detective(det_id) ON DELETE CASCADE);

CREATE TABLE Evidence(
    case_id VARCHAR(20),
    evidence VARCHAR(255),
    PRIMARY KEY(case_id,evidence),
    FOREIGN KEY(case_id) REFERENCES Cases(case_id) ON DELETE CASCADE
    );

CREATE TABLE Admin(
    adm_id VARCHAR(20) PRIMARY KEY,
    adm_name VARCHAR(20)
    );


ALTER TABLE Detective
ADD CONSTRAINT adm_id
FOREIGN KEY (adm_id)
REFERENCES  Admin(adm_id) ON DELETE CASCADE;


INSERT INTO Admin(adm_id,adm_name) VALUES ("A1","Deepthi"),("A2","Arun");
INSERT INTO Detective(det_id,det_name,gender,age,adm_id) VALUES ("D1","Arunima","Female",30,"A1"),("D2","Ranjan","Male",45,"A2");
INSERT INTO Cases(case_id,p_o_c,det_id,status,case_details) VALUES ("C1","Bangalore","D1",0,"https://tinyurl.com/mr3st6de"),("C2","Mumbai","D2",0,"https://tinyurl.com/bddewj6t");


CREATE TABLE Criminal(
    cri_id VARCHAR(20) PRIMARY KEY NOT NULL,
    cri_name VARCHAR(25),
    fingerprint VARCHAR(255),
    age INT,
    gender VARCHAR(20));

CREATE TABLE InvolvedIn(
    case_id VARCHAR(20),
    cri_id VARCHAR(20),
    PRIMARY KEY(case_id,cri_id),
    FOREIGN KEY(case_id) REFERENCES Cases(case_id) ON DELETE CASCADE,
    FOREIGN KEY(cri_id) REFERENCES Criminal(cri_id) ON DELETE CASCADE)
    ;


CREATE TABLE Victim(
    case_id VARCHAR(20),
    vic_name VARCHAR(20),
    vic_contact VARCHAR(13),
    PRIMARY KEY(case_id,vic_name),
    FOREIGN KEY(case_id) REFERENCES Cases(case_id) ON DELETE CASCADE)
    ;
