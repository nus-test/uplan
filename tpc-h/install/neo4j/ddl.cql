CREATE CONSTRAINT CONS_SUPPKEY FOR (s:Supplier) REQUIRE s.S_SUPPKEY IS UNIQUE;
LOAD CSV FROM 'file:///supplier.tbl' AS line FIELDTERMINATOR '|'
CREATE (supplier:SUPPLIER)
SET supplier.S_SUPPKEY = line[0],
    supplier.S_NAME = line[1],
    supplier.S_ADDRESS = line[2],
    supplier.S_NATIONKEY = line[3],
    supplier.S_PHONE = line[4],
    supplier.S_ACCTBAL = line[5],
    supplier.S_COMMENT = line[6];

CREATE CONSTRAINT CONS_CUSTKEY FOR (c:CUSTOMER) REQUIRE c.C_CUSTKEY IS UNIQUE;
LOAD CSV FROM 'file:///customer.tbl' AS line FIELDTERMINATOR '|'
CREATE (customer:CUSTOMER)
SET customer.C_CUSTKEY = line[0],
    customer.C_NAME = line[1],
	customer.C_ADDRESS = line[2],
    customer.C_NATIONKEY = line[3],
    customer.C_PHONE = line[4],
    customer.C_ACCTBAL = toFloat(line[5]),
    customer.C_MKTSEGMENT = line[6],
    customer.C_COMMENT = line[7];

LOAD CSV FROM 'file:///partsupp.tbl' AS line FIELDTERMINATOR '|'
CREATE (partsupp:PARTSUPP)
SET partsupp.PS_PARTKEY = line[0],
    partsupp.PS_SUPPKEY = line[1],
    partsupp.PS_AVAILQTY = line[2],
    partsupp.PS_SUPPLYCOST = line[3],
    partsupp.PS_COMMENT = line[4];

LOAD CSV FROM 'file:///lineitem.tbl' AS line FIELDTERMINATOR '|'
CREATE (lineitem:LINEITEM)
SET lineitem.L_ORDERKEY = line[0],
    lineitem.L_PARTKEY = line[1],
    lineitem.L_SUPPKEY = line[2],
    lineitem.L_LINENUMBER = line[3],
    lineitem.L_QUANTITY = toFloat(line[4]),
    lineitem.L_EXTENDEDPRICE = toFloat(line[5]),
    lineitem.L_DISCOUNT = toFloat(line[6]),
    lineitem.L_TAX = toFloat(line[7]),
    lineitem.L_RETURNFLAG = line[8],
    lineitem.L_LINESTATUS = line[9],
    lineitem.L_SHIPDATE = date(line[10]),
    lineitem.L_COMMITDATE = date(line[11]),
    lineitem.L_RECEIPTDATE = date(line[12]),
    lineitem.L_SHIPINSTRUCT = line[13],
    lineitem.L_SHIPMODE = line[14],
    lineitem.L_COMMENT = line[15];

CREATE CONSTRAINT CONS_NATIONKEY FOR (n:NATION) REQUIRE n.N_NATIONKEY IS UNIQUE;
LOAD CSV FROM 'file:///nation.tbl' AS line FIELDTERMINATOR '|'
CREATE (nation:NATION)
SET	    nation.N_NATIONKEY = line[0],
		nation.N_NAME = line[1],
        nation.N_REGIONKEY = line[2],
		nation.N_COMMENT = line[3];

CREATE CONSTRAINT CONS_ORDERKEY FOR (o:ORDERS) REQUIRE o.O_ORDERKEY IS UNIQUE;
LOAD CSV FROM 'file:///orders.tbl' AS line FIELDTERMINATOR '|'
CREATE (orders:ORDERS)
SET orders.O_ORDERKEY = line[0],
    orders.O_CUSTKEY = line[1],
    orders.O_ORDERSTATUS = line[2],
    orders.O_TOTALPRICE = line[3],
    orders.O_ORDERDATE = date(line[4]),
    orders.O_ORDERPRIORITY = line[5],
    orders.O_CLERK = line[6],
    orders.O_SHIPPRIORITY = line[7],
    orders.O_COMMENT = line[8];

CREATE CONSTRAINT CONS_PARTKEY FOR (p:PART) REQUIRE p.P_PARTKEY IS UNIQUE;
LOAD CSV FROM 'file:///part.tbl' AS line FIELDTERMINATOR '|'
CREATE (part:PART)
SET part.P_PARTKEY = line[0],
    part.P_NAME = line[1],
    part.P_MFGR = line[2],
    part.P_BRAND = line[3],
    part.P_TYPE = line[4],
    part.P_SIZE = line[5],
    part.P_CONTAINER = line[6],
    part.P_RETAILPRICE = line[7],
    part.P_COMMENT = line[8];

CREATE CONSTRAINT CONS_REGIONKEY FOR (r:REGION) REQUIRE r.R_REGIONKEY IS UNIQUE;
LOAD CSV FROM 'file:///region.tbl' AS line FIELDTERMINATOR '|'
CREATE (region:REGION)
SET region.R_REGIONKEY = line[0],
    region.R_NAME = line[1],
    region.R_COMMENT = line[2];



MATCH (lineitem:LINEITEM), (orders:ORDERS)
WHERE lineitem.L_ORDERKEY = orders.O_ORDERKEY
CREATE (lineitem)-[:BELONGS_TO]->(orders);

MATCH (customer:CUSTOMER), (orders:ORDERS)
WHERE customer.C_CUSTKEY = orders.O_CUSTKEY
CREATE (orders)-[:ORDERED_BY]->(customer);

MATCH (customer:CUSTOMER), (nation:NATION)
WHERE customer.C_NATIONKEY = nation.N_NATIONKEY
CREATE (customer)-[:FROM]->(nation);

MATCH (supplier:SUPPLIER), (nation:NATION)
WHERE supplier.S_NATIONKEY = nation.N_NATIONKEY
CREATE (supplier)-[:FROM]->(nation);

MATCH (nation:NATION), (region:REGION)
WHERE nation.N_REGIONKEY = region.R_REGIONKEY
CREATE (nation)-[:LOCATED_IN]->(region);

MATCH (lineitem:LINEITEM), (partsupp:PARTSUPP)
WHERE lineitem.L_PARTKEY = partsupp.PS_PARTKEY AND lineitem.L_SUPPKEY = partsupp.PS_SUPPKEY
CREATE (lineitem)-[:HAS_DETAILS]->(partsupp);

MATCH (partsupp:PARTSUPP), (part:PART)
WHERE partsupp.PS_PARTKEY = part.P_PARTKEY
CREATE (partsupp)-[:SUPPLIED_BY]->(part);

MATCH (partsupp:PARTSUPP), (supplier:SUPPLIER)
WHERE partsupp.PS_SUPPKEY = supplier.S_SUPPKEY
CREATE (partsupp)-[:SUPPLIED_BY]->(supplier);

-- CREATE CONSTRAINT CONS_LINENUMBER FOR (l:LINEITEM) REQUIRE l.L_LINENUMBER IS UNIQUE;