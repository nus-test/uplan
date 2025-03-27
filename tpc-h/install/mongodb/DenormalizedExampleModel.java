import java.io.*;
import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.regex.Pattern;

import com.mongodb.MongoClient;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import org.bson.Document;

public class DenormalizedExampleModel {

    private MongoCollection<Document> denormalized_order;

    ArrayList<Document> parts = new ArrayList<Document>();
    ArrayList<Document> nations = new ArrayList<Document>();
    ArrayList<Document> regions = new ArrayList<Document>();
    ArrayList<Document> lineitems = new ArrayList<Document>();
    ArrayList<Document> partsupps = new ArrayList<Document>();
    ArrayList<Document> suppliers = new ArrayList<Document>();
    ArrayList<Document> customers = new ArrayList<Document>();


    private MongoClient mongoClient;
    private MongoDatabase database;

    public static void main(String[] args) {

        MongoClient mongoClient = new MongoClient("localhost", 27017);
        DenormalizedExampleModel model = new DenormalizedExampleModel(mongoClient);

        model.initialiseData();

    }

    DateFormat format = new SimpleDateFormat("yyyy-mm-dd",
            java.util.Locale.ENGLISH);


    public DenormalizedExampleModel(MongoClient mongoClient) {

        this.mongoClient = mongoClient;

        this.database = this.mongoClient.getDatabase("mydb");
    }

    void initialiseData() {

        createPart();
        createRegion();
        createNation();
        createCustomer();
        createSupplier();
        createPartSupp();
        createLineItem();
        createOrder();
    }

    void createPart() {

        File file = new File("part.tbl");


        try (BufferedReader br = new BufferedReader(new FileReader(file))) {
            String line;

            while ((line = br.readLine()) != null) {
                // process the line.

                String[] lineFields = line.split(Pattern.quote("|"));

                Document part = new Document();

                part.append("PARTKEY", lineFields[0])
                        .append("NAME", lineFields[1]).append("MFGR", lineFields[2])
                        .append("BRAND", lineFields[3]).append("TYPE", lineFields[4])
                        .append("SIZE", lineFields[5])
                        .append("CONTAINER", lineFields[6]).append("RETAILPRICE", Double.valueOf(lineFields[7])).append("COMMENT", lineFields[8]);

                this.parts.add(part);
            }

        } catch (FileNotFoundException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }


    }

    void createCustomer() {


        File file = new File("customer.tbl");


        try (BufferedReader br = new BufferedReader(new FileReader(file))) {
            String line;

            while ((line = br.readLine()) != null) {
                // process the line.

                String[] lineFields = line.split(Pattern.quote("|"));

                Document customer = new Document();

                customer.append("CUSTKEY", lineFields[0])
                        .append("NAME", lineFields[1]).append("ADDRESS", lineFields[2])
                        .append("PHONE", lineFields[4]).append("ACCTBAL", Double.valueOf(lineFields[5]))
                        .append("MKTSEGMENT", lineFields[6])
                        .append("COMMENT", lineFields[7]);


                for (Document nation : this.nations) {
                    if (nation.get("NATIONKEY").equals(lineFields[3])) {
                        customer.append("Nation", nation);
                    }
                }

                this.customers.add(customer);
            }

        } catch (FileNotFoundException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }

    }

