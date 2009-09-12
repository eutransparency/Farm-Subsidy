DROP TABLE IF EXISTS payments;

CREATE TABLE payments
(
  paymentid integer,  
  globalpaymentid varchar(10),
  constraint globalpaymentid primary key (globalpaymentid),
  globalrecipientid varchar(10),
  globalrecipientidx varchar(10),
  globalschemeid varchar(10),
  amounteuro money,
  amountnationalcurrency money,
  year int,
  countrypayment varchar(2)
)
WITH (OIDS=FALSE);
ALTER TABLE payments OWNER TO farmsubsidy;



DROP TABLE IF EXISTS recipients;
CREATE TABLE recipients
(
  
  
  recipientid varchar(10),
  recipientidx varchar(10),
  globalrecipientid varchar(10),
  globalrecipientidx varchar(10),
  name text,
  address1 text,
  address2 text,
  zipcode varchar(10),
  town text,
  countryrecipient varchar(2),
  countrypayment varchar(2),
  geo1 text,
  geo2 text,
  geo3 text,
  geo4 text,
  geo1nationallanguage text,
  geo2nationallanguage text,
  geo3nationallanguage text,
  geo4nationallanguage text,
  lat double precision,
  lng double precision  
) WITH (OIDS=FALSE);
ALTER TABLE recipients OWNER TO farmsubsidy;

-- CREATE INDEX country
--    ON recipients USING btree (country);
--    

-- CREATE INDEX recipient_globalrecipientidx
--    ON recipients USING btree (globalrecipientidx);
-- 
-- CREATE INDEX globalrecipientid
--    ON recipients USING btree (globalrecipientid);



DROP TABLE IF EXISTS schemes;
CREATE TABLE schemes
(
  globalschemeid varchar,
  CONSTRAINT globalschemeid PRIMARY KEY (globalschemeid),
  namenationallanguage text,
  nameenglish text,
  budgetlines8digit varchar(10),
  countrypayment varchar(2)  
) WITH (OIDS=FALSE);
ALTER TABLE recipients OWNER TO farmsubsidy;




DROP TABLE IF EXISTS totals;
CREATE TABLE totals
(
  global_id character varying(10) NOT NULL,
  amount_euro money,
  "year" integer,
  countrypayment varchar(2)    
)
WITH (OIDS=FALSE);
ALTER TABLE totals OWNER TO postgres;
