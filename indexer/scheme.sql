DROP TABLE IF EXISTS data_payments;

CREATE TABLE data_payments
(
  paymentid integer,  
  globalpaymentid varchar(10),
  constraint globalpaymentid primary key (globalpaymentid),
  globalrecipientid varchar(10),
  globalrecipientidx varchar(10),
  globalschemeid varchar(10),
  amounteuro numeric,
  amountnationalcurrency numeric,
  year int,
  countrypayment varchar(2)
)
WITH (OIDS=FALSE);
ALTER TABLE data_payments OWNER TO farmsubsidy;



DROP TABLE IF EXISTS data_recipients;
CREATE TABLE data_recipients
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
ALTER TABLE data_recipients OWNER TO farmsubsidy;


DROP TABLE IF EXISTS data_schemes;
CREATE TABLE data_schemes
(
  globalschemeid varchar,
  CONSTRAINT globalschemeid PRIMARY KEY (globalschemeid),
  namenationallanguage text,
  nameenglish text,
  budgetlines8digit varchar(10),
  countrypayment varchar(2)  
) WITH (OIDS=FALSE);
ALTER TABLE data_schemes OWNER TO farmsubsidy;




DROP TABLE IF EXISTS data_totals;
CREATE TABLE data_totals
(
  global_id character varying(10) NOT NULL,
  amount_euro numeric,
  "year" integer,
  countrypayment varchar(2),
  nameenglish text   
)
WITH (OIDS=FALSE);
ALTER TABLE data_totals OWNER TO farmsubsidy;