    void createSupplier() {

        File file = new File("supplier.tbl");

        try (BufferedReader br = new BufferedReader(new FileReader(file))) {
            String line;

            while ((line = br.readLine()) != null) {
                // process the line.

                String[] lineFields = line.split(Pattern.quote("|"));

                Document supplier = new Document();

                supplier.append("SUPPKEY", lineFields[0])
                        .append("NAME", lineFields[1]).append("ADDRESS", lineFields[2])
                        .append("PHONE", lineFields[4]).append("ACCTBAL", Double.valueOf(lineFields[5]))
                        .append("COMMENT", lineFields[6]);

                for (Document nation : this.nations) {
                    if (nation.get("NATIONKEY").equals(lineFields[3])) {
                        supplier.append("Nation", nation);
                    }
                }

                this.suppliers.add(supplier);
            }

        } catch (FileNotFoundException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }

    void createPartSupp() {

        File file = new File("partsupp.tbl");


        try (BufferedReader br = new BufferedReader(new FileReader(file))) {
            String line;

            while ((line = br.readLine()) != null) {
                // process the line.

                String[] lineFields = line.split(Pattern.quote("|"));

                Document partsupp = new Document();

                partsupp.append("PARTKEY", lineFields[0]).append("SUPPKEY", lineFields[1]).append("AVAILQTY", Double.valueOf(lineFields[2]))
                        .append("SUPPLYCOST", Double.valueOf(lineFields[3])).append("COMMENT", lineFields[4]);

                for (Document supplier : this.suppliers) {
                    if (supplier.get("SUPPKEY").equals(lineFields[1])) {
                        partsupp.append("Supplier", supplier);
                    }
                }

                for (Document part : this.parts) {
                    if (part.get("PARTKEY").equals(lineFields[0])) {
                        partsupp.append("Part", part);
                    }
                }

                this.partsupps.add(partsupp);
            }

        } catch (FileNotFoundException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }

    }

    void createOrder() {

        File file = new File("orders.tbl");

        if (this.database.getCollection("orders") == null) {
            this.database.createCollection("orders");
        } else {
            this.database.getCollection("orders").drop();
            this.database.createCollection("orders");
        }

        denormalized_order = this.database
                .getCollection("orders");

        try (BufferedReader br = new BufferedReader(new FileReader(file))) {
            String line;

            while ((line = br.readLine()) != null) {
                // process the line.

                String[] lineFields = line.split(Pattern.quote("|"));

                Document orders = new Document();

                orders.append("ORDERKEY", lineFields[0])
                        .append("ORDERSTATUS", lineFields[2])
                        .append("TOTALPRICE", Double.valueOf(lineFields[3])).append("ORDERDATE", format.parse(lineFields[4]))
                        .append("ORDERPRIORITY", lineFields[5]).append("CLERK", lineFields[6])
                        .append("SHIPPRIORITY", lineFields[7]).append("COMMENT", lineFields[8]);

                ArrayList<Document> items = new ArrayList<Document>();
                for (Document lineitem : this.lineitems) {
                    if (lineitem.get("ORDERKEY").equals(lineFields[0])) {
                        items.add(lineitem);
                    }
                }

                for (Document customer : this.customers) {
                    if (customer.get("CUSTKEY").equals(lineFields[1])) {
                        orders.append("Customer", customer);
                    }
                }


                orders.append("Items", items);

                this.denormalized_order.insertOne(orders);
            }

        } catch (FileNotFoundException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        } catch (ParseException e) {
            e.printStackTrace();
        }
    }

    void createRegion() {

        File file = new File("region.tbl");


        try (BufferedReader br = new BufferedReader(new FileReader(file))) {
            String line;

            while ((line = br.readLine()) != null) {
                // process the line.

                String[] lineFields = line.split(Pattern.quote("|"));

                Document region = new Document();

                region.append("REGIONKEY", lineFields[0])
                        .append("NAME", lineFields[1]).append("COMMENT", lineFields[2]);

                this.regions.add(region);
            }

        } catch (FileNotFoundException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }

    void createNation() {

        File file = new File("nation.tbl");


        try (BufferedReader br = new BufferedReader(new FileReader(file))) {
            String line;

            while ((line = br.readLine()) != null) {
                // process the line.

                String[] lineFields = line.split(Pattern.quote("|"));

                Document nation = new Document();

                nation.append("NATIONKEY", lineFields[0])
                        .append("NAME", lineFields[1]).append("COMMENT", lineFields[3]);

                for (Document region : this.regions) {
                    if (region.get("REGIONKEY").equals(lineFields[2])) {
                        nation.append("Region", region);
                    }
                }

                this.nations.add(nation);
            }

        } catch (FileNotFoundException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }

    void createLineItem() {

        File file = new File("lineitem.tbl");


        try (BufferedReader br = new BufferedReader(new FileReader(file))) {
            String line;

            while ((line = br.readLine()) != null) {
                // process the line.

                String[] lineFields = line.split(Pattern.quote("|"));

                Document lineitem = new Document();

                lineitem.append("ORDERKEY", lineFields[0]).append("LINENUMBER", lineFields[3])
                        .append("QUANTITY", Double.valueOf(lineFields[4])).append("EXTENDEDPRICE", Double.valueOf(lineFields[5]))
                        .append("DISCOUNT", Double.valueOf(lineFields[6])).append("TAX", Double.valueOf(lineFields[7]))
                        .append("RETURNFLAG", lineFields[8]).append("LINESTATUS", lineFields[9])
                        .append("SHIPDATE", format.parse(lineFields[10])).append("COMMITDATE", format.parse(lineFields[11]))
                        .append("RECEIPTDATE", format.parse(lineFields[12])).append("SHIPINSTRUCT", lineFields[13])
                        .append("SHIPMODE", lineFields[14]).append("COMMENT", lineFields[15]);

                for (Document partsupp : this.partsupps) {
                    if (partsupp.get("PARTKEY").equals(lineFields[1]) && partsupp.get("SUPPKEY").equals(lineFields[2])) {
                        lineitem.append("PartSupp", partsupp);
                    }
                }

                this.lineitems.add(lineitem);
            }

        } catch (FileNotFoundException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        } catch (ParseException e) {
            e.printStackTrace();
        }
    }
}
