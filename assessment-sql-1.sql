SELECT inv.id          AS Invoice_ID,
       inv.billingdate AS Billing_Date,
       cus.name        AS Customer_Name,
       ref_cus.name    AS Referred_By_Customer_Name
FROM   invoices inv
       LEFT JOIN customers cus
              ON inv.customerid = cus.id
       LEFT JOIN customers ref_cus
              ON cus.referredby = ref_cus.id
ORDER  BY inv.billingdate 