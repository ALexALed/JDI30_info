CREATE TABLE COMPANY(
   id             TEXT PRIMARY KEY NOT NULL,
   name           TEXT NOT NULL,
   est_revenue    INT,
   url            TEXT,
   street         TEXT,
   city           TEXT,
   zip_code       TEXT,
   country        TEXT,
   employees_count INT,
   industry       TEXT
);
